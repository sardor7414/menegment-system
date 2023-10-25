from django.core.mail import send_mail



def send_message_to_email(email, inviter_email, code, token):
    url = f"http://127.0.0.1:8000/verify?token={token}"
    email_title = "Siz yangi ish oynasiga qo'shiladingiz"
    email_body = f"Sizni {inviter_email} faydalanuvchi taklif qilmoqda" \
                 f"Tasdiqlash uchun ushbu havolaga o'ting {url}" \
                 f"va ushbu kodni kiriting: {code}"
    send_mail(
        email_title, email_body, inviter_email, [email]
    )