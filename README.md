🔍 OSINT Exposure Report Generator

A cybersecurity project that analyzes publicly available information to assess personal exposure risk using OSINT (Open Source Intelligence) techniques.

---

🚀 Overview

This tool simulates the **reconnaissance phase of a cyber attack**, where publicly available data is collected to understand a target’s digital footprint.

The system gathers data from multiple sources and generates a **risk-based PDF report** with security recommendations.

---

🛠️ Features

* 🔎 Breach detection using public APIs
* 🌐 Username reconnaissance across multiple platforms using Sherlock
* 📧 Email reputation analysis
* 📊 Risk scoring system (Low / Medium / High / Critical)
* 📄 Automated PDF report generation

---

🧰 Tech Stack

* Python
* Requests (API integration)
* Sherlock (OSINT username tool)
* FPDF (PDF generation)

---

⚙️ How It Works

1. User inputs email and username
2. Tool checks:

   * Data breach exposure
   * Username presence across platforms
   * Email reputation risk
3. Calculates a risk score based on findings
4. Generates a structured PDF report

---

▶️ How to Run

```bash
pip install requests fpdf
python main.py
```

---

📊 Sample Output

The tool generates a PDF report containing:

* Breach history
* Social media footprint
* Email reputation analysis
* Risk score
* Security recommendations

---

📸 Screenshots

Terminal Execution

![Run 1](terminal-output-1.png)
![Run 2](terminal-output-2.png)

Sample PDF Report

![Report](report.png)

---

🧠 Key Learning

* Understanding OSINT techniques used in cybersecurity
* Practical implementation of reconnaissance methods
* API integration and automation using Python
* Risk analysis and report generation

---

⚠️ Disclaimer

This project is developed strictly for **educational and ethical purposes only**.
No unauthorized access or illegal data collection is performed.

---

📌 Future Improvements

* Web interface using Flask
* Integration with more OSINT APIs
* Advanced risk scoring algorithms
* Dashboard visualization

---
