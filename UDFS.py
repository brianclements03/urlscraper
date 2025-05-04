# UDFS AND OTHER FUNCTIONS TO BE USED IN THE CRAWLER
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_core.documents import Document
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from urllib.parse import urljoin, urlparse
import time
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import logging


import os
import json
import re
from urllib.parse import urlparse


# ########################################################################################################################################################
# Helper: Get internal links from a page. THE HELPER IS CREATING OUR LIST OF URLS TO SCRAPE
# ########################################################################################################################################################
def get_internal_links(url):
    time.sleep(random.uniform(1.0,2.5)) #Sleep betwen 1.0 and 2.5 seconds
    links = set()
    try:
        # response = requests.get(url, timeout=10) #this was the requests functions that partially failed b/c the base_url is set up with Gatsby/React--so requests.get() only fetches the raw HTML without JavaScript execution. (IE only a placeholder page with no <a> tags or links)
        driver.get(url) #selenium scraper instead of requests.get()
        time.sleep(2) # wait for JS to load
        # soup = BeautifulSoup(response.text, 'html.parser') # changing this to reflect the new Selenium driver instead of response.text
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            if parsed.netloc.endswith(DOMAIN_FILTER) and parsed.scheme.startswith("http"):
                clean_url = full_url.split('#')[0]
                links.add(clean_url)
        logger.info(f"Links added for tracking for this level: {list(links)}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        logger.warning(f"Response Exception: failed to fetch {url}: {e}")
    return links


# #######################################################################################################################################################
# A BLOCK OF CODE TO REDO THE ACTUAL SCRAPING, THIS TIME WITH SELENIUM'S WEBDRIVEWAIT FUNCTION TO MORE CAREFULLY SCRAPE AND ONLY GRAB "MAIN" CONTENT WRAPPERS.
# #######################################################################################################################################################

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import logging

def get_page_text_with_retry(driver, url, retries=2, wait_time=10, wait_for_selector="main"):
    """
    Load a URL using Selenium and retry if no content appears.
    Uses WebDriverWait to wait for a specific DOM element.
    """
    for attempt in range(1, retries + 2):  # first try + retries
        try:
            driver.get(url)

            # Wait for the main content to load
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")
            text = soup.get_text(separator="\n").strip()

            if text:
                return text

            logging.warning(f"[Attempt {attempt}] No meaningful content at {url}")

        except TimeoutException:
            logging.warning(f"[Attempt {attempt}] Timeout waiting for selector '{wait_for_selector}' on {url}")
        except Exception as e:
            logging.error(f"[Attempt {attempt}] Error loading {url}: {e}")

        time.sleep(2 + attempt)  # Backoff before retry

    logging.error(f"❌ Final failure for {url}")
    return ""

# #######################################################################################################################################################
# HELPERS FOR SAVING TO A SEPARATE FOLDER WITH CLEANER FILE NAMES AND JSON METADATA
# #######################################################################################################################################################

    def sanitize_url_for_filename(url):
    # Strip scheme and convert slashes to underscores
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    path = re.sub(r"[^\w\-]+", "_", path)  # Keep it filename-safe
    if not path:
        path = "index"
    return path[:50]  # limit length to avoid overly long filenames


def save_documents_locally(docs, folder_name="scraped_output"):
    output_dir = os.path.join(os.getcwd(), folder_name)
    os.makedirs(output_dir, exist_ok=True)

    for i, doc in enumerate(docs):
        url = doc.metadata.get("source", f"no_url_{i}")
        safe_name = sanitize_url_for_filename(url)
        base_name = f"{i:03}_{safe_name}"

        # Save content
        txt_path = os.path.join(output_dir, f"{base_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f_txt:
            f_txt.write(doc.page_content)

        # Save metadata
        json_path = os.path.join(output_dir, f"{base_name}.json")
        with open(json_path, "w", encoding="utf-8") as f_json:
            json.dump(doc.metadata, f_json, indent=2)

    print(f"✅ Saved {len(docs)} documents to: {output_dir}")