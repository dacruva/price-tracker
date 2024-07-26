from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Target
url = "https://www.amazon.com/Productivity-Qualcomm-Snapdragon-Included-Graphite/dp/B09XN5DF6Q/ref=sr_1_4?sr=8-4"
BUY_NOW_PRICE = 300

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

# Adding headers to the request
response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")

# Find the HTML element that contains the price
price = soup.find(class_="a-offscreen").get_text()

# Remove the dollar sign using split
float_price = float(price.split("$")[1])

print(float_price)

# Get the product title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Set the price below which you would like to get a notification


if float_price < BUY_NOW_PRICE:
    message = f"{title} is on sale for {price}!"

    # ====================== Sending the email ===========================

    with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), port=587) as connection:
        connection.starttls()
        result = connection.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL_ADDRESS"),
            to_addrs=os.getenv("EMAIL_ADDRESS"),
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )
