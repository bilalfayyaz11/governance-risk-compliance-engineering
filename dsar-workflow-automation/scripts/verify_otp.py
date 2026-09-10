import pyotp
import smtplib
from email.mime.text import MIMEText


def generate_otp(secret: str) -> str:
    """
    Generate a time-based OTP using the provided secret.

    Args:
        secret: Base32 secret key

    Returns:
        6-digit OTP string
    """
    return pyotp.TOTP(secret).now()


def send_otp_email(to_email: str, otp: str) -> None:
    """
    Send the OTP to the data subject via local SMTP.

    Args:
        to_email: Recipient email address
        otp: The OTP code to send
    """
    message = MIMEText(
        f"Your DSAR identity verification OTP is: {otp}\n"
        "This code is time-limited."
    )

    message["Subject"] = "DSAR Identity Verification"
    message["From"] = "privacy@example.local"
    message["To"] = to_email

    with smtplib.SMTP("localhost", 1025, timeout=10) as smtp:
        smtp.send_message(message)


def verify_otp(secret: str, user_input: str) -> bool:
    """
    Verify the OTP entered by the user against the secret.
    """
    return pyotp.TOTP(secret).verify(
        user_input.strip(),
        valid_window=1
    )


if __name__ == "__main__":
    secret = pyotp.random_base32()
    otp = generate_otp(secret)

    send_otp_email("subject@example.com", otp)

    print("OTP email sent successfully.")
    print(f"Generated OTP (testing only): {otp}")
    print(f"Secret (testing only): {secret}")
    print(f"Verification result: {verify_otp(secret, otp)}")
