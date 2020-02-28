from selenium import webdriver
import pytest, csv


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def url_list_func():
    url_list = []
    with open("output/url-dic.csv", 'rb') as f:
        reader = csv.reader(f)
        for urls in reader:
            url_list.append(urls[0])
    return url_list


@pytest.mark.parametrize("a_url", url_list_func())
def test_prod_list(driver, a_url):
    driver.get(a_url)
    pr_list = driver.find_elements_by_xpath('//li[contains(@id,"result_")]')
    mp_id = (driver.find_elements_by_xpath('//select[@title="Search in"]/option[@selected="selected"]')[0])\
        .get_attribute('value')[3:]
    pr_urls = []
    pr_urls_1 = [pr_url.get_attribute("data-asin") for pr_url in pr_list]
    with open("output/product_urls.txt", 'r') as myfile:
        myfile = myfile.read().split("\n")
        for pu in pr_urls_1:
            string = "https://www.amazon.com/dp/" + pu + "/ref=sr_1_1?m=" + mp_id
            if string not in myfile:
                pr_urls.append(pu)
    with open("output/product_urls.txt", 'a') as myfile:
        for pr_url in pr_urls:
            myfile.write("https://www.amazon.com/dp/" + pr_url + "/ref=sr_1_1?m=" + mp_id + "\n")
    assert True
