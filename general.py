import os

# Each website you crawl is a separate project (folder)
def creat_project_dir(directory1, directory2):
    if not os.path.exists(directory1):
        print ('Create directory ' + directory1)
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        print ('Create directory ' + directory2)
        os.makedirs(directory2)

# Create queue and crawled files (if not created)
def create_url_files(project_name, base_url):
    queue = project_name + '/queue_url.txt'
    crawled = project_name + '/crawled_url.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file: #a means write at the end of the file
        file.write(data + '\n')

# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass
        # Do nothing

# Read a file and convert each line to a set item
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item item will be a new line in the file
def set_to_file(links, file_name):
    with open(file_name, 'w') as f:
        for link in sorted(links):
            f.write(link + '\n')

def json_to_file(project_name, file_name, text):
    path = project_name + '/json_file/' + file_name
    with open(path, 'w+') as f:
        f.write(text + '\n')