import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import base64


# specify search query and number of images to download
searches_all = [
    "Bell's palsy people face images",
    "Butterfly Rash on face images",
    "dehydration cracked libs face images",
    "Drooping Eyelid ptosis face images",
    "jaundice Yellowish Skin and Eyes",
    "moles in face",
    "polycystic ovary syndrome hair in unusual places for woman face images",
    "Sores in face images",
    "xanthelasma Yellow Spots on Your Eyelids",
    "Puffy Eyes face images",
    "Melasma on face images",
    "alopecia hair loss face images",
    "face images",
    "people face images",
]

searches = [
    searches_all[13]
]

num_images = 50


for search in searches:
    search_query = search
    folder_name = search_query.replace(" ", "_")
    import os

    # create images directory if it doesn't exist
    if not os.path.exists(f'./images/{folder_name}'):
        os.makedirs(f'./images/{folder_name}')


    # configure Chrome options to download images to specified directory
    options = Options()
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": os.path.abspath("./images"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    # create a new Chrome web driver with options
    driver = webdriver.Chrome(options=options)

    # navigate to the Google Images search page
    driver.get("https://www.google.com/imghp")

    # wait for the search box element to become visible
    wait = WebDriverWait(driver, 10)
    box = driver.find_element(By.XPATH, '//input[@name="q"]')

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)

    # wait for the search results to load
    time.sleep(5)

    # scroll down to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(driver.find_elements(By.XPATH, '//img[@class="rg_i"]')) < num_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # find all the image elements and download the specified number of images
    image_elements = driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')
    print(f"Found {len(image_elements)} images")
    num_downloaded = 0
    for img in image_elements:
        if num_downloaded >= num_images:
            break
        
        try:
            url = img.get_attribute("src")
            print("image ", url)
            with open(f"./images/{folder_name}/{search_query}_{num_downloaded}.jpg", "wb") as out_file:
                try:
                    data = url.split(",")[1]
                    binary_data = base64.b64decode(data)
                except Exception as e:
                    response = requests.get(url, stream=True)
                    binary_data = response.content
                out_file.write(binary_data)

            num_downloaded += 1
        except Exception as e:
            print(e)


    # quit the web driver
    driver.quit()
