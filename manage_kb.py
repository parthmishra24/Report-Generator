import json
import questionary
import os
import sys
from style import custom_style  # ✅ centralized style import

KB_PATH = 'vuln_knowledgebase.json'

def load_knowledgebase():
    if not os.path.exists(KB_PATH):
        print("⚠️ Knowledge base not found. Creating a new one.")
        return {}
    with open(KB_PATH, 'r') as f:
        return json.load(f)

def save_knowledgebase(kb):
    with open(KB_PATH, 'w') as f:
        json.dump(kb, f, indent=2)
    print("✅ Knowledge base saved.")

def required_input(prompt):
    while True:
        answer = questionary.text(prompt, style=custom_style).ask()
        if answer is None:
            print("\n🛑 Cancelled.")
            sys.exit(0)
        if answer.strip():
            return answer.strip()
        print("❗ This field is required.")

def view_entries(kb):
    if not kb:
        print("🚫 Knowledge base is empty.")
        return
    print("\n📚 Vulnerabilities in Knowledge Base:")
    for name in kb:
        print(f"- {name}")
    print("")

def add_new_entry(kb):
    print("\n➕ Add a New Vulnerability Entry\n")
    name = required_input("🛡️ Vulnerability name:")
    if name in kb:
        overwrite = questionary.confirm(f"⚠️ '{name}' already exists. Overwrite?", style=custom_style).ask()
        if not overwrite:
            print("❌ Entry not added.")
            return
    cwe_id = required_input("📚 CWE-ID (e.g., CWE-89):")
    description = required_input("📝 Description:")
    impact = required_input("💥 Impact:")
    remediation = required_input("🛠️ Remediation:")
    kb[name] = {
        "cwe_id": cwe_id,
        "description": description,
        "impact": impact,
        "remediation": remediation
    }
    save_knowledgebase(kb)

def edit_entry(kb):
    if not kb:
        print("🚫 Knowledge base is empty.")
        return
    name = questionary.autocomplete(
        "✏️ Select vulnerability to edit:",
        choices=list(kb.keys()),
        match_middle=True,
        ignore_case=True,
        style=custom_style
    ).ask()
    if name is None:
        print("🛑 Cancelled.")
        return
    entry = kb[name]
    print("\n🔧 Leave fields blank to keep current values.\n")
    new_name = questionary.text(f"Name [{name}]:", style=custom_style).ask() or name
    new_cwe = questionary.text(f"CWE-ID [{entry.get('cwe_id', '')}]:", style=custom_style).ask() or entry.get('cwe_id', '')
    new_desc = questionary.text(f"Description [{entry.get('description', '')[:30]}...]:", style=custom_style).ask() or entry.get('description', '')
    new_impact = questionary.text(f"Impact [{entry.get('impact', '')[:30]}...]:", style=custom_style).ask() or entry.get('impact', '')
    new_remediation = questionary.text(f"Remediation [{entry.get('remediation', '')[:30]}...]:", style=custom_style).ask() or entry.get('remediation', '')
    if new_name != name:
        del kb[name]
    kb[new_name] = {
        "cwe_id": new_cwe,
        "description": new_desc,
        "impact": new_impact,
        "remediation": new_remediation
    }
    save_knowledgebase(kb)

def delete_entry(kb):
    if not kb:
        print("🚫 Knowledge base is empty.")
        return
    name = questionary.autocomplete(
        "❌ Select vulnerability to delete:",
        choices=list(kb.keys()),
        match_middle=True,
        ignore_case=True,
        style=custom_style
    ).ask()
    if name is None:
        print("🛑 Cancelled.")
        return
    confirm = questionary.confirm(f"Are you sure you want to delete '{name}'?", style=custom_style).ask()
    if confirm:
        del kb[name]
        save_knowledgebase(kb)
    else:
        print("✅ Deletion cancelled.")

def search_entries(kb):
    if not kb:
        print("🚫 Knowledge base is empty.")
        return
    keyword = required_input("🔎 Enter keyword to search:")
    keyword_lower = keyword.lower()
    results = []
    for name, details in kb.items():
        if (
            keyword_lower in name.lower()
            or keyword_lower in details.get("cwe_id", "").lower()
            or keyword_lower in details.get("description", "").lower()
            or keyword_lower in details.get("impact", "").lower()
            or keyword_lower in details.get("remediation", "").lower()
        ):
            results.append((name, details))
    if not results:
        print(f"❌ No entries found for '{keyword}'.")
    else:
        print(f"\n🔍 Found {len(results)} result(s):\n")
        for name, entry in results:
            print(f"🛡️ {name}")
            print(f"  - CWE-ID: {entry.get('cwe_id')}")
            print(f"  - Description: {entry.get('description')[:80]}...")
            print(f"  - Impact: {entry.get('impact')[:80]}...")
            print(f"  - Remediation: {entry.get('remediation')[:80]}...\n")

def quick_search_name(kb):
    if not kb:
        print("🚫 Knowledge base is empty.")
        return
    name = questionary.autocomplete(
        "🔍 Select a vulnerability by name:",
        choices=list(kb.keys()),
        match_middle=True,
        ignore_case=True,
        style=custom_style
    ).ask()
    if name is None:
        print("\n🛑 Cancelled.")
        return
    entry = kb.get(name, {})
    print(f"\n🛡️ {name}")
    print(f"  - CWE-ID: {entry.get('cwe_id')}")
    print(f"  - Description: {entry.get('description')}")
    print(f"  - Impact: {entry.get('impact')}")
    print(f"  - Remediation: {entry.get('remediation')}\n")

def main():
    while True:
        kb = load_knowledgebase()
        action = questionary.select(
            "📚 What do you want to do?",
            choices=[
                "➕ Add a new entry",
                "🔍 Quick search by name",
                "🧠 Deep keyword search",
                "📖 View vulnerability entries",
                "✏️  Edit an entry",
                "❌ Delete an entry",
                "🚪 Exit"
            ],
            style=custom_style
        ).ask()

        if "Add a new entry" in action:
            add_new_entry(kb)
        elif "Quick search" in action:
            quick_search_name(kb)
        elif "Deep keyword search" in action:
            search_entries(kb)
        elif "View vulnerability entries" in action:
            view_entries(kb)
        elif "Edit an entry" in action:
            edit_entry(kb)
        elif "Delete an entry" in action:
            delete_entry(kb)
        elif "Exit" in action:
            print("👋 Exiting.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user.")
        sys.exit(0)
