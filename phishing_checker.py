import re
from urllib.parse import urlparse

# Messages that are information only, not real warning signs.
INFO_MESSAGES = (
    "No URL entered",
    "Could not identify",
    "This text is not a valid URL",
    "No listed warning",
)

# Improvement D: a short reason for each warning, shown under the warning.
REASONS = {
    "Contains an @ symbol": "The browser ignores the text before @, so the link can look like one site but go to another.",
    "Unusually long URL": "A long link can hide the real destination far to the right.",
    "Uses an IP address": "Honest services normally use readable names; a bare number hides who owns the site.",
    "Contains many hostname": "Stacking many names makes a link look official while hiding the real domain.",
    "Contains a punycode": "Punycode can hide look-alike foreign letters that imitate a real name.",
    "Uses HTTP": "HTTP is not encrypted, so data can be seen on the way. HTTPS alone still does not prove trust.",
}


def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    # Improvement C: malformed input (for example http://[bad) must not crash.
    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def has_warnings(findings):
    """True if the findings contain real warnings, not just information messages."""
    return not findings[0].startswith(INFO_MESSAGES)


def reason_for(finding):
    """Return the simple-words reason for a warning, or None."""
    for start, reason in REASONS.items():
        if finding.startswith(start):
            return reason
    return None


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    # Improvement A: loop so several URLs can be checked without restarting.
    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except EOFError:
            print("\nGoodbye! Stay alert online.")
            break

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)
            reason = reason_for(item)
            if reason:
                print("    Why: " + reason)

        # Improvement B: clear summary when real warnings are found.
        if has_warnings(findings):
            print("\nREVIEW CAREFULLY: " + str(len(findings)) + " warning sign(s) found.")

        print("Never enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
