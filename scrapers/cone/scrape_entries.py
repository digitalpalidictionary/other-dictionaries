import csv
import json
import re
import time

from copy import deepcopy
from rich import print
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def bip() -> None:
    """Start a mini clock."""
    global start_time
    start_time = time.time()


def bop() -> str:
    "End the mini clock and return elapsed time."
    elapsed_time = time.time() - start_time
    return f"{elapsed_time:.3f}"


def scrape_entries():
    print("[yellow]scraping entries")

    cone_dict = load_json()
    cone_dict_old = deepcopy(cone_dict)

    driver = webdriver.Chrome()
    driver.get('https://gandhari.org/dictionary?section=dop')

    for count, headword in enumerate(cone_dict):
        if not cone_dict[headword]:
            bip()

            # # remove bad characters + ( ) 
            # if re.findall(r"\(|\)", headword):
            #     headword = re.sub(r"\(|\)", "", headword)
            # if re.findall(r"\[|\]", headword):
            #     headword = re.sub(r"\[|\]", "", headword)
            # if " + " in headword:
            #     headword = headword.replace(" + ", "")
            
            print(f"{count:>7} / {len(cone_dict):<7}[green]{headword:<30}", end="")

            search_box = driver.find_element("id", 'searchBox')
            search_box.clear()
            search_box.send_keys(headword)
            search_box.send_keys(Keys.RETURN)

            def wait_for_element(driver, by, value):
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, value)))
                    return element
                except Exception:
                    print(f"Element {value} not found within 10 seconds.", end=" ")
                    return None
            
            element = wait_for_element(driver, By.ID, "gd3form_lem")
            
            if element:
                gd3definition_element = driver.find_element(By.ID, "gd3definition")
                html = gd3definition_element.get_attribute('outerHTML')
                cone_dict[headword] = html
            print(f"{bop():>5}")

        if count % 100 == 0:
            if cone_dict != cone_dict_old:
                save_json(cone_dict)
                cone_dict_old = deepcopy(cone_dict)

    save_json(cone_dict)
    driver.quit()


def get_headwords():
    with open('headwords.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        cone_dict = {}
        for row in reader:
            headword = row[0]
            if (
                not headword.startswith("---")
                and headword not in cone_dict
            ):
                cone_dict[headword] = ""
    return cone_dict


def save_json(cone_dict):
    print("[green]saving json")
    with open('cone_dict.json', 'w') as f:
        json.dump(cone_dict, f, ensure_ascii=False, indent=4)
    

def load_json():
    with open('cone_dict.json', 'r') as f:
        return json.load(f)
    

if __name__ == "__main__":
    scrape_entries()

    # # reset
    # cone_dict = get_headwords()
    # save_json(cone_dict)



