from selenium import webdriver
import pytest, csv


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def store_ids_list():
    store_ids = []
    with open('output/Store-dic.csv', 'rb') as f:
        reader = csv.reader(f)
        for srow in reader:
            if len(srow) != 0:
                store_ids.append(srow[0])
    return store_ids


def keyword_ids_list():
    keyword_list = []
    with open('output/keyword-dic.csv', 'rb') as f:
        reader = csv.reader(f)
        for krow in reader:
            if len(krow) != 0:
                keyword_list.append(krow[0])
    return keyword_list


@pytest.mark.parametrize("store_id", store_ids_list())
@pytest.mark.parametrize("keyword", keyword_ids_list())
def test_get_pages(driver, keyword, store_id):
    driver.get("https://www.amazon.com/s/ref=sr_pg_1?me=" + store_id + "&rh=" + keyword +
                                    "&page=1&keywords=" + keyword + "&ie=UTF8&qid=1511940872&lo=none")
    page_end = int((try_except_page(driver, '//div[@id="pagn"]/span[last()-1]')))
    for n in range(1, page_end+1):
        p_url = "https://www.amazon.com/s/ref=sr_pg_" + str(n) + "?me=" + store_id + "&rh=" + \
                keyword + "&page=" + str(n) + "&keywords=" + keyword + "&ie=UTF8&qid=1511940872&lo=none"
        with open("output/url-dic.csv", 'ab') as f:
            myfile = csv.writer(f)
            myfile.writerow([p_url])
    assert True


def try_except_page(driver, xpath):
    try:
        page = (driver.find_elements_by_xpath(xpath)[0]).text
    except IndexError:
        page = '1'
    return page
