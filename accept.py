'''
Author       : JethronChen <JethronChen@163.com>
Date         : 2025-03-10 20:49:39 +0800
LastEditTime : 2025-03-10 21:54:55 +0800
Description  : 
'''

import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮箱配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "jethronchen@163.com"    # 发送邮箱的账号
SENDER_PASSWORD = ""                    # 邮箱申请到的密码
RECEIVER_EMAIL = ""                     # 接收通知的邮箱账号

# 论文查询配置
HEADERS = {
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# PAPER_IDS = [101,102,...]  # 论文 ID 列表
PAPER_IDS = []
BASE_URL = "https://cmt3.research.microsoft.com/api/odata/ICME2025/Submissions({})"


def send_email(subject, content):
    """
    发送邮件通知
    :param subject: 邮件主题
    :param content: 邮件正文
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


def get_paper_status(paper_id):
    """
    查询单篇论文状态
    :param paper_id: 论文 ID
    :return: 论文状态描述
    """
    url = BASE_URL.format(paper_id)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            res_info = response.json()
            status_id = res_info.get("StatusId", -1)

            status_dict = {
                1: "待决定",
                2: "🎉 ACCEPT! ",
                3: "已拒绝"
            }
            status_text = status_dict.get(status_id, "未知状态")

            return status_id, f"Paper {paper_id} Status: {status_text}"
        else:
            return None, f"⚠️ 论文 {paper_id} 请求失败，状态码: {response.status_code}"
    except Exception as e:
        return None, f"❌ 论文 {paper_id} 请求出错: {e}"


def check_paper_status():
    """
    检查所有论文状态并发送邮件通知
    """
    status_report = []
    accepted_papers = []

    for paper_id in PAPER_IDS:
        status_id, status_msg = get_paper_status(paper_id)
        status_report.append(status_msg)

        if status_id == 2:  # 如果论文被接收
            accepted_papers.append(paper_id)

    email_content = "\n".join(status_report)
    subject = "ℹ️ 论文状态更新通知"

    if accepted_papers:
        print("🎉 有论文被接受！")
        subject = "🎉 论文接收通知！"
        email_content = "以下论文已被接收:\n" + "\n".join(map(str, accepted_papers)) + "\n\n" + email_content

    send_email(subject, email_content)


def main():
    """
    主程序：定时查询论文状态
    """
    try:
        while True:
            print("\n🔍 正在查询论文状态...")
            check_paper_status()
            print("⏳ 查询完成，等待 15 分钟后再次查询。\n")
            time.sleep(60 * 15)  # 每 15 分钟查询一次
    except KeyboardInterrupt:
        print("\n🛑 程序已手动停止。")


if __name__ == "__main__":
    main()