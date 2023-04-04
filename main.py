import os
import requests
from twilio.rest import Client

# Set up the Twilio client
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# Set up your phone numbers
from_number = "whatsapp:" + os.environ["FROM_PHONE_NUMBER"]
to_number = "whatsapp:" + os.environ["TO_PHONE_NUMBER"]

def send_random_image():
  # Set up the URL to fetch a random image
  endpoint = "https://source.unsplash.com/random"

  # Fetch a random image
  response = requests.get(endpoint)

  # Verify that the content type is supported (JPEG, PNG, or GIF)
  if response.headers['Content-Type'] in ["image/jpeg", "image/png", "image/gif"]:
    # Send the image to the Whatsapp bot
    if response.status_code == 200:
      message = client.messages.create(media_url=response.url, from_=from_number, to=to_number)
      print("Image sent!")
    else:
      print("Failed to fetch image.")
  else:
    print(f"Unsupported image format: {response.headers['Content-Type']}")

send_random_image()