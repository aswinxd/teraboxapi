from pyrogram import Client, filters
import requests
import os

# Your Telegram bot credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# RapidAPI credentials for Terabox
RAPIDAPI_KEY = "your_rapidapi_key"
RAPIDAPI_HOST = "terabox-downloader-direct-download-link-generator.p.rapidapi.com"

# Initialize the Pyrogram client
app = Client("terabox_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handle the /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Welcome! Send me a Terabox link, and I'll download the file for you.")

# Function to get download link from Terabox using RapidAPI
def get_terabox_download_link(url):
    api_url = "https://terabox-downloader-direct-download-link-generator.p.rapidapi.com/fetch"

    payload = {"url": url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("download")
    else:
        raise Exception(f"Failed to get download link: {response.status_code}, {response.text}")

# Function to download the file from the generated download link
def download_file(download_link, filename):
    response = requests.get(download_link, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return filename

# Handle messages with Terabox links
@app.on_message(filters.text)
def handle_link(client, message):
    link = message.text
    if "terabox" in link:  # Basic validation for Terabox links
        message.reply_text("Processing your Terabox link...")

        try:
            # Get the direct download link
            download_link = get_terabox_download_link(link)
            filename = "downloaded_file.ext"  # Adjust filename as needed

            # Download the file
            downloaded_file = download_file(download_link, filename)

            # Send the downloaded file back to the user
            message.reply_document(document=downloaded_file)

            # Clean up the downloaded file after sending
            os.remove(downloaded_file)
        except Exception as e:
            message.reply_text(f"Error: {e}")
    else:
        message.reply_text("Please send a valid Terabox link.")

# Run the bot
app.run()
