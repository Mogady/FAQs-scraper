import scrapy
from FAQ.items import FAQItem


class FAQSpider(scrapy.Spider):
    name = 'revzilla'
    allowed_domains = ['revzilla.com']
    custom_settings = {
        'LOG_FILE': f'Log_{name}.txt',
        'LOG_LEVEL': 'DEBUG',
    }

    def __init__(self):
        super(FAQSpider, self).__init__()
        self.company_name = self.name
        self.start_url = 'https://www.revzilla.com/faq'

    def start_requests(self):
        start_url = self.start_url
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        questions = []
        for t in response.xpath("//div[@class='wysiwyg__content']//section//h2"):
            questions.append(t.xpath('string(.)').extract()[0])
        answers = []
        for i in range(1, len(questions)):
            answers.append(response.xpath(
                "//h2[{}]/following-sibling::p[count(.|//h2[{}]/preceding-sibling::p)=count(//h2[{}]/preceding-sibling::p)]".format(
                    i, i + 1, i + 1)).getall())
        answers.append(response.xpath(
            "//h2/following-sibling::p[count(following-sibling::h2)=0]").getall())
        if len(questions) != len(answers):
            raise scrapy.exceptions.DropItem('number of questions and answers is not equal')
        for q, ans in zip(questions, answers):
            item = {'question': q,
                    'answer': ans, 'category': 'Others', 'url': response.url, 'company': self.company_name}
            faq = FAQItem(item)
            yield faq

    def process_request(self, request):
        # Called for each request that goes through the downloader
        # middleware.
        return None
