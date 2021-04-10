from FAQ.items import FAQItem
import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse

CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument('--no-sandbox')
CHROME_OPTIONS.add_argument('--window-size=1420,1080')
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--disable-gpu')


class FAQSpider(scrapy.Spider):
    name = 'hallmark'
    allowed_domains = ['hallmark.com']
    custom_settings = {
        'LOG_FILE': f'Log_{name}.txt',
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self):
        super(FAQSpider, self).__init__()
        self.company_name = self.name
        self.start_url = 'https://care.hallmark.com/s/'

    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        categories = ['https://care.hallmark.com' + x for x in response.xpath("//a[@class='topicLink']/@href").getall()]
        cateogry_names = [x for x in response.xpath("//div[@class='topicLabel']/text()").getall()]
        for n, c in zip(categories, cateogry_names):
            for a in self.parse_categories(c):
                yield scrapy.Request(url=a, callback=self.parse_attr, meta={'category': n})

    def parse_categories(self, response):
        driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
        driver.get(response)
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@class='article-item selfServiceArticleListItem']"))
        )
        while True:
            try:
                load_more = driver.find_element_by_xpath(
                    "//button[@class='slds-button slds-button_brand slds-align_absolute-center loadmore']")
                driver.execute_script("arguments[0].click();", load_more)
                driver.implicitly_wait(2)
            except Exception as e:
                break
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@class='article-item selfServiceArticleListItem']")))

        articles = [x.get_attribute('href') for x in
                    driver.find_elements_by_xpath("//a[@class='article-link selfServiceArticleHeaderDetail']")]
        driver.close()
        return articles

    def parse_attr(self, response):
        item = {'question': response.xpath("//h1[@class='article-head selfServiceArticleHeaderDetail']/text()").get(),
                'answer': response.xpath("//article[@class='content']").get(), 'url': response.url,
                'category': response.meta['category'],
                'company': self.company_name}
        faq = FAQItem(item)

        return faq

    def process_request(self, request):
        # Called for each request that goes through the downloader
        # middleware.
        if 'hallmark.com' not in request.url or 'robots' in request.url:
            return None
        driver = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
        driver.get(request.url)
        if 'article' in request.url:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='slds-rich-text-editor__output uiOutputRichText forceOutputRichText']"))
            )
        else:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[@class='topicItem forceTopicFeaturedTopicItem']"))
            )

        body = driver.page_source
        url = driver.current_url
        driver.close()
        return HtmlResponse(url, body=body, encoding='utf-8', request=request)
