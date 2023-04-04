import os
import requests
from twilio.rest import Client
import schedule
import time
from datetime import datetime
from pytz import timezone

# Set up the Twilio client
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# Set up your phone numbers
from_number = "whatsapp:" + os.environ["FROM_PHONE_NUMBER"]
to_number = "whatsapp:" + os.environ["TO_PHONE_NUMBER"]

# Imgur API credentials
client_id = os.environ["IMGUR_CLIENT_ID"]
headers = {"Authorization": f"Client-ID {client_id}"}


def get_top_image_url():
    # Get the top images from Imgur in the last day
    response = requests.get(
        "https://api.imgur.com/3/gallery/t/funny/time/1",
        headers=headers,
    )
    items = response.json()["data"]["items"]

    # Find the first image post
    for item in items:
        if item["is_album"]:
            continue
        return item["link"]
    return None


def send_image(image_url):
    if image_url:
        # Send the image to the Whatsapp bot
        message = client.messages.create(
            media_url=image_url,
            from_=from_number,
            to=to_number,
        )
        print("Image sent!")
    else:
        print("Failed to fetch image.")


def job():
    top_image_url = get_top_image_url()
    send_image(top_image_url)
    print("Test")


def run_at_time(h, m, tz):
    local_timezone = timezone(tz)
    now = datetime.now(local_timezone)
    target_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)
    delay = (target_time - now).total_seconds()
    time.sleep(delay)
    job()


if __name__ == "__main__":
    schedule.every().day.at("10:30:00").do(run_at_time, 10, 30, "CET")
    while True:
        schedule.run_pending()
        time.sleep(1)
