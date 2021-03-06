from HTMLParser import HTMLParser
from urlparse import urljoin

__metaclass__ = type

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        # ===============================================
        HTMLParser.__init__(self) # important
        # ===============================================
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # when we call HTMLParser feed(), this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = urljoin(self.base_url, value)
                    print url
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
