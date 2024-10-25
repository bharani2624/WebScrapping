from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.indeed.com/q-software-developer-jobs.html")
time.sleep(5)

jobs = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

for job in jobs:
    title = job.find_element(By.CSS_SELECTOR, 'h2.jobTitle span').text.strip()
    company = job.find_element(By.CLASS_NAME, 'companyName').text.strip()
    print(f"Job Title: {title}, Company: {company}")

driver.quit()
