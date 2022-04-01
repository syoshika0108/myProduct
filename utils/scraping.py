#coding:utf-8

from os import SEEK_CUR
from selenium import webdriver
# from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as cs
 
PURPLE  = '\033[35m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
ENDC    = '\033[0m'
CHROMEDRIVER = "./chromedriver"
EMAIL = "shaun.the.earth@icloud.com"
PASSWORD = "shaun7218"
FILENAME = "./training_data/training.txt"

index = 1
cnt = 0

 
def ft_get_next_page(url):
	global index
	b.get(url)
	print(f"[{index}]", "current page is...", PURPLE, "---", b.title, "---", GREEN, b.current_url, ENDC)
	index += 1

chrome_service = cs.Service(executable_path = CHROMEDRIVER)
b = webdriver.Chrome(service = chrome_service)
FILE = open(FILENAME, "w")
b.maximize_window()

ft_get_next_page("https://www.onecareer.jp/")

b.find_element(By.LINK_TEXT, "ログイン").click()
b.find_element(By.ID, "user_email").send_keys(EMAIL)
b.find_element(By.ID, "user_password").send_keys(PASSWORD)
b.find_element(By.CLASS_NAME, "v2-vform-submit").click()

sectors = b.find_elements(By.CLASS_NAME, "v2-home-index-search-business-field-link")

# for sector in sectors:
# 	if sector.text == "IT・通信":
# 		ft_get_next_page(sector.get_attribute("href"))
# 		break
sectors_links = []
for sector in sectors:
	a = sector.get_attribute("href")
	sectors_links.append(a)
for link in sectors_links:
	ft_get_next_page(link)
	companies_elements = b.find_elements(By.CLASS_NAME, "v2-companies__title")
	companies_links = []
	for element in companies_elements:
		a = element.get_attribute("href")
		companies_links.append(a)
	for link in companies_links:
		ft_get_next_page(link)
		modes = b.find_elements(By.CLASS_NAME, "v2-companies-header-tab-nav__item")
		for mode in modes:
			if mode.text == "ES・体験談":
				mode_atag = mode.find_element(By.TAG_NAME, "a")
				link = mode_atag.get_attribute("href")
				ft_get_next_page(link)

				checkbox = b.find_element(By.XPATH, '//input[@value="recruitment"]')
				b.execute_script("arguments[0].click();", checkbox)
				checkbox = b.find_element(By.XPATH, '//input[@value="2022"]')
				b.execute_script("arguments[0].click();", checkbox)
				checkbox = b.find_element(By.XPATH, '//input[@value="2023"]')
				b.execute_script("arguments[0].click();", checkbox)
				checkbox = b.find_element(By.XPATH, '//input[@value="entry_sheet"]')
				b.execute_script("arguments[0].click();", checkbox)
				# value "1" means prehire
				checkbox = b.find_element(By.XPATH, '//input[@value="1"]')
				b.execute_script("arguments[0].click();", checkbox)
				b.find_element(By.CSS_SELECTOR, "input[value='絞り込む']").submit()

				entry_sheet_links = []
				entry_sheets = b.find_elements(By.CLASS_NAME, "v2-experience")
				for entry_sheet in entry_sheets:
					link = entry_sheet.find_element(By.TAG_NAME, "a").get_attribute("href")
					entry_sheet_links.append(link)
				for link in entry_sheet_links:
					ft_get_next_page(link)
					contents = b.find_element(By.CLASS_NAME, "v2-curriculum-item-body__content").find_elements(By.TAG_NAME, "p")
					for content in contents:
						if (len(content.text)) < 100:
							print(YELLOW, "\n-----trim start-----\n", ENDC)
							print(content.text)
							print(YELLOW, "\n-----trim end-----\n", ENDC)
							continue
						print("\n----- content.text -----\n")
						print(content.text.replace("\n", ""))
						FILE.write(content.text.replace("\n", ""))
						FILE.write("\n")
				break

b.set_window_size(1200, 600)
b.set_window_position(0, 0)
FILE.close()
b.quit()
