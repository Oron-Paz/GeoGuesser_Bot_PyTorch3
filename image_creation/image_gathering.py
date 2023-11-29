import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

continents = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Australia', 'South America']

def main():
    for continent in continents:
        folder_name = continent + '_images'

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        download_images(continent, 300, folder_name)

def download_images(data, num_images, folder_name):
    print(f'Searching Images for {data}....')

    search_url = Google_Image + 'q=' + data + " streetview"
    
    # Use Selenium to open a browser and simulate scrolling
    driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in your PATH
    driver.get(search_url)

    # Perform the initial scroll manually
    driver.find_element("css selector", "body").send_keys(Keys.END)
    time.sleep(2)

    for _ in range(12):  # Adjust the number of scrolls as needed
        driver.find_element("css selector", "body").send_keys(Keys.END)
        time.sleep(2)  # Adjust sleep time as needed

        try:
            show_more_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'LZ4I')))
            show_more_button.click()
        except:
            pass  # Continue scrolling if the button is not yet visible or clickable

    html = driver.page_source
    driver.quit()

    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
    
    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count += 1
            if count >= num_images:
                break
        except KeyError:
            continue
    
    print(f'Found {len(imagelinks)} images for {data}')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

        try:
            # Use PIL to open the image and extract the format
            img = Image.open(BytesIO(response.content))
            file_extension = img.format.lower()
        except Exception as e:
            print(f"Error determining image format: {e}")
            file_extension = 'jpg'

        imagename = os.path.join(folder_name, f'{data}_{i+1}.{file_extension}')
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print(f'Download Completed for {data}!')

if __name__ == '__main__':
    main()
