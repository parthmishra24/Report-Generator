import questionary
import sys

def required_input(message):
    while True:
        answer = questionary.text(message).ask()
        if answer is None:
            print("\n🛑 Operation cancelled.")
            sys.exit(0)
        if answer.strip():
            return answer.strip()
        print("❗ This field is required. Please enter a valid value.\n")

def collect_vulnerabilities():
    vulnerabilities = []

    count_input = questionary.text("🔐 Enter number of vulnerabilities to report:").ask()
    if count_input is None:
        print("\n🛑 Cancelled.")
        sys.exit(0)

    try:
        count = int(count_input)
    except ValueError:
        print("❌ Please enter a valid number.")
        return []

    for i in range(count):
        print(f"\n--- Vulnerability {i + 1} ---")

        name = required_input("🛡️ Name:")
        cwe_id = required_input("📚 CWE-ID (e.g., CWE-79):")
        description = required_input("📝 Description:")
        impact = required_input("💥 Impact:")
        remediation = required_input("🛠️ Remediation:")
        affected_url = required_input("🌐 Affected URL:")

        severity = questionary.select(
            "🚨 Severity:",
            choices=["Critical", "High", "Medium", "Low"]
        ).ask()
        if severity is None:
            print("\n🛑 Cancelled.")
            sys.exit(0)

        status = questionary.select(
            "📌 Status:",
            choices=["Open", "Fixed", "Validated"]
        ).ask()
        if status is None:
            print("\n🛑 Cancelled.")
            sys.exit(0)

        # Multi-screenshot support
        screenshot_paths = []
        while True:
            add_more = questionary.confirm("📎 Do you want to add a screenshot for this vulnerability?").ask()
            if add_more is None:
                print("\n🛑 Cancelled.")
                sys.exit(0)
            if not add_more:
                break
            path = questionary.path("📁 Select screenshot file:").ask()
            if path is None:
                print("\n🛑 Cancelled.")
                sys.exit(0)
            screenshot_paths.append(path.strip())

        vuln = {
            "name": name,
            "cwe_id": cwe_id,
            "description": description,
            "impact": impact,
            "remediation": remediation,
            "affected_url": affected_url,
            "severity": severity,
            "status": status,
            "screenshots": screenshot_paths
        }

        vulnerabilities.append(vuln)

    return vulnerabilities
