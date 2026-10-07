// TalkDesk — reference System Under Test, C# implementation.
//
// Conforms to contract/CONTRACT.md. Deliberately imperfect: every weakness is

// without reading the contract — a defect silently removed is a Week 3 exercise
// silently removed.

using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Npgsql;

// The container healthcheck runs this same binary with --healthcheck rather
// than shelling out to curl, which the aspnet runtime image does not ship.
if (args.Contains("--healthcheck"))
{
    using var probe = new HttpClient { Timeout = TimeSpan.FromSeconds(3) };
    try
    {
        var r = await probe.GetAsync("http://localhost:8080/health");
        return r.IsSuccessStatusCode ? 0 : 1;
    }
    catch { return 1; }
}

var builder = WebApplication.CreateBuilder(args);
builder.Services.ConfigureHttpJsonOptions(o =>
{
    o.SerializerOptions.PropertyNamingPolicy = null;          // the contract uses snake_case keys verbatim
    o.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.Never;
});

// unhandled error discloses a stack trace. ZAP's baseline scan reports it.
var app = builder.Build();
app.UseDeveloperExceptionPage();

var connString = Environment.GetEnvironmentVariable("DB_URL")
    ?? "Host=localhost;Port=5432;Database=talkdesk;Username=talkdesk;Password=talkdesk";

string[] Tracks = ["testing", "architecture", "delivery", "culture"];
string[] Statuses = ["submitted", "accepted", "rejected"];

NpgsqlConnection Db()
{
    var c = new NpgsqlConnection(connString);
    c.Open();
    return c;
}

static string Iso(DateTime d) => d.ToString("yyyy-MM-ddTHH:mm:ss") + "Z";

// ────────────────────────────────────────────────────────── health
app.MapGet("/health", () =>
{
    try
    {
        using var c = Db();
        using var cmd = new NpgsqlCommand("SELECT 1", c);
        cmd.ExecuteScalar();
        return Results.Ok(new Dictionary<string, object?> { ["status"] = "ok" });
    }
    catch
    {
        return Results.Json(new Dictionary<string, object?> { ["status"] = "degraded" },
                            statusCode: 503);
    }
});

// ────────────────────────────────────────────────────────── API

// speaker: 101 round trips for a page of 100. A single JOIN is the correct
// implementation, and Week 3's load test is what makes the difference visible.
app.MapGet("/api/talks", (string? track, string? status) =>
{
    using var c = Db();
    var sql = new StringBuilder("SELECT * FROM talks WHERE 1=1");
    using var cmd = new NpgsqlCommand { Connection = c };
    if (track is not null)  { sql.Append(" AND track = @track");   cmd.Parameters.AddWithValue("track", track); }
    if (status is not null) { sql.Append(" AND status = @status"); cmd.Parameters.AddWithValue("status", status); }
    sql.Append(" ORDER BY id LIMIT 100");
    cmd.CommandText = sql.ToString();

    var rows = new List<(Dictionary<string, object?> talk, int speakerId)>();
    using (var r = cmd.ExecuteReader())
        while (r.Read()) rows.Add((ReadTalk(r), r.GetInt32(r.GetOrdinal("speaker_id"))));

    var outList = new List<Dictionary<string, object?>>();
    foreach (var (talk, speakerId) in rows)
    {

        using var sc = new NpgsqlCommand("SELECT id, name FROM speakers WHERE id = @id", c);
        sc.Parameters.AddWithValue("id", speakerId);
        using var sr = sc.ExecuteReader();
        sr.Read();
        talk["speaker"] = new Dictionary<string, object?>
        {
            ["id"] = sr.GetInt32(0), ["name"] = sr.GetString(1)
        };
        outList.Add(talk);
    }
    return Results.Ok(outList);
});

// column: a full table scan per request. The statement is parameterised — this
// is a performance defect, not an injection one.
app.MapGet("/api/talks/search", (string? q) =>
{
    using var c = Db();
    using var cmd = new NpgsqlCommand(
        "SELECT t.*, s.name AS speaker_name FROM talks t " +
        "JOIN speakers s ON s.id = t.speaker_id " +
        "WHERE t.title ILIKE @q ORDER BY t.id LIMIT 100", c);
    cmd.Parameters.AddWithValue("q", $"%{q ?? ""}%");

    var outList = new List<Dictionary<string, object?>>();
    using var r = cmd.ExecuteReader();
    while (r.Read())
    {
        var t = ReadTalk(r);
        t["speaker"] = new Dictionary<string, object?>
        {
            ["id"] = r.GetInt32(r.GetOrdinal("speaker_id")),
            ["name"] = r.GetString(r.GetOrdinal("speaker_name"))
        };
        outList.Add(t);
    }
    return Results.Ok(outList);
});

