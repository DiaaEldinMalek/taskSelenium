from dotenv import load_dotenv
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import convert_result_to_csv
import argparse

sys.path.append("/drivers")

load_dotenv()

url = os.getenv("guru-url")
username = os.getenv("guru-username")
password = os.getenv("guru-password")

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


from refactoring_guru import GuruScraper

GuruScraper(driver=driver, url=url, email=username, password=password).main()
parser = argparse.ArgumentParser(description="Process some options.")
parser.add_argument("--to-csv", action="store_true", help="Convert result to CSV")
args = parser.parse_args()

if args.to_csv:
    convert_result_to_csv()
