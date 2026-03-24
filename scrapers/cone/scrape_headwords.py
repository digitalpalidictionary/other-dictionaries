import time
from rich import print
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


pali_alphabet = [
    "a", "ā", 
    "i", "ī", "u", "ū", "e", "o",
    "k", "kh", "g", "gh", "ṅ",
    "c", "ch", "j", "jh", "ñ",
    "ṭ", "ṭh", "ḍ", "ḍh", "ṇ",
    "t", "th", "d", "dh", "n",
    "p", "ph", "b", "bh", "m",
    "y", "r", "l", "s", "v", "h", "ḷ", "ṃ"
    ]

def scrape_headwords():
    print("[yellow]scraping headwords")

    driver = webdriver.Chrome()
    driver.get('https://gandhari.org/dictionary?section=dop')
    
    for letter in pali_alphabet:
        print(f"[green]letter: {letter}")
        search_box = driver.find_element("id", 'searchBox')
        search_box.clear()
        search_box.send_keys(letter)
        search_box.send_keys(Keys.RETURN)
        time.sleep(7)

        try:
            show_all_button = driver.find_element(By.ID, "llw")
            show_all_button.click()
            time.sleep(5)
        except Exception:
            print("[red]no 'show more' button")

        elements_with_tag0 = driver.find_elements(By.XPATH, "//*[contains(@class, 'tag0')]")
        headwords_list = [element.text for element in elements_with_tag0]

        with open("headwords.tsv", "a") as f:
            f.write(f"---{letter}---\n")
            for headword in headwords_list:
                f.write(f"{headword}\n")
    
    driver.quit()


if __name__ == "__main__":
    scrape_headwords()


