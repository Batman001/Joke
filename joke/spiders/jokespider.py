from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from joke.items import JokeItem
import string

class JokeSpider(Spider):
    name = 'joke'
    base_url = 'http://xiaohua.zol.com.cn'
    url = 'http://xiaohua.zol.com.cn/new/1.html'
    start_urls = ['http://xiaohua.zol.com.cn/new/1.html']

    def parse(self, response):
        item = JokeItem()
        selector = Selector(response)
        jokes = selector.xpath('//li[@class="article-summary"]')
        print("==================================",len(jokes))
        nextPage = selector.xpath('//div[@class="page"]/a[@class="page-next"]/@href').extract()
        print(nextPage)
        for joke in jokes:
            yield Request(str(self.base_url + str(joke.xpath('span[@class="article-title"]/a/@href').extract()[0])), callback=self.parseContent)
        
        yield Request(str(self.base_url + str(nextPage[0])), callback=self.parse)

    def parseContent(self, response):
        selector = Selector(response)
        contents = selector.xpath('//div[@class="article-text"]').extract()
        print('content', len(contents))
        with open("jokes.txt", 'a') as f:
            final = "E\n"
            for content in contents:
                if str(content) == '':
                    continue
                final += str(content).replace('<p>', '').replace('</p>', '').replace('<div class="article-text">', '').replace('</div>', '').replace('\t', '')
            final += "\n"
            f.write(final)
            print("jokes into file Done!")
