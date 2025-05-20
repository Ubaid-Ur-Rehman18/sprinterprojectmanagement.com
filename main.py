from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit-form/")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    sender_email = "ubaid.rehman.ai@gmail.com"
    app_password = "uiacvptifgskrute"  # App password from Gmail
    receiver_email = "ubaid.rehman.ai@gmail.com"  # 👈 FIXED email to receive messages

    # Construct email
    subject = f"New Contact Message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        return JSONResponse(content={"success": True, "message": "Email sent"})
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"success": False, "message": "Failed to send email"})
