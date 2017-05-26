from HTMLParser import HTMLParser
# from urlparse import urlparse
from urlparse import urljoin

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super(LinkFinder, self).__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # when we call HTMLParser feed(), this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = urljoin(self.base_url, value)
                    self.links.add(url)
        print (tag)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

finder = LinkFinder()
finder.feed('<html><head><title>Test</title></head><html>')