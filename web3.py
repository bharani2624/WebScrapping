from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import os

if not os.path.exists("downloaded_images"):
    os.makedirs("downloaded_images")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.sick.com/in/en/catalog/products/detection-sensors/photoelectric-sensors/w4/wtb4fp-22161120a00/p/p661408?tab=detail"
driver.get(url)

try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
    print("Page loaded successfully!")
except TimeoutException:
    print("Page took too long to load. Exiting.")
    driver.quit()

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

product_details = {}
tables = soup.find_all('table')

if tables:
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all(['th', 'td'])
            if len(columns) == 2:
                key = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                product_details[key] = value
    print("\nDetails:")
    for k, v in product_details.items():
        print(f"{k}: {v}")

images = soup.find_all('img')
for index, image in enumerate(images):
    image_url = image.get('src')
    if image_url:
        print(f"Found image URL: {image_url}")
        try:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_filename = f"downloaded_images/image_{index + 1}.jpg"
                with open(image_filename, "wb") as file:
                    file.write(image_response.content)
                print(f"Downloaded: {image_filename}")
            else:
                print(f"No Image: {image_url}")
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")

datasheet_url = "https://cdn.sick.com/media/pdf/8/08/408/dataSheet_WTB4FP-22161120A00_1222998_en.pdf"
print(f"Downloading datasheet from: {datasheet_url}")

try:
    datasheet_response = requests.get(datasheet_url)
    if datasheet_response.status_code == 200:
        with open("product_datasheet.pdf", "wb") as file:
            file.write(datasheet_response.content)
        print("Datasheet downloaded successfully!")
    else:
        print("Failed to download the datasheet.")
except Exception as e:
    print(f"Error downloading the datasheet: {e}")

driver.quit()
