import os
import sys
import shutil
import questionary
from pyfiglet import Figlet
from colorama import init, Fore, Style

from colorama import Fore, Style

def color_status(status):
    status = status.lower()
    if status == 'open':
        return Fore.RED + status.capitalize() + Style.RESET_ALL
    elif status == 'fixed':
        return Fore.GREEN + status.capitalize() + Style.RESET_ALL
    elif status == 'validated':
        return Fore.CYAN + status.capitalize() + Style.RESET_ALL
    return status


def color_severity(severity):
    severity = severity.lower()
    if severity == 'critical':
        return Fore.LIGHTBLACK_EX + severity.capitalize() + Style.RESET_ALL
    elif severity == 'high':
        return Fore.RED + severity.capitalize() + Style.RESET_ALL
    elif severity == 'medium':
        return Fore.YELLOW + severity.capitalize() + Style.RESET_ALL
    elif severity == 'low':
        return Fore.GREEN + severity.capitalize() + Style.RESET_ALL
    return severity

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
    terminal_width = shutil.get_terminal_size().columns
    f = Figlet(font='slant')
    banner = f.renderText("SnortGen")
    
    # Print banner centered with color
    for line in banner.splitlines():
        print(Fore.CYAN + Style.BRIGHT + line.center(terminal_width))
    
    print(Fore.YELLOW + Style.BRIGHT + "by Parth Mishra".center(terminal_width))
    print(Fore.MAGENTA + "🔐 CLI VAPT Report Generator".center(terminal_width))
    print(Fore.WHITE + "────────────────────────────────────────────────────────".center(terminal_width))

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
            print("╭────┬──────────────────────────────┬──────────────┬────────────╮")
            print("│ No │ Vulnerability                │ Severity     │ Status     │")
            print("├────┼──────────────────────────────┼──────────────┼────────────┤")
            for i, v in enumerate(vulns, 1):
                name = v['name'][:28].ljust(28)
                sev_text = v['severity'].capitalize().ljust(12)
                stat_text = v['status'].capitalize().ljust(10)
    
                colored_severity = color_severity(sev_text)
                colored_status = color_status(stat_text)
    
                print(f"│ {str(i).rjust(2)} │ {name} │ {colored_severity} │ {colored_status} │")
                print("╰────┴──────────────────────────────┴──────────────┴────────────╯")

                
                
                
            confirm = questionary.confirm("📝 Proceed to generate the report?", style=custom_style).ask()
            if not confirm:
                print("❌ Report generation cancelled.")
                sys.exit(0)

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
