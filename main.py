import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver
service = Service('C:\\chromedriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# URLs and login credentials
admin_login_url = "https://platform.swahilipothub.org/admin/login/?next=/admin/"
add_page_url = "https://platform.swahilipothub.org/admin/youthApp/youth/add/"
email = "c.mwalimo@swahilipothub.co.ke"
password = "@Sph12345"
excel_file = "C:\\test\\tes.xlsx"

# Define field mappings
fields_to_check = {
    'first_name': 'first_name',
    'middle_name': 'middle_name',
    'last_name': 'last_name',
    'identification_document_number': 'identification_document_number',
    'phone_number': 'phone_number',
    'email': 'email',
    'areas_of_interest': 'areas_of_interest',
    'county_of_residence': 'county_of_residence',
    'subcounty_of_residence': 'subcounty_of_residence',
    'ward_of_residence': 'ward_of_residence'
}

# Log in to Django admin
def login():
    driver.get(admin_login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
    time.sleep(3)
    print("Logged in successfully.")

# Function to fill and verify fields
def fill_and_verify_field(selector, value, by=By.NAME):
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, selector)))
        element.clear()
        element.send_keys(value)
        print(f"Filled '{selector}' with '{value}'.")

        entered_value = element.get_attribute('value')
        if entered_value == value:
            print(f"Verified '{selector}': Value correctly entered as '{entered_value}'.")
        else:
            print(f"Verification failed for '{selector}': Expected '{value}', but got '{entered_value}'.")

    except Exception as e:
        print(f"Error with element '{selector}': {e}")

# Function to fill in a searchable dropdown
def fill_and_select_dropdown(field_name, value):
    try:
        # Open the dropdown for searchable input
        dropdown_trigger = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'.field-{field_name} .select2-selection')))
        dropdown_trigger.click()
        print(f"Opened dropdown for '{field_name}'.")

        # Enter the value in the search input
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
        search_input.clear()
        search_input.send_keys(value)
        time.sleep(1)  # Allow options to load

        # Select the first option
        first_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-results__option--highlighted'))
        )
        first_option.click()
        print(f"Selected '{value}' for '{field_name}'.")

    except Exception as e:
        print(f"Error with dropdown '{field_name}': {e}")

# Function to select a non-searchable dropdown for areas_of_interest
def select_standard_dropdown(selector, value):
    try:
        # Locate the select element
        select_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, selector)))
        select = Select(select_element)

        # Attempt exact match first
        try:
            select.select_by_visible_text(value)
            print(f"Selected '{value}' for '{selector}' (exact match).")
        except:
            # If exact match fails, iterate through options to find a partial match
            matched = False
            for option in select.options:
                option_text = option.text.strip()
                if value.lower() in option_text.lower():
                    option.click()
                    print(f"Selected '{option_text}' for '{selector}' (partial match).")
                    matched = True
                    break
            if not matched:
                print(f"No match found for '{value}' in '{selector}' options.")
    except Exception as e:
        print(f"Error selecting '{selector}': {e}")

# Select nationality
def select_nationality():
    try:
        dropdown_trigger = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection')))
        dropdown_trigger.click()
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
        search_input.clear()
        search_input.send_keys('Kenyan' + Keys.ENTER)
        print("Selected nationality: Kenyan")
    except Exception as e:
        print(f"Error selecting nationality: {e}")

# Process and fill data from Excel
def process_data():
    data = pd.read_excel(excel_file)
    print("Data columns:", data.columns)

    for index, row in data.iterrows():
        driver.get(add_page_url)
        time.sleep(2)

        for field, column_name in fields_to_check.items():
            if column_name not in data.columns:
                print(f"Column '{column_name}' does not exist in the data.")
                continue

            value = str(row[column_name]).strip() if pd.notna(row[column_name]) else ''
            
            # Use the standard dropdown for areas_of_interest
            if field == 'areas_of_interest':
                select_standard_dropdown(field, value)
            # Use the dropdown filling function for other searchable dropdown fields
            elif field in ['county_of_residence', 'subcounty_of_residence', 'ward_of_residence']:
                fill_and_select_dropdown(field, value)
            else:
                fill_and_verify_field(selector=field, value=value)

        select_nationality()
        print(f"Record {index + 1} processed successfully.")

    print("All records processed.")

