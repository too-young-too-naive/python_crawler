import threading
import Queue
import time
from spider import Spider
from domain import *
from general import *
from config import *

QUEUE_FILE = PROJECT_NAME + '/queue_url.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled_url.txt'
queue = Queue.Queue()  # pay attention
domain_name = get_domain_name(HOMEPAGE)


# Create worker threads (will die when main exists)
def create_workers():
    # create threads
    for x in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
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
    Spider(PROJECT_NAME, HOMEPAGE, domain_name, FILE_ORDER)
    create_workers()
    crawl()


if __name__ == '__main__':
    # execute only if run as a script
    main()