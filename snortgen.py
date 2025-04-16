import os
import sys
import shutil
import questionary
from pyfiglet import Figlet
from colorama import init, Fore, Style

from style import custom_style
from vuln_input_handler import collect_vulnerabilities
from docx_report_generator import generate_docx_report
import csv

def parse_csv(csv_path):
    vulnerabilities = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vuln = {
                    "name": row['name'],
                    "cwe_id": row['cwe_id'],
                    "description": row['description'],
                    "impact": row['impact'],
                    "remediation": row['remediation'],
                    "affected_url": row['affected_url'],
                    "severity": row['severity'],
                    "status": row['status'],
                    "screenshots": row['screenshots'].split(';') if row.get('screenshots') else []
                }
                vulnerabilities.append(vuln)
        return vulnerabilities
    except Exception as e:
        print(f"❌ Failed to parse CSV: {e}")
        return []

init(autoreset=True)

def print_banner():
    f = Figlet(font='slant')
    banner = f.renderText("SnortGen")
    terminal_width = shutil.get_terminal_size().columns
    for line in banner.splitlines():
        print(Fore.CYAN + Style.BRIGHT + line.center(terminal_width))
    print(Fore.YELLOW + Style.BRIGHT + "by Parth Mishra".center(terminal_width) + "\n")

def prompt_template_path():
    while True:
        try:
            template_path = questionary.path("Enter path to the report template (.docx):", style=custom_style).ask()
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

    # ✅ Ask for input mode
    mode = questionary.select(
        "🔰 How do you want to proceed?",
        choices=[
            "Automated Method",
            "CSV Method"
        ],
        style=custom_style
    ).ask()

    if mode == "Automated Method":
        template_path = prompt_template_path()
        vulns = collect_vulnerabilities()
        if vulns:
            generate_docx_report(
                vulnerabilities=vulns,
                template_path=template_path,
                output_path="reports"
            )
    elif mode == "CSV Method":
        csv_path = questionary.path("📄 Enter path to CSV file:", style=custom_style).ask()
        if csv_path and os.path.isfile(csv_path):
            vulns = parse_csv(csv_path)
            if vulns:
                template_path = prompt_template_path()
                generate_docx_report(
                    vulnerabilities=vulns,
                    template_path=template_path,
                    output_path="reports"
                )
        else:
            print("❌ Invalid or missing CSV file path.")

if __name__ == "__main__":
    try:
        print_banner()
        main()
    except KeyboardInterrupt:
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
