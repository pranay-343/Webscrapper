from selenium import webdriver
import pytest, csv, re
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


url_list = []
with open("output/product_urls.txt", 'r') as myfile:
    c = csv.reader(myfile, delimiter='\n', skipinitialspace=True)
    for line in c:
        url_list.append(line[0])


def try_expect_price(driver, xpath1, xpath2):
    try:
        tem_price = driver.find_element_by_xpath(xpath1).text
    except NoSuchElementException:
        try:
            tem_price = driver.find_element_by_xpath(xpath2).text
        except NoSuchElementException:
            tem_price = "0"
    # tem_price_1 = ' '.join([word.capitalize() for word in tem_price.split(' ')])
    tem_price = tem_price.encode('ascii', 'ignore')
    # print tem_price
    if tem_price.find("FREE Shipping") > -1:
        print tem_price
        tem_price = "0"
    return tem_price


def num_in_txt(txt):
    if re.findall("\d*\.?\d+", txt):
        return re.findall("\d*\.?\d+", txt)[0]
    else:
        return "0"


@pytest.mark.parametrize("url", url_list)
def test_prod_page(driver, url):
    sku1, price1 = get_sku_price(driver, url)
    url_new = "https://www.amazon.com/dp/" + sku1
    sku2, price2 = get_sku_price(driver, url_new)
    qt = 7
    if price1 == 0:
        qt = 0
    with open("output/Bulk Upload 16th Nov-1.csv", 'ab') as f:
        myfile = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        myfile.writerow([price2, "Dsa-STL-" + sku1, price1, qt, sku1, "ASIN", "New", "Brand New In original package"])

    with open("output/Autoprice-16 Nov.csv", 'ab') as f:
        myfile = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        myfile.writerow(["Dsa-STL-" + sku1, price1, price1 * 2, "RuleC-BulkEditing", "Start"])
    assert True


def get_sku_price(driver, url):
    driver.get(url)
    driver.implicitly_wait(15)
    prz = num_in_txt(
        try_expect_price(driver, '//span[contains(@class,"price3P")]', '//span[@id="priceblock_ourprice"]'))
    sprz = num_in_txt(try_expect_price(driver, '//span[contains(@class,"shipping3P")]',
                                       '//span[@id="ourprice_shippingmessage"]/span'))
    sku = (driver.current_url.split("dp/"))[1].split("/")[0]
    price = round(float(prz) + float(sprz), 2)
    return [sku, price]


def get_txt(driver, xpath):
    try:
        txt = driver.find_element_by_xpath(xpath).text
    except:
        txt = "NA"
    return txt


def remove_unicode(string_data):
    if string_data is None:
        return string_data
    if isinstance(string_data, str):
        string_data = str(string_data.decode('ascii', 'ignore'))
    else:
        string_data = string_data.encode('ascii', 'ignore')
    remove_ctrl_chars_regex = re.compile(r'[^\x20-\x7e]')
    return remove_ctrl_chars_regex.sub('', string_data)

