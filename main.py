import threading
import Queue
import time
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
FILE_ORDER = 0
QUEUE_FILE = PROJECT_NAME + '/queue_url.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled_url.txt'
NUMBER_OF_THREADS = 1
CRAWLED_DEPTH = 2
queue = Queue.Queue() #pay attention
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, FILE_ORDER)

# Create worker threads (will die when main exists)
def create_workers():
    # create 8 or 2 threads
    for x in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work) #target is ?
        t.daemon = True
        t.start()
    # raw_input('Press enter to kill thread')


# Do the next job in the queue
def work():
    while True:
        time.sleep(1)
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()



# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print (str(len(queued_links)) + ' links in the queue')
        create_jobs()

def main():
    create_workers()
    crawl()

if __name__ == '__main__':
    # execute only if run as a script
    main()