// non-integer throws rather than returning a clean 404.
app.MapGet("/api/talks/{id}", (string id) =>
{
    var talkId = int.Parse(id);                                  // deliberately unguarded
    using var c = Db();
    using var cmd = new NpgsqlCommand("SELECT * FROM talks WHERE id = @id", c);
    cmd.Parameters.AddWithValue("id", talkId);

    Dictionary<string, object?>? talk = null;
    int speakerId = 0;
    string? abstractText = null;
    using (var r = cmd.ExecuteReader())
        if (r.Read())
        {
            talk = ReadTalk(r);
            speakerId = r.GetInt32(r.GetOrdinal("speaker_id"));
            var ao = r.GetOrdinal("abstract");
            abstractText = r.IsDBNull(ao) ? null : r.GetString(ao);
        }
    if (talk is null) return Results.NotFound(new { detail = "talk not found" });

    using var sc = new NpgsqlCommand("SELECT * FROM speakers WHERE id = @id", c);
    sc.Parameters.AddWithValue("id", speakerId);
    using var sr = sc.ExecuteReader();
    sr.Read();
    talk["abstract"] = abstractText;
    talk["speaker"] = new Dictionary<string, object?>
    {
        ["id"] = sr.GetInt32(sr.GetOrdinal("id")),
        ["name"] = sr.GetString(sr.GetOrdinal("name")),
        ["email"] = sr.GetString(sr.GetOrdinal("email")),
        ["bio"] = sr.IsDBNull(sr.GetOrdinal("bio")) ? null : sr.GetString(sr.GetOrdinal("bio"))
    };
    return Results.Ok(talk);
});

app.MapPost("/api/talks", (JsonElement body) =>
{
    var title = body.TryGetProperty("title", out var tv) ? (tv.GetString() ?? "").Trim() : "";
    var track = body.TryGetProperty("track", out var kv) ? kv.GetString() ?? "" : "";
    if (title.Length == 0) return Results.BadRequest(new { detail = "title is required" });
    if (!Tracks.Contains(track)) return Results.BadRequest(new { detail = "invalid track" });

    var speakerId = body.GetProperty("speaker_id").GetInt32();
    var abs = body.TryGetProperty("abstract", out var av) ? av.GetString() ?? "" : "";

    using var c = Db();
    using (var check = new NpgsqlCommand("SELECT 1 FROM speakers WHERE id = @id", c))
    {
        check.Parameters.AddWithValue("id", speakerId);
        if (check.ExecuteScalar() is null)
            return Results.NotFound(new { detail = "speaker not found" });
    }
    using var cmd = new NpgsqlCommand(
        "INSERT INTO talks (speaker_id,title,abstract,track) VALUES (@s,@t,@a,@k) RETURNING *", c);
    cmd.Parameters.AddWithValue("s", speakerId);
    cmd.Parameters.AddWithValue("t", title);
    cmd.Parameters.AddWithValue("a", abs);
    cmd.Parameters.AddWithValue("k", track);
    using var r = cmd.ExecuteReader();
    r.Read();
    var created = ReadTalk(r);
    created["speaker"] = new Dictionary<string, object?> { ["id"] = speakerId };
    return Results.Created($"/api/talks/{created["id"]}", created);
});

// tests/. A valid score runs the check; nothing runs the rejection.
app.MapMethods("/api/talks/{id}", ["PATCH"], (int id, JsonElement body) =>
{
    string? status = body.TryGetProperty("status", out var sv) ? sv.GetString() : null;
    int? score = body.TryGetProperty("score", out var cv) && cv.ValueKind == JsonValueKind.Number
        ? cv.GetInt32() : null;

    if (status is not null && !Statuses.Contains(status))
        return Results.BadRequest(new { detail = "invalid status" });
    if (score is not null && (score < 1 || score > 10))
        return Results.BadRequest(new { detail = "score must be 1..10" });

    var sets = new List<string>();
    using var c = Db();
    using var cmd = new NpgsqlCommand { Connection = c };
    if (status is not null) { sets.Add("status = @st"); cmd.Parameters.AddWithValue("st", status); }
    if (score is not null)  { sets.Add("score = @sc");  cmd.Parameters.AddWithValue("sc", score.Value); }
    if (sets.Count == 0) return Results.BadRequest(new { detail = "nothing to update" });

    cmd.Parameters.AddWithValue("id", id);
    cmd.CommandText = $"UPDATE talks SET {string.Join(", ", sets)} WHERE id = @id RETURNING *";
    using var r = cmd.ExecuteReader();
    if (!r.Read()) return Results.NotFound(new { detail = "talk not found" });
    return Results.Ok(ReadTalk(r));
});

