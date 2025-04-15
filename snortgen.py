import os
import sys
import questionary
from pyfiglet import Figlet
from vuln_input_handler import collect_vulnerabilities
from docx_report_generator import generate_docx_report

def print_banner():
    f = Figlet(font='slant')
    print(f.renderText("SnortGen"))
    print("by Parth\n")

def main():
    print_banner()
    os.makedirs("reports", exist_ok=True)

    template_path = questionary.path("📄 Enter path to the report template (.docx):").ask()
    if template_path is None:
        print("\n🛑 Operation cancelled.")
        sys.exit(0)

    vulns = collect_vulnerabilities()

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
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)\n")
        sys.exit(0)
