from urllib2 import urlopen
from link_finder import LinkFinder
from urlparse import urljoin
from domain import *
import chardet
from general import *
import sys
from urllib import quote, quote_plus
import string
reload(sys)


class Spider:

    # Class variables (are shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    server_name = ''
    queue_file = ''
    crawled_file = ''
    json_file = ''
    json_text = dict()
    file_order = 0
    queue = set()
    crawled = set()

    # dic=dict()
    # c1 = html_bytes.decode("utf-8")
    # c2 = c1.encode("utf-8")
    # dic["c"] = c2
    # with open("a.json", "w") as fw:
    #     json.dump(dic, fw)
    def __init__(self, project_name, base_url, domain_name, server_name, file_order):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.server_name = server_name
        Spider.queue_file = Spider.project_name + '/queue_url.txt'
        Spider.crawled_file = Spider.project_name + '/crawled_url.txt'
        Spider.file_order = file_order

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # static method means this method(function) does not belong to the class, so no relation with "self"
    @staticmethod
    def boot():
        creat_project_dir(Spider.project_name, Spider.project_name + '/json_file')
        creat_project_dir(Spider.project_name, Spider.project_name + '/text_file')

        create_url_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # multi-thread program, so need to display the url name to user
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print (thread_name + ' now crawling ' + page_url)
            print ('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url)) #
            Spider.queue.remove(page_url) # update the waiting queue
            Spider.crawled.add(page_url) # update the crawled list
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(quote(page_url.encode('utf-8'), safe=string.printable))
            # make sure you get the html data
            if response.info().gettype() == 'text/html':
                html_bytes = response.read() # html_byte is 01010101
                decode_type = chardet.detect(html_bytes)['encoding']
                html_string = html_bytes.decode(decode_type)
                Spider.concat_json(Spider.base_url, page_url, html_string)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print ('Error: can not crawl page! ' + str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def concat_json(base_url, page_url, text):
        url = urljoin(base_url, page_url)
        Spider.json_text['url'] = url
        Spider.json_text['content'] = text
        if len(Spider.crawled) > Spider.file_order:
            Spider.file_order = len(Spider.crawled)
        name = 'web' + str(Spider.file_order) + '.json'
        json_to_file(Spider.project_name, name, Spider.json_text)
        # print Spider.json_text

    @staticmethod
    def concat_text(text):
        if len(Spider.crawled) > Spider.file_order:
            Spider.file_order = len(Spider.crawled)
        name = 'web' + str(Spider.file_order) + '.html'
        text_to_file(Spider.project_name, name, text)

    @staticmethod
    # check whether already exists in waiting list and whether already in crawled list
    def add_links_to_queue(links):
        for url in links:
            url = del_version(url)
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.server_name != get_server_name(url):
                # check whether the url belong to my web, in case of google, facebook whatever
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        try:
            set_to_file(Spider.queue, Spider.queue_file)
            set_to_file(Spider.crawled, Spider.crawled_file)
        except Exception as e:
            print 'Error when updating files: ' + str(e)
