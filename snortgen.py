import os
import questionary
from vuln_input_handler import collect_vulnerabilities
from docx_report_generator import generate_docx_report

if __name__ == "__main__":
    try:
        os.makedirs("reports", exist_ok=True)

        # Prompt user for template path
        template_path = questionary.path("📄 Enter path to the report template (.docx):").ask()

        # Collect vulnerability data
        vulns = collect_vulnerabilities()

        # Generate the report
        if vulns:
            generate_docx_report(
                vulnerabilities=vulns,
                template_path=template_path,
                output_path="reports"
            )
    except KeyboardInterrupt:
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)")