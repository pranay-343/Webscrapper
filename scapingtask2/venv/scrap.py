from bs4 import BeautifulSoup
import urllib
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')

urlpage =['http://us-business.info/directory/runnemede-nj/part2/']

# query the website and return the html to the variable 'page'
page = urllib.urlopen('http://us-business.info/directory/runnemede-nj/part2/')
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')
rows=[]
test= []
data = soup.findAll('div', class_="vcard")

#all = data[0]
for new in data:
    try:

            name = new.find('div', class_="fn org").get_text()
            street = new.find('span', class_="street-address").get_text()
            loc = new.find('span', class_="locality").get_text()
            tel = new.find('div', class_="tel").get_text()

    except:
        tel = None
    test = [name, street, loc, tel]
    with open('techtrack100.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(test)
        print test


# Create csv and write rows to output file




