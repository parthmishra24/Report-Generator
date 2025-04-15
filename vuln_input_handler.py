import questionary

def required_input(message):
    while True:
        answer = questionary.text(message).ask()
        if answer and answer.strip():
            return answer.strip()
        print("❗ This field is required. Please enter a valid value.\n")

def collect_vulnerabilities():
    vulnerabilities = []

    try:
        count = int(required_input("🔐 Enter number of vulnerabilities to report:"))
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

        status = questionary.select(
            "📌 Status:",
            choices=["Open", "Fixed", "Validated"]
        ).ask()

        # 🖼️ Collect multiple screenshot paths
        screenshot_paths = []
        while True:
            add_more = questionary.confirm("📎 Do you want to add a screenshot for this vulnerability?").ask()
            if not add_more:
                break
            path = questionary.path("📁 Select screenshot file:").ask()
            if path:
                screenshot_paths.append(path.strip())
            else:
                print("❗ Screenshot path cannot be empty.")

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