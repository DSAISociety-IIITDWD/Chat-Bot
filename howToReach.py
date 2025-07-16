from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--window-size=1920,1080")

# ✅ Replace with your actual path
chrome_driver_path = r"C:\Users\kumar\OneDrive\Desktop\AllProjects\webScraping\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Open Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open IIITDWD How to Reach page
driver.get("https://iiitdwd.ac.in/how-to-reach/")
time.sleep(5)

listTransport = ['air', 'rail', 'road', 'car']
data = []
travelmode_id = 1
for i in listTransport:
    button = driver.find_element(By.ID, f'radix-«Rptrtqjb»-trigger-{i}')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, f"radix-«Rptrtqjb»-trigger-{i}")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    time.sleep(2)
    button.click()
    time.sleep(5)

    # Parse content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs_1 = soup.find_all('div', class_='text-title-3 font-normal')

    for div in divs_1:
        try:
            header = div.find('h3').text.strip()
            description = div.find('p').text.strip()
            data.append([travelmode_id, i, header, description])
            travelmode_id += 1
        except:
            continue  # Skip divs that don’t have both h3 and p

# Save to CSV
df = pd.DataFrame(data, columns=["travelmode_id", "Tab", "Mode", "Description"])
df.to_csv("how_to_reach_detailed.csv", index=False)

print("✅ Saved to how_to_reach_detailed.csv")

# Close the browser
driver.quit()
