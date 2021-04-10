import scrapy
from FAQ.items import FAQItem


class FAQSpider(scrapy.Spider):
    name = 'zappos'
    allowed_domains = ['zappos.com']
    custom_settings = {
        'LOG_FILE': f'Log_{name}.txt',
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self):
        super(FAQSpider, self).__init__()
        self.company_name = self.name
        self.start_url = 'https://www.zappos.com/c/general-questions'

    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        questions = response.xpath("//dl//dt//abbr[@title='Question']/parent::dt//h4/text()").getall()
        answers = response.xpath("//dl//dd//abbr[@title='Answer']/parent::dd//div").getall()
        if len(questions) != len(answers):
            raise scrapy.exceptions.DropItem('number of questions and answers is not equal')
        for q, ans in zip(questions, answers):
            item = {'question': q,
                    'answer': ans,
                    'category': 'Others',
                    'url': response.url, 'company': self.company_name}
            faq = FAQItem(item)
            yield faq

    def process_request(self, request):
        # Called for each request that goes through the downloader
        # middleware.
        return None
