import os
import sys
import shutil
import questionary
from pyfiglet import Figlet
from colorama import init, Fore, Style

from style import custom_style
from vuln_input_handler import collect_vulnerabilities
from docx_report_generator import generate_docx_report

init(autoreset=True)  # ✅ Initialize colorama

def print_banner():
    f = Figlet(font='slant')
    banner = f.renderText("SnortGen")
    terminal_width = shutil.get_terminal_size().columns

    # Print centered and colored banner
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
    template_path = prompt_template_path()
    vulns = collect_vulnerabilities()
    if vulns:
        generate_docx_report(vulnerabilities=vulns, template_path=template_path, output_path="reports")

if __name__ == "__main__":
    try:
        print_banner()  # ✅ Show banner first
        main()
    except KeyboardInterrupt:
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
