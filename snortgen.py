import os
import sys
import questionary
from vuln_input_handler import collect_vulnerabilities
from docx_report_generator import generate_docx_report

def prompt_template_path():
    while True:
        try:
            template_path = questionary.path("📄 Enter path to the report template (.docx):").ask()
            if template_path is None:
                print("\n🛑 Cancelled by user.")
                sys.exit(0)
            if not os.path.isfile(template_path):
                print(f"❌ File not found: {template_path}")
            else:
                return template_path
        except KeyboardInterrupt:
            print("\n🛑 Cancelled by user.")
            sys.exit(0)

def main():
    os.makedirs("reports", exist_ok=True)

    # 📄 Ask for a valid template path
    template_path = prompt_template_path()

    # 🛡️ Collect vulnerability data
    vulns = collect_vulnerabilities()

    # 📄 Generate the DOCX report
    if vulns:
        generate_docx_report(
            vulnerabilities=vulns,
            template_path=template_path,
            output_path="reports"
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
