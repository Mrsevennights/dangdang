class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        return len(self.new_urls) > 0

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None:
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        if self.has_new_url():
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            return new_url
