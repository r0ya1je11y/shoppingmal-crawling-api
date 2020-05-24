import ssl, codecs, time, urllib3, requests, json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict
from parse import *

context = ssl._create_unverified_context()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path = "C:/Users/skydn/downloads/chromedriver.exe"
driver = webdriver.Chrome(path)

baseurl = "https://item.taobao.com/item.htm?id="
productID = input()
url = baseurl + productID
driver.get(url)

# Click the alert window
#if driver.find_element_by_id('simpleAlert'):
#    inputElement = driver.find_element_by_id('simpleAlert')
#    inputElement.click()
#    time.sleep(2)

# Take a 'BeautifulSoup'
result = urlopen(url, context=context)
time.sleep(10)
bsObj = BeautifulSoup(result.read(), "html.parser")

# Parse a name of the product
Name = bsObj.find('h3', {'class':'tb-main-title'})
productName = Name.text.strip()
print(productName)

print("============")
# Parse a option of the product
Skin = bsObj.find('div', {'class':'tb-skin'})
Option = Skin.find('dl').find('dd').find_all('a')

optionTitle = []
for title in Option:
    optionTitle.append(title.find('span').text)
    print(title.find('span').text) # Option Title

print("============")

optionImage = []
for image in Option:
    if image.get('style') is not None:
        styleTag = image.get('style')
        result = parse("background:url({}) center no-repeat;", styleTag)
        optionImage.append(result[0])
        print(result[0]) # Option Image if exist
    else:
        optionImage.append("")

print("============")

productOption = {}
for i in range(0, len(optionTitle)-1):
    productOption[optionTitle[i]] = optionImage[i]
# Parse a price of the product
Price_div = bsObj.find('ul', class_="tb-meta")
print(Price_div)

#driver.close()


#========================================

# Make .json file
file_data = OrderedDict()

file_data["name"] = productName
file_data["id"] = productID
#file_data["price"] = productPrice
file_data["option"] = productOption

print(json.dumps(file_data, ensure_ascii=False, indent='\t'))

with open('data/taobao.json', 'w', encoding="utf-8") as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')