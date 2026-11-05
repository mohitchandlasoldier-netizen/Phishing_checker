# Phishing_checker
# EWB Phishing URL Awareness Checker

## Overview
Phishing is a trick where a criminal sends a fake link or message to make you share a password, card number or OTP. This small Python command-line tool reads the text of a URL and points out a few visible warning signs. It never opens the link, so nothing is visited or sent anywhere.

## Features
- Detects an @ symbol in the URL
- Flags unusually long URLs (over 100 characters)
- Flags IP-address hostnames
- Flags many hostname segments (5 or more)
- Flags punycode-style hostnames (xn--)
- Flags the HTTP scheme
- Loop mode: check many URLs in one run, type `q` to quit
- "REVIEW CAREFULLY" summary with the number of warning signs found
- Safe handling of malformed input such as `http://[bad` (no crash)
- A one-line "Why" explanation under every warning

## Requirements
Python 3.10 or later. No extra packages.

## How to Run
Windows: python phishing_checker.py
Mac/Linux: python3 phishing_checker.py

## Example Output
```
EWB Phishing URL Awareness Checker
Text checks only - this program does not open URLs.

Enter a sample URL (or type q to quit): http://192.0.2.10/account

Result:
- Uses an IP address instead of a familiar domain.
    Why: Honest services normally use readable names; a bare number hides who owns the site.
- Uses HTTP. HTTPS alone does not prove trust.
    Why: HTTP is not encrypted, so data can be seen on the way. HTTPS alone still does not prove trust.

REVIEW CAREFULLY: 2 warning sign(s) found.
Never enter passwords from unexpected links.
```

## Testing
| # | Input | Expected | Actual | Result |
|---|-------|----------|--------|--------|
| 1 | https://www.example.com/login | No warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP address + HTTP | IP address warning + HTTP warning | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol + HTTP | @ symbol warning + HTTP warning | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments | Many hostname segments warning | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname | Punycode-style hostname warning | PASS |

The full table with exact output is in `tests/test_samples.md`.

## Screenshots
![Sample run](screenshots/sample_run.png)
![Test results](screenshots/test_results.png)

## Improvements
1. Loop with quit - the program used to stop after one URL. Now a `while True` loop keeps asking until the user types `q`, `quit` or `exit`. I tested it by running several URLs in one session and then quitting.
2. "Review carefully" summary - a helper function `has_warnings()` separates real warnings from information messages (like "No URL entered"), and the program prints how many warning signs were found. I tested it with URLs that have warnings and with ones that do not.
3. Safe handling of malformed input - `urlparse` is wrapped in `try / except ValueError`, so `http://[bad` prints "This text is not a valid URL format." instead of crashing. I tested it with that exact input.
4. Simple explanations - a `REASONS` dictionary prints a one-line "Why" under each warning, so the user learns why the clue matters.

After every change I re-ran all five sample tests and they still pass.

## Limitations
This is an educational tool. It only reads URL text. It does not visit
URLs, scan for malware or prove that a URL is safe. No warning signs
found does NOT mean a URL is safe.

## Ethical Use
Use sample strings only. Do not collect credentials. Do not use this
project to deceive anyone or to test websites without permission.

## Author
[Mohit], [], EWB Courses
