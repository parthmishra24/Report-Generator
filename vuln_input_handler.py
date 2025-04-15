import questionary
import json
import os
import sys

# Load local vuln knowledge base
def load_knowledgebase(path='vuln_knowledgebase.json'):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Failed to load knowledgebase: {e}")
        return {}

def save_knowledgebase(kb, path='vuln_knowledgebase.json'):
    try:
        with open(path, 'w') as file:
            json.dump(kb, file, indent=2)
        print("✅ Knowledge base updated.")
    except Exception as e:
        print(f"❌ Failed to save knowledge base: {e}")

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
    knowledgebase = load_knowledgebase()
    vuln_names = list(knowledgebase.keys()) + ["Other (Manual Entry)"]

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

        name = questionary.autocomplete(
            "🛡️ Enter or choose Vulnerability Name:",
            choices=vuln_names,
            match_middle=True,
            ignore_case=True
        ).ask()

        if name is None:
            print("\n🛑 Cancelled.")
            sys.exit(0)

        if name == "Other (Manual Entry)":
            name = required_input("✏️ Enter custom vulnerability name:")
            description = required_input("📝 Description:")
            impact = required_input("💥 Impact:")
            remediation = required_input("🛠️ Remediation:")
            cwe_id = required_input("📚 CWE-ID (e.g., CWE-79):")

            # 💾 Ask to save to knowledge base
            save_vuln = questionary.confirm("💾 Save this vulnerability to knowledge base for future use?").ask()
            if save_vuln:
                knowledgebase[name] = {
                    "cwe_id": cwe_id,
                    "description": description,
                    "impact": impact,
                    "remediation": remediation
                }
                save_knowledgebase(knowledgebase)

        else:
            auto = knowledgebase.get(name, {})
            description = auto.get("description") or required_input("📝 Description:")
            impact = auto.get("impact") or required_input("💥 Impact:")
            remediation = auto.get("remediation") or required_input("🛠️ Remediation:")
            cwe_id = auto.get("cwe_id") or required_input("📚 CWE-ID (e.g., CWE-79):")

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
