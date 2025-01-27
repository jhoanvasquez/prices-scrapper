import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_olimpica_data(pages=1, output_file="olimpica_products.xlsx"):
    base_url = "https://www.olimpica.com/supermercado/despensa/granos?page={}"

    scraped_data = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        response = requests.get(base_url.format(page))
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        container = soup.select_one("#gallery-layout-container")

        if not container:
            print(f"No product container found on page {page}.")
            continue

        products = container.find_all('div', class_='vtex-search-result-3-x-galleryItem')

        for product in products:
            name_tag = product.find('span', class_='vtex-product-summary-2-x-productBrand')
            product_name = name_tag.text.strip() if name_tag else "N/A"

            price_tag = product.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
            total_price = price_tag.text.strip() if price_tag else "N/A"

            scraped_data.append({
                "Producto": product_name,
                "Precio": total_price,
                "Supermercado": "Olimpica"
            })

    df = pd.DataFrame(scraped_data)
    df.to_excel(output_file, index=False)
    print(f"Data successfully saved to {output_file}")

scrape_olimpica_data(pages=4)
