# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in `asr-eval-toolkit`, please report it privately:

1. **Email**: Send details to veyhthan@gmail.com with the subject line `[SECURITY] asr-eval-toolkit vulnerability`
2. **Include**:
   - A description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
3. **Response**: You will receive a response within 48 hours. If the vulnerability is confirmed, we will work on a fix and coordinate disclosure.

## Scope

This security policy covers the `asr-eval-toolkit` Python package and its associated repository at `github.com/veyhthan/asr-eval-toolkit`.

## Security Considerations

`asr-eval-toolkit` is a minimal, dependency-free toolkit that processes local transcript files. The primary security considerations are:

- **File paths**: The toolkit reads and writes files based on user-provided paths. Users should only process trusted input files.
- **No network calls**: The toolkit does not make any network requests by design.
- **No code execution**: The toolkit does not execute arbitrary code.

If you discover a vulnerability that contradicts any of these guarantees, please report it using the process above.
