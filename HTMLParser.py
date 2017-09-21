import re, json
from lxml import etree

class HtmlParser:
    def parser(self, response):
        if 'category' in response.url:
            items = self._parse(response)
            return items
        elif 'list' in response.url:
            items = self._parse_rate(response)
            return items
        else:
            items = self._parse_store(response)
            return items


    def _parse(self, response):
        items = []
        tree = etree.HTML(response.text)
        try:
            product_list = tree.xpath('//ul[@class="bigimg"]/li')
            for product in product_list:
                product_id = ''.join(product.xpath('./@id'))[1:]
                shop = product.xpath('./p[4]')[0].xpath('string(.)')
                if shop == '当当自营':
                    shop_id = str(0)
                else:
                    shop_id = ''.join(product.xpath('./p[4]/a[1]/@href'))[25:]
                url = ''.join(product.xpath('./a[1]/@href'))
                image_url = ''.join(product.xpath('./a[1]/img/@data-original'))
                if not image_url:
                    image_url = ''.join(product.xpath('./a[1]/img/@src'))
                title = ''.join(product.xpath('./p[1]/a/text()'))
                original_price = ''.join(product.xpath('./p[3]/span[2]/text()'))
                now_price = ''.join(product.xpath('./p[3]/span[1]/text()'))
                authors = product.xpath('./p[6]/span[1]')[0].xpath('string(.)')
                publication_time = ''.join(product.xpath('./p[6]/span[2]/text()'))[2:]
                press = ''.join(product.xpath('./p[6]/span[3]/a/text()'))
                product_rate_url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId=' +\
                                   product_id + '&mainProductId=' + product_id
                other_store_url = 'http://product.dangdang.com/index.php?r=callback%2Fspu-prod&productId=' +\
                                  product_id + '&shopId=' + shop_id
                item = {'product_id': product_id, 'shop': shop, 'shop_id': shop_id, 'url': url,
                        'image_url': image_url, 'title': title, 'original_price': original_price,
                        'now_price': now_price, 'authors': authors, 'publication_time': publication_time, 'press': press,
                        'product_rate_url': product_rate_url, 'other_store_url': other_store_url}
                items.append(item)
            next_page_url = tree.xpath('//div[@class="paging"]/ul/li[last()-1]/a/@href')
            if next_page_url:
                next_page_url = 'http://category.dangdang.com' + next_page_url[0]
            else:
                next_page_url = 'No next page'
            items.append(next_page_url)
            return items
        except Exception as e:
            print(e)
            return None


    def _parse_store(self, response):
        items = []
        value = json.loads(response.text)
        try:
            product_id = re.findall(r'productId=([0-9]+)', response.url)[0]
            min_price = value.get('data').get('minPrice')
            sellers_count = value.get('data').get('sellersCount')
            item = {'product_id': product_id, 'min_price': min_price, 'sellers_count': sellers_count}
            items.append(item)
            return items
        except Exception as e:
            print(e)
            return None

    def _parse_rate(self, response):
        items = []
        value = json.loads(response.text)
        try:
            product_id = value.get('data').get('summary').get('main_product_id')
            comment_num = value.get('data').get('summary').get('total_comment_num')
            good_rate = value.get('data').get('summary').get('goodRate')
            page_count = value.get('data').get('summary').get('pageCount')
            item = {'product_id': product_id, 'comment_num': comment_num,
                    'good_rate': good_rate, 'page_count': page_count}
            items.append(item)
            return items
        except Exception as e:
            print(e)
            return None