// a fixed comparison; this system does not teach authentication. What it teaches
// is that an endpoint accepting unlimited attempts is a finding.
app.MapPost("/api/login", (JsonElement body) =>
{
    var email = body.TryGetProperty("email", out var e) ? e.GetString() ?? "" : "";
    var password = body.TryGetProperty("password", out var p) ? p.GetString() ?? "" : "";
    if (email.EndsWith("@talkdesk.test") && password == "reviewer")
        return Results.Ok(new Dictionary<string, object?>
        {
            ["token"] = "talkdesk-demo-token-not-a-credential"
        });
    return Results.Json(new { detail = "invalid credentials" }, statusCode: 401);
});

// ────────────────────────────────────────────────────────── HTML

// X-Frame-Options on any HTML response. ZAP's baseline scan reports all four.

string Page(string title, string body) => $$"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{title}} · TalkDesk</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 60rem; color:#222; }
      nav a { margin-right: 1rem; }
      table { border-collapse: collapse; width: 100%; }
      th, td { text-align: left; padding: .5rem; border-bottom: 1px solid #ddd; }
      .badge-submitted { color: #c8c8c8; }
      .badge-accepted  { color: #1a7f37; }
      .badge-rejected  { color: #a40e26; }
      label { display:block; margin-top:1rem; font-weight:600; }
      input, textarea, select { width:100%; padding:.4rem; }
      button { margin-top:1rem; padding:.5rem 1rem; }
    </style>
    </head>
    <body>
    <h1>TalkDesk</h1>
    <nav><a href="/">Talks</a><a href="/submit">Submit a talk</a><a href="/login">Sign in</a></nav>
    {{body}}
    </body>
    </html>
    """;

app.MapGet("/", () =>
{
    using var c = Db();
    using var cmd = new NpgsqlCommand(
        "SELECT t.id, t.title, t.track, t.status, s.name AS speaker_name FROM talks t " +
        "JOIN speakers s ON s.id = t.speaker_id ORDER BY t.id LIMIT 50", c);
    var sb = new StringBuilder();
    using var r = cmd.ExecuteReader();
    while (r.Read())
        sb.Append($"<tr><td><a href=\"/api/talks/{r.GetInt32(0)}\">{Esc(r.GetString(1))}</a></td>")
          .Append($"<td>{Esc(r.GetString(4))}</td><td>{r.GetString(2)}</td>")
          .Append($"<td><span class=\"badge-{r.GetString(3)}\">{r.GetString(3)}</span></td></tr>");

    return Results.Content(Page("Talks",
        "<h2>Submitted talks</h2><table><thead><tr><th>Title</th><th>Speaker</th>" +
        $"<th>Track</th><th>Status</th></tr></thead><tbody>{sb}</tbody></table>"),
        "text/html; charset=utf-8");
});

app.MapGet("/submit", () => Results.Content(Page("Submit a talk", """
    <h2>Submit a talk</h2>
    <form method="post" action="/api/talks">
      <label for="speaker_id">Speaker ID</label>
      <input id="speaker_id" name="speaker_id" type="number" required>
      <label for="title">Title</label>
      <input id="title" name="title" type="text" required>
      <!-- no <label>, no aria-label, no title attribute -->
      <textarea id="abstract" name="abstract" rows="5"></textarea>
      <label for="track">Track</label>
      <select id="track" name="track">
        <option>testing</option><option>architecture</option>
        <option>delivery</option><option>culture</option>
      </select>
      <button type="submit">Submit</button>
    </form>
    """), "text/html; charset=utf-8"));

app.MapGet("/login", () => Results.Content(Page("Sign in", """
    <h2>Reviewer sign-in</h2>
    <form method="post" action="/api/login">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" required>
      <label for="password">Password</label>
      <input id="password" name="password" type="password" required>
      <button type="submit">Sign in</button>
    </form>
    """), "text/html; charset=utf-8"));

app.Run("http://0.0.0.0:8080");

// ────────────────────────────────────────────────────────── helpers
static Dictionary<string, object?> ReadTalk(NpgsqlDataReader r)
{
    var scoreOrd = r.GetOrdinal("score");
    return new Dictionary<string, object?>
    {
        ["id"] = r.GetInt32(r.GetOrdinal("id")),
        ["title"] = r.GetString(r.GetOrdinal("title")),
        ["track"] = r.GetString(r.GetOrdinal("track")),
        ["status"] = r.GetString(r.GetOrdinal("status")),
        ["score"] = r.IsDBNull(scoreOrd) ? null : r.GetInt32(scoreOrd),
        ["created_at"] = Iso(r.GetDateTime(r.GetOrdinal("created_at")))
    };
}

static string Esc(string s) =>
    s.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;");
