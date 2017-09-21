from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from multiprocessing.managers import BaseManager
import time

class Worker:
    def work(self, task_queue, result_queue, url_queue):
        downloader = HtmlDownloader()
        parser = HtmlParser()
        while True:
            while not task_queue.empty():
                new_url = task_queue.get()
                print('获得新任务: %s' % new_url)
                response = downloader.download(new_url)
                items = parser.parser(response)
                if len(items) > 1:
                    for i in range(0, 60):
                        product_rate_url = items[i].get('product_rate_url')
                        print('获得链接:%s' % product_rate_url)
                        other_store_url = items[i].get('other_store_url')
                        print('获得链接:%s' % other_store_url)
                        url_queue.put(product_rate_url)
                        url_queue.put(other_store_url)
                        print('获取结果:%s' % str(items[i]))
                        result_queue.put(items[i])
                    next_page_url = items[-1]
                    if next_page_url == 'No next page':
                        print('已经爬取到最后一页，工作节点准备结束')
                        result_queue.put('end')
                        return
                    url_queue.put(next_page_url)
                    print('获得链接:%s' % next_page_url)
                else:
                    print('获取结果:%s' % str(items[0]))
                    result_queue.put(items[0])


if __name__ == '__main__':
    worker = Worker()
    BaseManager.register('task_queue')
    BaseManager.register('result_queue')
    BaseManager.register('url_queue')

    manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'dang')
    manager.connect()
    task_queue = manager.task_queue()
    result_queue = manager.result_queue()
    url_queue = manager.url_queue()
    worker.work(task_queue, result_queue, url_queue)
    print('爬虫退出')