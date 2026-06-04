import requests
import subprocess
import os
from fpdf import FPDF
from datetime import datetime

# -------------------------------
# Phase 1: Breach Check (FREE API)
# -------------------------------
def check_breaches(email):
    print("\n🔍 Phase 1: Checking breach history (FREE API)...")

    url = f"https://api.xposedornot.com/v1/check-email/{email}"

    try:
        response = requests.get(url)
        data = response.json()

        if "Error" in data:
            print("  No breaches found")
            return []

        elif data.get("status") == "found":
            count = data.get("breaches", 0)
            print(f"  Found in {count} breach(es)")

            breaches = []
            for b in data.get("exposed_breaches", []):
                breaches.append({
                    "Name": str(b),
                    "BreachDate": "Unknown",
                    "DataClasses": ["Email"]
                })

            return breaches

        else:
            print("  No breaches found")
            return []

    except Exception as e:
        print(f"  Error: {e}")
        return []


# -------------------------------
# Phase 2: Username OSINT
# -------------------------------
def check_username(username):
    print("\n🔍 Phase 2: Scanning username across platforms...")

    output_file = f"{username}_results.txt"

    try:
        subprocess.run(
            ["sherlock", username, "--output", output_file],
            timeout=120
        )

        found = []

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            found = [l.strip().replace("[+] ", "") for l in lines if l.startswith("[+]")]

            print(f"  Found on {len(found)} platforms")

        return found

    except Exception as e:
        print(f"  Error: {e}")
        return []


# -------------------------------
# Phase 3: Email Reputation
# -------------------------------
def check_email_reputation(email):
    print("\n🔍 Phase 3: Checking email reputation...")

    url = f"https://emailrep.io/{email}"
    headers = {"User-Agent": "OSINT-Tool"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"  Risk Level: {data.get('risk', 'unknown').upper()}")
            return data

        elif response.status_code == 429:
            print("  Rate limited - try later")
            return {}

        else:
            print(f"  Error: {response.status_code}")
            return {}

    except Exception as e:
        print(f"  Error: {e}")
        return {}


# -------------------------------
# Risk Calculation (NO EMOJIS)
# -------------------------------
def calculate_risk(breaches, platforms_found, email_rep):
    score = 0

    score += len(breaches) * 20
    score += len(platforms_found) * 2

    if email_rep.get("suspicious"):
        score += 30

    risk = email_rep.get("risk", "none")

    if risk == "high":
        score += 30
    elif risk == "medium":
        score += 15

    score = min(score, 100)

    if score >= 70:
        return score, "CRITICAL"
    elif score >= 40:
        return score, "HIGH"
    elif score >= 20:
        return score, "MEDIUM"
    else:
        return score, "LOW"


# -------------------------------
# PDF Report (SAFE TEXT)
# -------------------------------
def safe_text(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1')


def generate_pdf(email, username, breaches, platforms, email_rep, risk_score, risk_label):
    print("\nGenerating PDF report...")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("OSINT EXPOSURE REPORT"), ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, safe_text(f"Email: {email}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Username: {username}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)

    pdf.ln(5)

    pdf.cell(0, 10, safe_text(f"Risk Score: {risk_score}/100 - {risk_label}"), ln=True)

    pdf.ln(5)

    # Breaches
    pdf.cell(0, 10, safe_text("Breaches:"), ln=True)
    if breaches:
        for b in breaches:
            pdf.cell(0, 8, safe_text(f"- {b['Name']} ({b['BreachDate']})"), ln=True)
    else:
        pdf.cell(0, 8, safe_text("No breaches found"), ln=True)

    pdf.ln(5)

    # Platforms
    pdf.cell(0, 10, safe_text("Platforms Found:"), ln=True)
    for p in platforms[:10]:
        pdf.cell(0, 8, safe_text(f"- {p}"), ln=True)

    pdf.ln(5)

    # Email reputation
    pdf.cell(0, 10, safe_text("Email Reputation:"), ln=True)
    pdf.multi_cell(0, 8, safe_text(str(email_rep)))

    filename = f"OSINT_Report_{email.replace('@','_').replace('.','_')}.pdf"
    pdf.output(filename)

    print(f"Report saved as: {filename}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    print("=" * 50)
    print(" OSINT EXPOSURE REPORT GENERATOR")
    print("=" * 50)

    email = input("\nEnter target email: ").strip()
    username = input("Enter target username: ").strip()

    breaches = check_breaches(email)
    platforms = check_username(username)
    email_rep = check_email_reputation(email)

    risk_score, risk_label = calculate_risk(breaches, platforms, email_rep)

    print(f"\nRisk Score: {risk_score}/100 - {risk_label}")

    generate_pdf(email, username, breaches, platforms, email_rep, risk_score, risk_label)

    print("\nScan Complete!")