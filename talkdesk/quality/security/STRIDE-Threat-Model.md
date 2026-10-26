# STRIDE Threat Model

## Feature: Health Endpoint (/health)

| Threat | Example | Mitigation |
|----------|----------|----------|
| Spoofing | Unauthorized client impersonates service | Authentication and network controls |
| Tampering | Response modified in transit | HTTPS/TLS |
| Repudiation | Requests cannot be traced | Logging and audit records |
| Information Disclosure | Sensitive data exposed in responses | Return only status information |
| Denial of Service | Excessive requests degrade service | Rate limiting and autoscaling |
| Elevation of Privilege | User gains higher permissions | Least-privilege access controls |
