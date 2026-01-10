# Security Policy

## Supported Versions

We actively support the security of the following versions of MesaFlow:

| Version | Supported          |
| ------- | ------------------ |
| 3.1.x   | :white_check_mark: |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a Vulnerability

We take the security of our systems seriously. If you believe you have found a security vulnerability in MesaFlow, please report it to us as described below.

**Do not report security vulnerabilities through public GitHub issues.**

### How to Report

Please send an email to **security@mesaflow.com.br** with the following details:

1.  **Type of Vulnerability:** (e.g., SQL Injection, XSS, IDOR).
2.  **Affected Component:** (e.g., API, Frontend, Mobile App).
3.  **Steps to Reproduce:** A clear, step-by-step guide to reproduce the issue.
4.  **Proof of Concept:** Screenshots or scripts (if applicable).

### Detailed Policies

For more information on our security practices and legal commitments, please refer to:

- [Responsible Disclosure Policy](docs/legal/SECURITY_DISCLOSURE.md)
- [Data Breach Notification Policy](docs/legal/DATA_BREACH_NOTIFICATION.md)
- [Privacy Policy](docs/legal/PRIVACY_POLICY.md)
- [Trust Center](/trust)

### Our Response Process

1.  **Acknowledgement:** We will acknowledge receipt of your report within 48 hours.
2.  **Assessment:** Our security team will assess the severity and impact.
3.  **Fix:** We will work on a fix and release it as soon as possible.
4.  **Disclosure:** Once fixed, we may publicly acknowledge your contribution (with your permission).

## Security Measures

MesaFlow implements the following security measures by design:
- **Row-Level Security (RLS):** Database-level tenant isolation.
- **Encryption:** All data in transit is encrypted via TLS 1.2+.
- **Sanitization:** Inputs are sanitized to prevent Injection attacks.
- **Audit Logs:** Critical actions are logged immutably.
