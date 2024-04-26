#import the libraries
import bs4 as bs
import sys
import schedule
import time
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
frequecy = 2500
duration = 1000

class Page(QWebEnginePage):
    def __init__(self,url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()


    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('load finished')

    def Callable(self,html_str):
        self.html = html_str
        self.app.quit()

def exact_url(url):
    index = url.find("BO")
    index = index +10
    current_url = ""
    current_url = url[:index]
    return current_url

def mainprogram():
    url = "https://www.amazon.in/Airtel-4G-Hotspot-E5573Cs-609-Portable/dp/B06WV9WR4Z"
    page = Page(url)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    js_test = soup.find('span', class_='a-price-whole')
    if js_test is None:
        js_test = soup.find('span', class_='a-price')
    
    if js_test:
        str_price = ''.join(js_test.stripped_strings)
        # Remove any commas from the price string
        str_price = str_price.replace(',', '')
        if str_price and str_price != '.':
            try:
                current_price = float(str_price)
                your_price = 600
                if current_price < your_price:
                    print("Price decreased. Book now.")
                else:
                    print("Price is high. Please wait for the best deal.")
                    print("current price",current_price)
            except ValueError:
                print("Failed to convert price to float:", str_price)
        else:
            print("Price string is empty or contains only a dot ('.')")
    else:
        print("Price element not found on the page.")
def job():
    print("tracking...")
    mainprogram()

schedule.every(1).minute.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
    