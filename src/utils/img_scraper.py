import io
import os
import time
import requests
from PIL import Image
from selenium import webdriver
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

def fetch_image_urls(
    query: str,
    max_links_to_fetch: int,
    wd: webdriver,
    sleep_between_interactions: int = 0.01,
):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))

    button = wd.find_element(By.CSS_SELECTOR, ".Nc7WLe")
    button.click()

    image_urls = set()
    results_start = 0

    while True:
        scroll_to_end(wd)

        thumbnail_results: List[WebElement] = wd.find_elements(
            By.CSS_SELECTOR, "img.Q4LuWd"
        )

        number_results = len(thumbnail_results)

        print(
            f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}"
        )

        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            actual_images: List[WebElement] = wd.find_elements(
                By.CSS_SELECTOR, "img.n3VNCb"
            )

            for actual_image in actual_images:
                if actual_image.get_attribute(
                    "src"
                ) and "http" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute("src"))

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                return image_urls
        else:
            load_more_button: WebElement = wd.find_elements(By.CSS_SELECTOR, ".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
            else: 
                print("No more images")
                return image_urls
        
        # move the result startpoint further down
        results_start = len(thumbnail_results)


def download_image(folder_path: str, url: str, search_term: str, driver: webdriver):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_path = os.path.join(folder_path, search_term + ".jpg")
        with open(file_path, "wb") as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        driver.quit()
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, target_path, number_images=1):
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )
    target_folder = os.path.join(target_path)

    # create the directory
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # search the image
    with driver:
        res = fetch_image_urls(
            search_term, number_images, wd=driver, sleep_between_interactions=1
        )

    # download the image
    for elem in res:
        download_image(target_folder, elem, search_term, driver)


def main():
    a = str
    b = str
    search_and_download(a, b, number_images=5)


if __name__ == "__main__":
    main()
