import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
# Function to scrape product details
def scrape_product_details(product_url):
    # Send an HTTP GET request to the product URL
    response = requests.get(product_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product title
        product_title = soup.find('span', {'class': 'B_NuCI'}).text.strip()

        # Extract product price
        product_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()

        # Extract product ratings
        product_ratings = soup.find('div', {'class': '_3LWZlK'}).text.strip()

        # Extract product reviews
        product_reviews = []
        review_elements = soup.find_all('div', {'class': 'col _2wzgFH'})
        for review_element in review_elements:
            review_text = review_element.find('div', {'class': 't-ZTKy'}).text.strip()
            product_reviews.append(review_text)

        # Create a dictionary to store the product details
        product_details = {
            'Title': product_title,
            'Price': product_price,
            'Ratings': product_ratings,
            'Reviews': product_reviews
        }
        return product_details
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

# Function to scrape multiple product URLs
def scrape_multiple_products(product_urls):
    all_product_details = []
    for url in product_urls:
        product_info = scrape_product_details(url)
        if product_info:
            all_product_details.append(product_info)
    return all_product_details

# List of Flipkart product URLs you want to scrape
product_urls = [
    'https://www.flipkart.com/asus-vivobook-15-core-i3-11th-gen-1115g4-8-gb-512-gb-ssd-windows-11-home-x515ea-ej322ws-x515ea-ej328ws-thin-light-laptop/p/itmaafbc240a8774?pid=COMGA5TUCZAV4HGH&lid=LSTCOMGA5TUCZAV4HGHWM8PS0&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&spotlightTagId=BestsellerId_6bo%2Fb5g&srno=s_1_3&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&fm=search-autosuggest&iid=471fb073-63b5-4780-a552-9ddaedcd6622.COMGA5TUCZAV4HGH.SEARCH&ppt=sp&ppn=sp&qH=312f91285e048e09',
    'https://www.flipkart.com/hp-15s-2023-intel-core-i5-11th-gen-1155g7-16-gb-512-gb-ssd-windows-11-home-15s-fr4001tu-thin-light-laptop/p/itm2420d6e75acdb?pid=COMGZNSB6GCJVUPX&lid=LSTCOMGZNSB6GCJVUPXOWTDNN&marketplace=FLIPKART&q=laptop+hp&store=6bo%2Fb5g&spotlightTagId=FkPickId_6bo%2Fb5g&srno=s_1_3&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_ps&fm=search-autosuggest&iid=03656ba8-ac23-484b-bd2a-38bc8dbfbeb1.COMGZNSB6GCJVUPX.SEARCH&ppt=sp&ppn=sp&qH=afa4496eec6c609d',
    'https://www.flipkart.com/hp-omen-core-i5-13th-gen-13420h-16-gb-512-gb-ssd-windows-11-home-6-graphics-nvidia-geforce-rtx-4050-16-wd0880tx-gaming-laptop/p/itm8b6455a0e5a67?pid=COMGRFA3FSYTP4FE&lid=LSTCOMGRFA3FSYTP4FEPMNJN3&marketplace=FLIPKART&q=hp+gaming+laptop&store=6bo%2Fb5g&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&fm=Search&iid=en_T38tPq-1J70vdsP7EM_RdHvSBqU_7w3t3ggJ7dI4ho0-y1wRybM390gVhvneMV4KacepUjIu6zQrGsHFH58EpA%3D%3D&ppt=sp&ppn=sp&ssid=gdmgjjdks00000001694115744020&qH=ea0dc41f5c63c439'
    # Add more product URLs as needed
]

# Call the function to scrape multiple product details
all_product_info = scrape_multiple_products(product_urls)
csv_file_name = 'flipkart_products.csv'

# Write the product details to a CSV file
with open(csv_file_name, mode='w', newline='',encoding="UTF-8") as csv_file:
    fieldnames = ['Title', 'Price', 'Ratings', 'Reviews']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write product details for each product
    for product_info in all_product_info:
        writer.writerow(product_info)

print(f"Data has been saved to {csv_file_name}.")
# Display product details for each product
for i, product_info in enumerate(all_product_info, start=1):
    print(f"Product {i} Details:")
    print(f"Title: {product_info['Title']}")
    print(f"Price: {product_info['Price']}")
    print(f"Ratings: {product_info['Ratings']}")
    print("Reviews:")
    for j, review in enumerate(product_info['Reviews'], start=1):
        print(f"Review {j}: {review}")
    print("\n")
