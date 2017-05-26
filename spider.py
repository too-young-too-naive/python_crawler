from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

class Spider:

    # Class variables (are shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()


    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.crawled_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # static method means this method(function) does not belong to the class, so no relation with "self"
    @staticmethod
    def boot():
        creat_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    #multithread program, so need to display the url name to user
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print (thread_name + 'now crawling ' + page_url)
            print ('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_link(page_url)) #
            Spider.queue.remove(page_url) # update the waiting queue
            Spider.crawled.add(page_url) # update the crawled list
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            # make sure you get the html data
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read() # html_byte is 01010101
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print ('Error: can not crawl page!')
            return set()
        return finder.page_links()

    @staticmethod
    # check whether already exists in waiting list and whether already in crawled list
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                # check whether the url belong to my web, in case of google, facebook
                continue
            Spider.queue.add(url)

    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)