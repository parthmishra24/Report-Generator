# 🛡️ VAPT Report Generator & Vulnerability Knowledge Base (CLI Suite)
![Alt text](https://github.com/parthmishra24/Report-Generator/blob/main/snortgen.png?raw=true)
A professional CLI-based toolkit to streamline your **Vulnerability Assessment & Penetration Testing (VAPT)** workflow.  
This tool helps you **document findings**, **generate clean DOCX reports**, and **manage your own AI-powered knowledge base** — all through a powerful Python terminal interface.

---

## ✨ Features

### 📄 VAPT Report Generator
- Generate professional DOCX reports using your own template
- Input vulnerabilities one-by-one (bulk-friendly)
- Auto-fill Description, Impact & Remediation from a local JSON knowledge base
- Attach multiple screenshots per vulnerability
- Export reports to `/reports/` directory
- Fully CLI-driven

### 🧠 Vulnerability Knowledge Base Manager
- Add, view, edit, or delete vulnerabilities in a JSON format
- Quick search by name (with autocomplete)
- Deep keyword search (across all fields)
- Save new vulns from `snortgen.py` or manage via `manage_kb.py`

### 📄 CSV Method
SnortGen supports automated vulnerability reporting using a CSV file for bulk import.
A pre-built template is already included in the root directory:
```
📁 snortgen_template.csv
```

#### ✏️ How to Use:
1. Open snortgen_template.csv in any spreadsheet editor (Excel, Google Sheets, etc.).
2. Fill in the required vulnerability details as per the headers: name, cwe_id, description, impact, remediation, affected_url, severity, status, and screenshots
3. For multiple screenshots, separate file paths using a semicolon ```;```.
4. Save the file and run the tool: ```python3 snortgen.py```.
5. Enter the full path to your .csv file when asked.
---

## ⚙️ Prerequisites

Python 3.7+

## ⬇️ Installation

Required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. 📄 Generate a VAPT Report
```
python3 snortgen.py
```
What it does:
- Prompts for the path to your DOCX template
- Asks for the number of vulnerabilities
- Supports auto-filling from a local knowledge base
- Supports bulk screenshots per vuln
- Saves final report in /reports with a custom filename

---

2. 🧠 Manage the Knowledge Base
```
python3 manage_kb.py
```
CLI Options:
- ➕ Add a new entry
- 🔍 Quick search by name (autocomplete)
- 🧠 Deep keyword search (across all fields)
- 📖 View all entries
- ✏️ Edit an existing vulnerability
- ❌ Delete a vulnerability
- 🚪 Exit

---

💡 Smart Autofill Features

During report generation:
- You select a vulnerability from an autocomplete list
- If the entry exists in JSON → description, impact, remediation, and CWE-ID auto-fill
- Otherwise, you enter manually and can choose to save it

---

📦 Output
- Report is generated in .docx format using your template
Includes:
- Vulnerability summary table
- Detailed findings with screenshots
- Saved inside /reports/ folder

---

👨‍💻 Author

Parth Mishra | 
Security Engineer | Red Team Enthusiast