# Run the automation
try:
    login()
    process_data()
finally:
    driver.quit()
    print("Browser closed.")




# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Set up WebDriver
# service = Service('C:\\chromedriver\\chromedriver.exe')
# driver = webdriver.Chrome(service=service)

# # URLs and login credentials
# admin_login_url = "https://platform.swahilipothub.org/admin/login/?next=/admin/"
# add_page_url = "https://platform.swahilipothub.org/admin/youthApp/youth/add/"
# email = "c.mwalimo@swahilipothub.co.ke"
# password = "@Sph12345"
# excel_file = "C:\\test\\tes.xlsx"

# # Define field mappings
# fields_to_check = {
#     'first_name': 'first_name',
#     'middle_name': 'middle_name',
#     'last_name': 'last_name',
#     'identification_document_number': 'identification_document_number',
#     'phone_number': 'phone_number',
#     'email': 'email',
#     'areas_of_interest': 'areas_of_interest',
#     'county_of_residence': 'county_of_residence',
#     'subcounty_of_residence': 'subcounty_of_residence',
#     'ward_of_residence': 'ward_of_residence'
# }

# # Log in to Django admin
# def login():
#     driver.get(admin_login_url)
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(email)
#     driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
#     time.sleep(3)
#     print("Logged in successfully.")

# # Function to fill and verify fields
# def fill_and_verify_field(selector, value, by=By.NAME):
#     try:
#         element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, selector)))
#         element.clear()
#         element.send_keys(value)
#         print(f"Filled '{selector}' with '{value}'.")

#         entered_value = element.get_attribute('value')
#         if entered_value == value:
#             print(f"Verified '{selector}': Value correctly entered as '{entered_value}'.")
#         else:
#             print(f"Verification failed for '{selector}': Expected '{value}', but got '{entered_value}'.")

#     except Exception as e:
#         print(f"Error with element '{selector}': {e}")

# # Function to fill in a searchable dropdown
# def fill_and_select_dropdown(field_name, value):
#     try:
#         # Click the dropdown to open it
#         dropdown_trigger = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'.field-{field_name} .select2-selection')))

#         dropdown_trigger.click()
#         print(f"Opened dropdown for '{field_name}'.")

#         # Wait for the search input to be visible and enter the value
#         search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
#         search_input.clear()
#         search_input.send_keys(value)
#         time.sleep(1)  # Wait for options to load

#         # Select the first visible option
#         first_option = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-results__option--highlighted'))
#         )
#         first_option.click()
#         print(f"Selected '{value}' for '{field_name}'.")

#     except Exception as e:
#         print(f"Error with dropdown '{field_name}': {e}")

# # Select nationality
# def select_nationality():
#     try:
#         dropdown_trigger = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection')))
#         dropdown_trigger.click()
#         search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
#         search_input.clear()
#         search_input.send_keys('Kenyan' + Keys.ENTER)
#         print("Selected nationality: Kenyan")
#     except Exception as e:
#         print(f"Error selecting nationality: {e}")

# # Process and fill data from Excel
# def process_data():
#     data = pd.read_excel(excel_file)
#     print("Data columns:", data.columns)

#     for index, row in data.iterrows():
#         driver.get(add_page_url)
#         time.sleep(2)

#         for field, column_name in fields_to_check.items():
#             if column_name not in data.columns:
#                 print(f"Column '{column_name}' does not exist in the data.")
#                 continue

#             value = str(row[column_name]).strip() if pd.notna(row[column_name]) else ''
            
#             # Use the dropdown filling function for specific fields
#             if field in ['areas_of_interest', 'county_of_residence', 'subcounty_of_residence', 'ward_of_residence']:
#                 fill_and_select_dropdown(field, value)
#             else:
#                 fill_and_verify_field(selector=field, value=value)

#         select_nationality()
#         print(f"Record {index + 1} processed successfully.")

#     print("All records processed.")

# # Run the automation
# try:
#     login()
#     process_data()
# finally:
#     driver.quit()
#     print("Browser closed.")
