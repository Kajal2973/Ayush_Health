'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up ChromeDriver path
service = Service('chromedriver.exe')  # Add path if needed
driver = webdriver.Chrome(service=service)

# Open target website
driver.get('https://example.com')

# Get page title
title = driver.title
print(f"Page title: {title}")

# Scrape specific elements
data = driver.find_elements(By.CLASS_NAME, 'class-name')
for item in data:
    print(item.text)

# Close browser
driver.quit()
'''