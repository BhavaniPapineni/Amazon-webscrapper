import requests
from bs4 import BeautifulSoup
import csv, os
import random, time

# url for searching samsung in amazon.in
url = "https://www.amazon.in/s?k=iphone"

# using headers 
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

# request to website
response = requests.get(url, headers=headers)

# response checking 
print(response.status_code)

# print(response.content) # content in byte format

# parsing the content of webpage
soup = BeautifulSoup(response.content, "lxml")

# find all product containers
products = soup.find_all("div", {"data-component-type": "s-search-result"})

file_name = "products.csv"

# create file with header only if it doesn't exist
file_exists = os.path.exists(file_name)

if not file_exists:
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Product_Title", "Price"])

# read existing rows once
with open(file_name, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    existing_rows = {tuple(row) for row in reader}

# append new unique products
with open(file_name, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # iterating over each product container thats extracted
    for product in products:
        # N/A is a safecheck. When the element is missing program crashes to avoid that we use N/A
        title = product.h2.text.strip() if product.h2 else "N/A"
        # "a-price-whole" is Amazon's css class for storing price 
        price_tag = product.find("span", "a-price-whole")
        price = price_tag.text if price_tag else "N/A"

        # checking for duplicates
        if (title, price) not in existing_rows:
            writer.writerow([title, price])
            # preventing duplicates
            existing_rows.add((title, price))  

# printing no.of products that are extracted
print(len(products))

# adding human-like behaviour so Amazon does not block us from extracting data
time.sleep(random.uniform(2,5))