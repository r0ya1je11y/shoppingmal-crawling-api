import ssl, codecs, time, urllib3, requests, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementNotVisibleException
from collections import OrderedDict
from parse import *

def CrawlingTaobao(productID, userID, userPasswd):
    context = ssl._create_unverified_context()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # webdriver path settings
    path = "C:/Users/skydn/downloads/chromedriver.exe"
    driver = webdriver.Chrome(path)

    # Make a url of a product
    baseurl = "https://item.taobao.com/item.htm?id="
    url = baseurl + productID
    driver.get(url)

    # Click the alert window
    try:
        IsAlart = driver.switch_to_alert()
        IsAlart.accept()
    except:
        "There is no alert"

    # Login Taobao
    driver.implicitly_wait(5)

    driver.switch_to_frame(driver.find_element_by_id('sufei-dialog-content'))

    driver.find_element_by_id('fm-login-id').send_keys(userID) # Input the ID
    driver.find_element_by_id('fm-login-password').send_keys(userPasswd) # Input the Password

    time.sleep(3)

    source = driver.find_element_by_id('nc_1_n1z')
    destination = driver.find_element_by_id('nc_1__scale_text')
    action = ActionChains(driver)
    action.click_and_hold(source).move_to_element_with_offset(destination, 250, 20).pause(1).release().perform() # Drag-and-drop slidebar

    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click() # Click the login button

    driver.switch_to_default_content()

    time.sleep(3)

    # Take a 'BeautifulSoup'
    html = driver.page_source
    bsObj = BeautifulSoup(html, "html.parser")

    # Parse a name of the product
    Name = bsObj.find('h3', {'class':'tb-main-title'})
    productName = Name.text.strip()

    # Parse a option of the product
    Skin = bsObj.find('div', {'class':'tb-skin'})
    Option = Skin.find('dl').find('dd').find_all('a')

    optionTitle = []
    for title in Option:
        optionTitle.append(title.find('span').text)

    optionImage = []
    for image in Option:
        if image.get('style') is not None:
            styleTag = image.get('style')
            result = parse("background:url({}) center no-repeat;", styleTag)
            optionImage.append(result[0])
        else:
            optionImage.append("")

    # Parse a Price of the product
    driverOption = driver.find_elements_by_css_selector('#J_isku > div > dl.J_Prop.tb-prop.tb-clear.J_Prop_Color > dd > ul > li > a')
    productPrice = []
    for option in driverOption:
        option.send_keys(Keys.ENTER)
        try:
            driver.find_element((By.ID, 'J_PromoPriceNum'))
            productPrice.append(driver.find_element_by_id('J_PromoPriceNum').text)
        except:
            productPrice.append(driver.find_element_by_class_name('tb-rmb-num').text)

    # Make dictionary for all information of product
    productOption = {}
    for i in range(0, len(optionTitle)-1):
        productInfo = {}
        productInfo['price'] = productPrice[i]
        productInfo['image'] = optionImage[i]
        productOption[optionTitle[i]] = productInfo # Make dictionary of {optionTitle:optionImage}

    driver.close()

    # Make .json file
    file_data = OrderedDict()

    file_data["name"] = productName
    file_data["id"] = productID
    file_data["url"] = url
    file_data["option"] = productOption

    with open('data/' + productID + '.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent='\t')