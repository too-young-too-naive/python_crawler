# parse URLs into components
from urlparse import urlparse

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

# Get sub domain name (mail.name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc #network location
    except:
        return ''


print(get_domain_name('http://email.example.thenewboston.com/index.php'))