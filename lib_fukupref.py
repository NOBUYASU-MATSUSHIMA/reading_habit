from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def BookSearch_in_FukPrefLib():
    driver = webdriver.Chrome()
    url="https://www2.lib.pref.fukuoka.jp/"
    driver.get(url)
    driver.maximize_window()
    sleep(1)
    
    driver.set_window_size(1296, 688)
    driver.find_element(By.CSS_SELECTOR, ".global_link:nth-child(2) .accordion-002-span").click()
    driver.find_element(By.NAME, "txt_word").click()
    driver.find_element(By.NAME, "txt_word").send_keys("Python")
    driver.find_element(By.NAME, "submit_btn_searchEasy").click()
    driver.find_element(By.CSS_SELECTOR, ".nav-area:nth-child(10) li:nth-child(2) > a").click()
    driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .title").click()

    driver.quit()

BookSearch_in_FukPrefLib()







