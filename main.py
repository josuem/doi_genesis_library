''' genesis_library.py
A simple program to find a list of DOI on genesis library.

TODO: 
- new program to extract DOI from page
'''
__author__ = 'Josué Meneses Díaz'
__email__ = 'josue.meneses@usach.cl'
__version__ = '1.0'

# source : https://www.youtube.com/watch?v=wbfcuoKzHgc&t=12s
# source : https://www.youtube.com/watch?v=18fxDASTmX0&list=PLas30d-GGNa2UW9-1H-NCNrUocvWD9cyh&index=4

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions() 
# options.add_argument("download.default_directory=C:/Users/josue/Downloads/testDOI/")

path   = os.getcwd()
chrome = '\\chromedriver'

url 	= 'http://libgen.rs/'
# page 	= requests.get(url)
xlsxFilename 	= 'DOIs.xlsx' 

xlsx = pd.read_excel( xlsxFilename ).fillna('')
driver = webdriver.Chrome( executable_path = path + chrome ) 

def every_downloads_chrome(driver):
	''' wait for download finish
	Source: https://stackoverflow.com/a/60677334'''

	if not driver.current_url.startswith("chrome://downloads"):
		driver.get("chrome://downloads/")
	return driver.execute_script("""
		return document.querySelector('downloads-manager')
		.shadowRoot.querySelector('#downloadsList')
		.items.filter(e => e.state === 'COMPLETE')
		.map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
		""")

for i in range(len(xlsx)):
	# DOI = 'https://doi.org/10.1122/8.0000488'
	# DOI = 'https://doi.org/10.1121/1.1909020'
	
	DOI = xlsx.iat[ i, 0]
	print('Processing DOI: %s \n', DOI)
	os.system('cls')

	driver.get( url )

	search = driver.find_element_by_id('searchform')
	buttonScientificArticles = driver.find_element_by_xpath(r'/html/body/table/tbody[2]/tr/td[2]/form/table/tbody/tr/td[3]/input') 
	buttonScientificArticles.click()
	search.send_keys( DOI)
	search.send_keys(Keys.ENTER)

	time.sleep(1)

	try:
		enable = driver.find_element_by_xpath(r'/html/body/div[1]/div')
	except:
		enable = driver.find_element_by_xpath(r'/html/body/p[2]')

	print( enable.text )

	if enable.text != 'No articles were found.' and xlsx.iat[ i, 2] != 'yes':
		print('DOI available')
		# Change the page to donwload
		buttonLibgen = driver.find_element_by_xpath(r'/html/body/table/tbody/tr/td[5]/ul/li[2]/a')
		buttonLibgen.click()
		time.sleep(1)
		# download pdf
		buttonGET = driver.find_element_by_xpath(r'//*[@id="download"]/h2/a')
		buttonGET.click()
		time.sleep(3)

		# waits for all the files to be completed and returns the paths
		paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
		print(paths)

		xlsx.iat[ i, 1] = 'yes'
		xlsx.iat[ i, 2] = 'yes'

	elif xlsx.iat[ i, 2] != 'yes':
		print('Paper was downloaded, Skipping!!!')

	else:
		print('DOI not available')
		xlsx.iat[ i, 1] = 'no'
		xlsx.iat[ i, 2] = 'no'

	time.sleep(5)
driver.close()
xlsx.to_excel( xlsxFilename, index=False)
print('Review finished!!!')
print(xlsx)