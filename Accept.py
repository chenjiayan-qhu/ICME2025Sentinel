'''
Author       : JethronChen <JethronChen@163.com>
Date         : 2025-03-10 20:49:39 +0800
LastEditTime : 2025-03-13 18:02:22 +0800
Description  : 
'''
import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

# email config
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = ""
SENDER_PASSWORD = ""
RECEIVER_EMAIL = ""

# request headers
HEADERS = {
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# PAPER_IDS = [100,101,102]  # sample
PAPER_IDS = []  # paper ID
BASE_URL = "https://cmt3.research.microsoft.com/api/odata/ICME2025/Submissions({})"

LAST_STATUSES = {paper_id: None for paper_id in PAPER_IDS}  # last status of each paper
LAST_EMAIL_TIME = time.time()  # last email time
EMAIL_INTERVAL = 60 * 60  # send email every 60 minutes
QUERY_INTERVAL = 60 * 1  # query every 1 minute


def send_email(subject, content):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Mail sending failure: {e}")


def get_paper_status(paper_id):
    """
    get paper StatusOd by paper_id
    """
    url = BASE_URL.format(paper_id)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            res_info = response.json()
            status_id = res_info.get("StatusId", -1)
            status_dict = {
                1: "No Update",         # statusid = 1
                2: "🎉 Accepted",       # statusid = 2
                3: "Maybe Rejected"     # statusid = 3
            }
            status_text = status_dict.get(status_id, "Unknown")
            print(f"🐌 Paper {paper_id}, Status: {status_text}")
            return status_id, f"Paper {paper_id} Status: {status_text}"
        else:
            return None, f"⚠️ Paper {paper_id} request failed: {response.status_code}"
    except Exception as e:
        return None, f"❌ Paper {paper_id} request failure: {e}"


def check_paper_status():

    global LAST_EMAIL_TIME
    status_report = []
    important_updates = []

    for paper_id in PAPER_IDS:
        status_id, status_msg = get_paper_status(paper_id)
        status_report.append(status_msg)

        if status_id in [2, 3] and LAST_STATUSES[paper_id] != status_id:
            important_updates.append(f"📌 {status_msg}")
            LAST_STATUSES[paper_id] = status_id

    if important_updates:
        send_email("📢 Paper Status Update", "\n".join(important_updates))

    current_time = time.time()
    if current_time - LAST_EMAIL_TIME >= EMAIL_INTERVAL:
        send_email("⏳ Paper Status Report", "\n".join(status_report))
        LAST_EMAIL_TIME = current_time
    


if __name__ == "__main__":
    print("\n🔔 Program start, press Ctrl+C to stop.")
    try:
        while True:
            now = datetime.datetime.now()
            print("\n🕒 Current Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
            print("\n🔍 Checking the status of the paper...\n")
            check_paper_status()
            print(f"\n⏳ Next query in {int(QUERY_INTERVAL / 60)} minutes...")
            time.sleep(QUERY_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Program stopped by user.")