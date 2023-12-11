import scrapy
from relacionados_google.items import RelacionadosGoogleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
#from scrapy_splash import SplashRequest

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    start_urls = ["https://www.google.com/search?q=como+ser+un+buen+manager&sca_esv=581137776&sxsrf=AM9HkKlR037hlRb86MPjFlpPwNM_P-h4_g%3A1699605962891&ei=yu1NZfT5NYm2i-gPyeWXkA0&oq=como+ser+un+buen+mana&gs_lp=Egxnd3Mtd2l6LXNlcnAiFWNvbW8gc2VyIHVuIGJ1ZW4gbWFuYSoCCAAyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSOohUABYnRRwAHgAkAEAmAFZoAHnC6oBAjIxuAEDyAEA-AEBwgIHECMYigUYJ8ICExAuGIoFGLEDGIMBGMcBGNEDGEPCAgoQABiKBRixAxhDwgILEAAYgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICBBAjGCfCAgcQABiKBRhDwgILEAAYigUYsQMYgwHCAgsQLhiABBjHARjRA8ICCBAuGIAEGLEDwgIEEAAYA8ICCBAAGIAEGLEDwgILEC4YgAQYsQMYgwHCAggQLhiABBjUAsICCxAuGIoFGLEDGIMBwgIIEAAYgAQYyQPCAggQABiKBRiSA8ICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAgoQABiABBgUGIcCwgIIEAAYFhgeGA_iAwQYACBBiAYBugYGCAEQARgU&sclient=gws-wiz-serp#ip=1"]

    def parse(self, response):
        keyword = RelacionadosGoogleItem()
        
        links = LinkExtractor(
            allow_domains=['google.com'],
            restrict_xpaths=['//a[@class= "k8XOCe R0xfCb VCOFK s8bAkb"]']
            #allow="/es/"
        ).extract_links(response)

        outlinks = []
        for link in links:
            url =link.url
            outlinks.append(url)
            yield Request(url, callback=self.parse)

        keyrel1 = response.xpath('//div[@class="s75CSd u60jwe r2fjmd AB4Wff"]/text()').extract()
        keyrel2 = response.xpath('//div[@class="s75CSd u60jwe r2fjmd AB4Wff"]/b/text()').extract()
        question = response.xpath('//span[@class="CSkcDe"]/text()').extract()
       
        maxterms = max(len(question),len(keyrel1))
            
        for poskey in range(0,maxterms):
            if poskey < len(question):
                keyword['keywordquestion']=question[poskey]
            else:
                keyword['keywordquestion']=None
            if poskey < len(keyrel1):
                if keyrel1[poskey][0] ==' ':
                    #if len(keyrel2)>=poskey:
                        keyword['keywordrelated']= keyrel2[poskey] + keyrel1[poskey]
                    #else:
                        #keyword['keywordrelated']= keyrel1[poskey]
                else:

                    #if len(keyrel2) < poskey:
                        #keyword['keywordrelated']= keyrel1[poskey]
                    #else:
                        keyword['keywordrelated']= keyrel1[poskey] + keyrel2[poskey]
            else:
                keyword['keywordrelated']= None
            yield  keyword
