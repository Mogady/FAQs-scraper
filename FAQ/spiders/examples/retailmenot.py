from FAQ.items import FAQItem
import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument('--no-sandbox')
CHROME_OPTIONS.add_argument('--window-size=1420,1080')
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--disable-gpu')


class FAQSpider(scrapy.Spider):
    name = 'retailmenot'
    allowed_domains = ['retailmenot.com']
    custom_settings = {
        'LOG_FILE': f'Log_{name}.txt',
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self):
        super(FAQSpider, self).__init__()
        self.company_name = self.name
        self.start_url = 'https://help.retailmenot.com/s/'

    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        sources = []
        driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
        driver.get(response.url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='slds-card__footer slds-text-align_center topicFooter']"))
        )
        sample_cat = driver.find_elements_by_xpath(
            "//div[@class='slds-card__footer slds-text-align_center topicFooter']")[0]
        driver.execute_script("arguments[0].click();", sample_cat)
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='topicLink cHelpTopics']")))
        categories = driver.find_elements_by_xpath(
            "//div[@class='topicLink cHelpTopics']//a")
        names = [x.text for x in driver.find_elements_by_xpath(
            "//div[@class='topicLink cHelpTopics']//a")]
        for i in range(len(categories)):
            driver.execute_script("arguments[0].click();", categories[i])
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='topicLink cHelpTopics']")))
            tmp_url = driver.current_url
            questions = driver.find_elements_by_xpath("//a[@class='articleLink']")
            for j in range(len(questions)):
                driver.execute_script("arguments[0].click();", questions[j])
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH,
                                                         "//div[@class='slds-rich-text-editor__output uiOutputRichText forceOutputRichText']")))
                sources.append((driver.page_source, driver.current_url, names[i]))
                driver.get(tmp_url)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='topicLink cHelpTopics']")))
                questions = driver.find_elements_by_xpath("//a[@class='articleLink']")
                time.sleep(1)

            categories = driver.find_elements_by_xpath(
                "//div[@class='topicLink cHelpTopics']//a")

        driver.close()
        for s in sources:
            yield self.parse_attr(s)

    def parse_attr(self, tup):
        response = scrapy.Selector(text=tup[0])
        item = {'question': response.xpath("//h1[@class='article-head selfServiceArticleHeaderDetail']/text()").get(),
                'answer': response.xpath("//article[@class='content']").get(), 'url': tup[1], 'category': tup[2],
                'company': self.company_name}
        faq = FAQItem(item)

        return faq

    def process_request(self, request):
        # Called for each request that goes through the downloader
        # middleware.
        return None
