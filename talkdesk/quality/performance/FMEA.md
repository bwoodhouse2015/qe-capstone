# Failure Mode and Effects Analysis (FMEA)

| Failure Mode | Effect | Detection | Severity | Mitigation |
|-------------|---------|-----------|----------|------------|
| High concurrent load | Increased p95 latency | k6 thresholds | 4 | Horizontal scaling |
| Database saturation | Slow responses | Health endpoint / latency monitoring | 5 | Connection pooling |
| Application process failure | Service unavailable | Health checks | 5 | Auto restart and monitoring |
