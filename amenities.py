from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

URL = "https://iiitdwd.ac.in/amenities/"
headers = {
    "User-Agent": "Mozilla/5.0 (IIITDWD Bot; scraping for educational/demo purposes; contact: youremail@example.com)"
}

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--window-size=1920,1080")

chrome_driver_path = r"C:\Users\kumar\OneDrive\Desktop\AllProjects\webScraping\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service,options=chrome_options)


driver.get("https://iiitdwd.ac.in/amenities/")

time.sleep(5)
listAmenities=['academic','residential','dining','other']
all_data = []
infra_id = 1

for i in listAmenities:
    button = driver.find_element(By.CSS_SELECTOR, f'[id^="radix-"][id$="trigger-{i}"]')
    wait = WebDriverWait(driver, 2)
    button_wait = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'[id^="radix-"][id$="trigger-{i}"]')))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    time.sleep(2)
    button.click()
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs_main = soup.find_all('div', class_='flex-1 outline-none space-y-4')

    for div_main in divs_main:
        divs = div_main.find_all('div', class_='bg-white text-card-foreground flex flex-col gap-6 rounded-xl border py-6 shadow-sm')

        for div in divs:
            card_header_tag = div.find('div', class_='@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 has-[data-slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6')
            card_title = card_header_tag.find('div', class_='leading-none !text-title-1 font-semibold text-main flex items-center gap-2')
            card_description = card_header_tag.find('div', class_='text-muted-foreground !text-title-3 font-normal')

            card_content_para = div.find('div', class_='px-6 space-y-6 text-title-3 font-medium')
            description = card_content_para.p.text.strip() if card_content_para and card_content_para.p else np.nan

            card_content = card_content_para.find_all('div', class_='bg-background p-4 rounded-lg') if card_content_para else []

            facilities_list = []
            location = np.nan

            for content in card_content:
                header = content.find('h3', class_='font-semibold text-title-2 text-main mb-4')
                header_text = header.text.strip() if header else ''

                if "location" in header_text.lower():
                    location = content.text.replace(header_text, "").strip()
                else:
                    ul_tag = content.find('ul')
                    if ul_tag:
                        li_tags = ul_tag.find_all('li')
                        for li in li_tags:
                            facilities_list.append(li.text.strip())

            facilities = ", ".join(facilities_list) if facilities_list else np.nan
            image_div = div.find('img')
            image_url = image_div['src'] if image_div and image_div.has_attr('src') else np.nan
            name = card_title.text.strip() if card_title else np.nan
            infra_type = card_description.text.strip() if card_description else np.nan

            all_data.append([
                infra_id,
                i,
                name,
                infra_type,
                description,
                location,
                facilities,
                image_url
            ])
            infra_id += 1

columns = ['amenity_id','amenity_type', 'name', 'type', 'description', 'location', 'facilities', 'image_url']
df = pd.DataFrame(all_data, columns=columns)
df.to_csv("amenity.csv", index=False)
print("Saved to amenity.csv")

