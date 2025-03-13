# ICME2025Sentinel
This program is designed to monitor the latest acceptance status of ICME 2025 papers. Enter your cookie and paper ID, and the program will automatically check the latest status for you and send the results to your email.

### 🛠️ Usage
1. Configure the email SMTP information and fill in the missing variable values.
2. Log in to the **CMT**, retrieve your Cookie, and insert it into the **HEADERS** variable.
3. Enter the **PaperIDs** you want to monitor. You can only retrieve the status of papers you authored or reviewed.
4. run Accept.py

### 🔮 Introduction
After you fill in the email configuration, the script will automatically check the status of the paper, each query interval is the value of the variable **QUERY_INTERVAL**. If the status of the paper changes, the system will automatically send an email to **RECEIVER_EMAIL**. Also, to prevent you from worrying about not receiving messages for a long time 😭, set the value of the **EMAIL_INTERVAL** variable to ensure that you receive a recent status email at regular intervals.

🍀 Good Lucky! Accept! 🍀

