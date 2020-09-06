import scrapy,random,string
from ..items import VijaysalesElectronicsItem

class VijaysalesSpider(scrapy.Spider):

    name = 'vijaytablet'
    pageno=20

    start_urls=['https://www.vijaysales.com/Mobiles-Tablets/TABLETS/1/976']

    def parse(self, response, **kwargs):

        page = response.css("a.vj-cur-pnter::attr('href')").getall()

        for p in page:

             yield scrapy.Request(p, callback=self.parse_elec)

       # page = 'https://www.snapdeal.com/acors/json/product/get/search/175/'+ str(VijaysalesSpider.pageno)+ '/20?q=&sort=plrty'
        #if VijaysalesSpider.pageno <= 100:
         #   VijaysalesSpider.pageno += 20
          #  yield response.follow(page, callback=self.parse)


    def parse_elec(self, response):

         items = VijaysalesElectronicsItem()

         product_name = response.css('#ContentPlaceHolder1_h1ProductTitle::text').get()

         storeprice = response.css('#ContentPlaceHolder1_divPrdPriceStucture .row_ .amt::text').get()

         storeLink = response.url

         id = storeLink[::-1].find('/')


         photos = response.css('img#ContentPlaceHolder1_ProductImage').xpath("@src").get()

         spec_title = response.css(".sptyp::text").extract()

         spec_detail = response.css(".spval::text").extract()

         product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))

        #rating = response.css('span.avrg-rating::text').get()
        #reviews = response.css('#defaultReviewsCard p::text').extract()

         stores = {

             "rating": [],
             "reviews":[],
             'storeproductid': storeLink[-id:],
             "storeLink": storeLink,
             "storeName": "Vijaysales",
             "storePrice": storeprice,

        }

         items['product_name'] = product_name.strip()
         items['product_id'] = product_id
         items['stores'] = stores
         items['category'] = 'electronics'
         items['subcategory'] = 'tablet'
         items['brand'] = product_name.split()[0]
         items['description'] = {}

         for i in range(len(spec_title)):
              items['description'][spec_title[i].strip()] = spec_detail[i].strip()

         items['photos'] = photos

         yield items