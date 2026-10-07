package test.talkdesk;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.format.DateTimeFormatter;
import java.util.*;


@SpringBootApplication
public class TalkDeskApplication {
    public static void main(String[] args) {
        SpringApplication.run(TalkDeskApplication.class, args);
    }
}

@RestController
class TalkDeskController {

    private static final Set<String> TRACKS =
            Set.of("testing", "architecture", "delivery", "culture");
    private static final Set<String> STATUSES =
            Set.of("submitted", "accepted", "rejected");
    private static final DateTimeFormatter ISO = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    private final JdbcTemplate jdbc;

    TalkDeskController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    // ────────────────────────────────────────────────── health
    @GetMapping("/health")
    Map<String, String> health() {
        jdbc.queryForObject("SELECT 1", Integer.class);
        return Map.of("status", "ok");
    }

    // ────────────────────────────────────────────────── API
    
    @GetMapping("/api/talks")
    List<Map<String, Object>> listTalks(@RequestParam(required = false) String track,
                                        @RequestParam(required = false) String status) {
        StringBuilder sql = new StringBuilder("SELECT * FROM talks WHERE 1=1");
        List<Object> args = new ArrayList<>();
        if (track != null)  { sql.append(" AND track = ?");  args.add(track); }
        if (status != null) { sql.append(" AND status = ?"); args.add(status); }
        sql.append(" ORDER BY id LIMIT 100");

        List<Map<String, Object>> rows = jdbc.query(sql.toString(), this::rowToTalk, args.toArray());
        for (Map<String, Object> t : rows) {

            Map<String, Object> sp = jdbc.queryForMap(
                    "SELECT id, name FROM speakers WHERE id = ?", t.remove("speaker_id"));
            t.put("speaker", Map.of("id", sp.get("id"), "name", sp.get("name")));
        }
        return rows;
    }

    
    @GetMapping("/api/talks/search")
    List<Map<String, Object>> search(@RequestParam(defaultValue = "") String q) {
        return jdbc.query(
                "SELECT t.*, s.name AS speaker_name FROM talks t " +
                "JOIN speakers s ON s.id = t.speaker_id " +
                "WHERE t.title ILIKE ? ORDER BY t.id LIMIT 100",
                (rs, i) -> {
                    Map<String, Object> t = rowToTalk(rs, i);
                    t.put("speaker", Map.of("id", t.remove("speaker_id"),
                                            "name", rs.getString("speaker_name")));
                    return t;
                }, "%" + q + "%");
    }

    
    @GetMapping("/api/talks/{id}")
    Map<String, Object> getTalk(@PathVariable String id) {
        int talkId = Integer.parseInt(id);                       // deliberately unguarded
        List<Map<String, Object>> found = jdbc.query(
                "SELECT * FROM talks WHERE id = ?", this::rowToTalk, talkId);
        if (found.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "talk not found");
        }
        Map<String, Object> t = found.get(0);
        Map<String, Object> sp = jdbc.queryForMap(
                "SELECT * FROM speakers WHERE id = ?", t.remove("speaker_id"));
        t.put("abstract", jdbc.queryForObject(
                "SELECT abstract FROM talks WHERE id = ?", String.class, talkId));
        t.put("speaker", mapOfNullable("id", sp.get("id"), "name", sp.get("name"),
                                       "email", sp.get("email"), "bio", sp.get("bio")));
        return t;
    }

    
    @PostMapping("/api/talks")
    ResponseEntity<Map<String, Object>> create(@RequestBody Map<String, Object> body) {
        String title = String.valueOf(body.getOrDefault("title", "")).trim();
        String track = String.valueOf(body.getOrDefault("track", ""));
        if (title.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "title is required");
        }
        if (!TRACKS.contains(track)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "invalid track");
        }
        Integer speakerId = ((Number) body.get("speaker_id")).intValue();
        Integer exists = jdbc.query("SELECT 1 FROM speakers WHERE id = ?",
                rs -> rs.next() ? 1 : null, speakerId);
        if (exists == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "speaker not found");
        }
        Map<String, Object> created = jdbc.queryForObject(
                "INSERT INTO talks (speaker_id,title,abstract,track) VALUES (?,?,?,?) RETURNING *",
                this::rowToTalk, speakerId, title,
                String.valueOf(body.getOrDefault("abstract", "")), track);
        created.put("speaker", Map.of("id", created.remove("speaker_id")));
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    
    @PatchMapping("/api/talks/{id}")
    Map<String, Object> patch(@PathVariable int id, @RequestBody Map<String, Object> body) {
        String status = body.get("status") == null ? null : String.valueOf(body.get("status"));
        Integer score = body.get("score") == null ? null : ((Number) body.get("score")).intValue();
        if (status != null && !STATUSES.contains(status)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "invalid status");
        }
        if (score != null && (score < 1 || score > 10)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "score must be 1..10");
        }
        List<String> sets = new ArrayList<>();
        List<Object> args = new ArrayList<>();
        if (status != null) { sets.add("status = ?"); args.add(status); }
        if (score != null)  { sets.add("score = ?");  args.add(score); }
        if (sets.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "nothing to update");
        }
        args.add(id);
        List<Map<String, Object>> updated = jdbc.query(
                "UPDATE talks SET " + String.join(", ", sets) + " WHERE id = ? RETURNING *",
                this::rowToTalk, args.toArray());
        if (updated.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "talk not found");
        }
        Map<String, Object> t = updated.get(0);
        t.remove("speaker_id");
        return t;
    }

    
    @PostMapping("/api/login")
    Map<String, String> login(@RequestBody Map<String, String> body) {
        String email = String.valueOf(body.getOrDefault("email", ""));
        String password = String.valueOf(body.getOrDefault("password", ""));
        if (email.endsWith("@talkdesk.test") && "reviewer".equals(password)) {
            return Map.of("token", "talkdesk-demo-token-not-a-credential");
        }
        throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "invalid credentials");
    }

    // ────────────────────────────────────────────────── HTML
    
    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    String home() {
        StringBuilder rows = new StringBuilder();
        for (Map<String, Object> t : listTalks(null, null).subList(0, 50)) {
            @SuppressWarnings("unchecked")
            Map<String, Object> sp = (Map<String, Object>) t.get("speaker");
            rows.append("<tr><td><a href=\"/api/talks/").append(t.get("id")).append("\">")
                .append(esc(String.valueOf(t.get("title")))).append("</a></td><td>")
                .append(esc(String.valueOf(sp.get("name")))).append("</td><td>")
                .append(t.get("track")).append("</td><td><span class=\"badge-")
                .append(t.get("status")).append("\">").append(t.get("status"))
                .append("</span></td></tr>");
        }
        return page("Talks", "<h2>Submitted talks</h2><table><thead><tr>" +
                "<th>Title</th><th>Speaker</th><th>Track</th><th>Status</th>" +
                "</tr></thead><tbody>" + rows + "</tbody></table>");
    }

    
    @GetMapping(value = "/submit", produces = MediaType.TEXT_HTML_VALUE)
    String submitForm() {
        return page("Submit a talk", """
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
            </form>""");
    }

    @GetMapping(value = "/login", produces = MediaType.TEXT_HTML_VALUE)
    String loginForm() {
        return page("Sign in", """
            <h2>Reviewer sign-in</h2>
            <form method="post" action="/api/login">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" required>
              <label for="password">Password</label>
              <input id="password" name="password" type="password" required>
              <button type="submit">Sign in</button>
            </form>""");
    }

    // ────────────────────────────────────────────────── helpers
    private Map<String, Object> rowToTalk(ResultSet rs, int i) throws SQLException {
        Map<String, Object> t = new LinkedHashMap<>();
        t.put("id", rs.getInt("id"));
        t.put("title", rs.getString("title"));
        t.put("track", rs.getString("track"));
        t.put("status", rs.getString("status"));
        int score = rs.getInt("score");
        t.put("score", rs.wasNull() ? null : score);
        t.put("speaker_id", rs.getInt("speaker_id"));
        t.put("created_at", rs.getTimestamp("created_at").toLocalDateTime().format(ISO) + "Z");
        return t;
    }

    private static Map<String, Object> mapOfNullable(Object... kv) {
        Map<String, Object> m = new LinkedHashMap<>();
        for (int i = 0; i < kv.length; i += 2) m.put(String.valueOf(kv[i]), kv[i + 1]);
        return m;
    }

    private static String esc(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }

    
    private static String page(String title, String body) {
        return """
            <!doctype html>
            <html lang="en">
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>%s · TalkDesk</title>
            <style>
              body { font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 60rem; color:#222; }
              nav a { margin-right: 1rem; }
              table { border-collapse: collapse; width: 100%%; }
              th, td { text-align: left; padding: .5rem; border-bottom: 1px solid #ddd; }
              .badge-submitted { color: #c8c8c8; }
              .badge-accepted  { color: #1a7f37; }
              .badge-rejected  { color: #a40e26; }
              label { display:block; margin-top:1rem; font-weight:600; }
              input, textarea, select { width:100%%; padding:.4rem; }
              button { margin-top:1rem; padding:.5rem 1rem; }
            </style>
            </head>
            <body>
            <h1>TalkDesk</h1>
            <nav><a href="/">Talks</a><a href="/submit">Submit a talk</a><a href="/login">Sign in</a></nav>
            %s
            </body>
            </html>""".formatted(title, body);
    }
}
