from selenium import webdriver
from selenium.webdriver.common.by import By
from secrets import secrets
import datetime

# Allows chrome to be headless with chrome version
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get('https://apps.nottingham.edu.my/jw/web/login')

# Logic to pick 3 days ahead
today = datetime.date.today()
bkDate = today + datetime.timedelta(days=3)
bkDateNum = bkDate.strftime("%d")

# Log in
user_textbox = driver.find_element(By.ID, "j_username")
user_textbox.send_keys(secrets["user"])

password_textbox = driver.find_element(By.ID, "j_password")
password_textbox.send_keys(secrets["password"])

login_button = driver.find_element(By.CSS_SELECTOR, "input.form-button")
login_button.click()

for i in range(0, 2):
    # Redirect to booking
    driver.get("https://apps.nottingham.edu.my/jw/web/userview/booking/v/_/request")
    common_url = "/html/body/div[2]/div[1]/div/div[2]/main/div[1]/fieldset/form/"

    # Select room
    if "strength" in secrets["purpose"].lower():
        strength_room = driver.find_element(By.XPATH, common_url + "div[1]/div[2]/div/div[1]/label[1]/i")
        strength_room.click()
        room = 1
    elif "cardio" in secrets["purpose"].lower():
        cardio_room = driver.find_element(By.XPATH, common_url + "div[1]/div[2]/div/div[1]/label[2]/i")
        cardio_room.click()
        room = 2
    elif "swim" in secrets["purpose"].lower():
        swimming_pool = driver.find_element(By.XPATH, common_url + "div[1]/div[2]/div/div[1]/label[3]/i")
        swimming_pool.click()
        room = 3

    # Click next
    next_btn = driver.find_element(By.XPATH, common_url + 'div[3]/div[2]/div/i/input')
    next_btn.click()

    # Fill up booking form
    number_textbox = driver.find_element(By.ID, "contact_no")
    number_textbox.send_keys(secrets["number"])

    purpose_textbox = driver.find_element(By.ID, "purpose")
    purpose_textbox.send_keys(secrets["purpose"])

    venue_list = driver.find_element(By.XPATH, common_url + f"div[2]/div[2]/div[6]/select/option[{room}]")
    venue_list.click()

    bkDate_textBox = driver.find_element(By.XPATH, common_url + "div[6]/div[2]/div/input")
    bkDate_textBox.click()

    bkDate_input = driver.find_element(By.XPATH, f"/html/body/div[3]/table/tbody/tr/td/a[text()={bkDateNum}]")
    bkDate_input.click()

    # Pick slot
    slot = driver.find_element(By.XPATH,
                               common_url + f"div[9]/div[2]/div[2]/div[1]/label[{int(secrets['time1']) + i}]/i")
    slot.click()

    complete_btn = driver.find_element(By.XPATH, common_url + f"div[11]/div[2]/div/i/input")
    complete_btn.click()
