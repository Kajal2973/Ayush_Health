from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def scrape_ayush_data(query):
    service = Service("chromedriver.exe")  # Specify the path to your ChromeDriver
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com")
    
    time.sleep(3)  # Give time for page to load
    results = []

    herbs = driver.find_elements(By.CLASS_NAME, "herb-card")
    for herb in herbs:
        name = herb.find_element(By.TAG_NAME, "h2").text
        benefits = herb.find_element(By.CLASS_NAME, "benefits").text
        results.append({"name": name, "benefits": benefits})
    
    driver.quit()
    return results
