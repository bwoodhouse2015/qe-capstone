# TalkDesk — the reference System Under Test

A conference talk-submission desk, supplied with the program as a **safety net**.

If your own System Under Test collapses — it will not build, the licence turns
out to be wrong, your employer says no — switch to this one and carry on. You
lose nothing: it satisfies every criterion in Week 1 §0.2, it ships with a
Dockerfile, and it is small enough to read in an afternoon.

**It is not a template for your own project.** You choose that on Week 1, Day 1
and keep it for four weeks. This is the fallback.

## Run it

**It needs Docker, and nothing else.** Week 0 installs it; `./scripts/verify-setup.sh`
in your starter repository tells you whether it is working.

```bash
docker compose --profile python up -d --wait     # or java, or dotnet
```

Then open http://localhost:8080. Stop it with `docker compose down`.

Three implementations of one contract, so whichever language you picked in
Week 0, there is a version in it.

| What you see | What to do |
|---|---|
| `Cannot connect to the Docker daemon` | Docker is not running. Start Docker Desktop, or `sudo service docker start` |
| It hangs on `--wait` | The database is still coming up on a first run. Give it a minute; then `docker compose logs` |
| `port is already allocated` | Something else holds 8080. Stop it, or edit the port mapping in `docker-compose.yml` |
| The Java or .NET profile fails to build | Both need to download dependencies on first build. Check your network, or use `--profile python`, which is the one verified end to end |

> **Localhost only.** The compose file binds `127.0.0.1` on purpose. This is a
> teaching fixture with known weaknesses — do not put it anywhere public.

## What is in here

| | |
|---|---|
| `python/`, `java/`, `dotnet/` | the three implementations |
| `db/` | schema and seed data |
| `tests/` | a starting test suite — deliberately incomplete, which is the point |
| `docker-compose.yml` | brings up the database and whichever implementation you name |

**`tests/` is not a finished suite.** It is what a real project hands you: some
coverage, some gaps, and no map of which is which. Finding out is the work.
