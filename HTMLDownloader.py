import requests, time, random

class HtmlDownloader:
    def download(self, url):
        if url is None:
            return
        user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
        if 'product' in url:
            referer = 'http://product.dangdang.com/'
            headers = {'User-Agent': user_agent, 'Referer': referer}
        else:
            headers = {'User-Agent': user_agent}

        time.sleep(random.random() * 20)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if 'category' in response.url:
                response.encoding = 'GB2312'
            if 'product' in response.url:
                response.encoding = 'GBK'
            return response