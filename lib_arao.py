from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



driver = webdriver.Chrome()

def BookSearch_in_AraoLib():
    url="https://www.arao-lib.jp/"
    driver.get(url)
    driver.maximize_window()
    sleep(1)
    
    driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > img").click()
    sleep(1)
    
    driver.find_element(By.ID, "keyword").click()
    sleep(1)
    
    driver.find_element(By.ID, "keyword").send_keys("python")
    sleep(1)
    
    driver.find_element(By.CSS_SELECTOR, ".search").click()
    sleep(1)
    
    driver.find_element(By.CSS_SELECTOR, ".pagerBox:nth-child(2) .disp:nth-child(2) > a").click()
    sleep(1)
     
    driver.find_element(By.ID, "img_9784299008152").click()
    sleep(3)

    driver.quit()







