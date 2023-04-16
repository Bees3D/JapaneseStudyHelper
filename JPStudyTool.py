from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pyperclip

chromedriver = "file location"
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-logging"])
option.binary_location = "file location"
s = Service(chromedriver)
driver = webdriver.Chrome(service=s, options=option)


JISHO = "https://www.jisho.org"
OJAD = "https://www.gavo.t.u-tokyo.ac.jp/ojad/"
YOUGLISH = "https://youglish.com/japanese"
WORD = pyperclip.paste()


obsidian_new_note = rf"file location"

obsidian_file_location = r"file location"


def all_links():
    # Open all 3 of my most commonly used links for studying
    driver.get(JISHO)
    jisho_search = driver.find_element("xpath", '//*[@id="keyword"]')
    jisho_search.clear()
    jisho_search.send_keys(WORD)
    jisho_search.send_keys(Keys.RETURN)
    jisho_details = driver.find_element("xpath", '//*[@id="primary"]/div[1]/div[1]/a')
    jisho_details.click()
    jisho_link = "[Jisho]" + "(" + driver.current_url + ")"

    word_type = driver.find_element(
        "xpath", '//*[@id="page_container"]/div/div/article/div/div[2]/div/div[1]'
    )

    # Find meaning/definition
    meaning = driver.find_element(
        "xpath",
        '//*[@id="page_container"]/div/div/article/div/div[2]/div/div[2]/div/span[2]',
    ).text

    # Find kunyomi and onyomi readings
    kunyomi = driver.find_element(
        "xpath", '//*[@id="page_container"]/div/div/aside/div/div/div/div[5]/span[2]/a'
    ).text
    onyomi = driver.find_element(
        "xpath", '//*[@id="page_container"]/div/div/aside/div/div/div/div[6]/span[2]/a'
    ).text
    readings = f"**Kun**: {kunyomi}\n**On**: {onyomi}"

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(OJAD)
    ojad_search = driver.find_element("xpath", '//*[@id="search_word"]')
    ojad_search.clear()
    ojad_search.send_keys(WORD)
    ojad_search.send_keys(Keys.RETURN)
    ojad_link = "[OJAD]" + "(" + driver.current_url + ")"

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(YOUGLISH)
    youglish_search = driver.find_element("xpath", '//*[@id="q"]')
    youglish_search.clear()
    youglish_search.send_keys(WORD)
    youglish_search.send_keys(Keys.RETURN)
    youglish_link = "[YouGlish]" + "(" + driver.current_url + ")"

    with open(obsidian_file_location, "r+", encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            if line.strip() == "":
                f.write(
                    f"[[{WORD}]] - {meaning} | {jisho_link} | {ojad_link} | {youglish_link}\n***\n"
                )

    with open(obsidian_new_note, "w+", encoding="utf-8") as f:
        f.write(
            f"{jisho_link} | {ojad_link} | {youglish_link}\n***\n**READINGS**:\n{readings}\n***\n**MEANING**:\n{meaning}\n***\n**EXAMPLES**:\n"
        )
