import re
import json
import urllib
import requests


def download_page_body(url):

    try:
        response = requests.get(url)

    except Exception as e:
        print(f'Error {e}')
        return ''

    return response.text


class Manager:
    def __init__(self):
        pass

    def add_site_to_be_parsed(self, site_root_url):
        pass

    def add_sites_to_be_parsed(self, *sites_root_urls):
        pass


class Page:

    URL_PATTERN = re.compile(r'="((\bhttp\b|\bftp\b|\bhttps|\bftps\b|)?(:\/\/)?[\w@:%,._\+\-~#=/]*\.[\w@:%,_\+\-.~#?&//=]*)')
    TITLE_PATTERN = re.compile('<title>([\w\s-]+)</title>')

    def __init__(self, site_url, path=''):

        self.__site_url = site_url  # https://domain.com
        self.___path = path  # /path/to/page.html
        self.__body = ''

        self.page_url = urllib.parse.urljoin(site_url, path)  # https://domain.com/path/to/page.html
        self.links = []
        self.title = ''
        self.is_visited = False

    def __str__(self):
        return f'Page {self.___path} has {len(self.links)} links. Visited: {self.is_visited}'

    def __get_page_links(self):

        if not self.__body:
            print(f'Body page {self.___path} is empty. Will not process')
            return

        result = re.findall(self.URL_PATTERN, self.__body)

        if not result:
            print(f'No links found on page {self.___path}')

        else:
            print(f'On page {self.___path} found {len(result)} links.')
            self.links = [Link(el[0]) for el in result if not el[0].startswith('mailto')]

    def __get_page_body(self):

        self.__body = download_page_body(self.page_url)

    def __get_page_title(self):

        if not self.__body:
            print(f'Body page {self.___path} is empty. Will not process')
            return

        result = re.findall(self.TITLE_PATTERN, self.__body)

        if result:
            self.title = result[0]
            print(f'Page {self.___path} has a title {self.title}')
            return

        else:
            print(f'Page {self.___path} has no title')

    def process(self):

        self.__get_page_body()
        self.__get_page_title()
        self.__get_page_links()

    def get_links_urls(self):
        return tuple(link.url for link in self.links)


class Link:

    def __init__(self, url):

        self.url = url
        self.is_followed = False

    def __is_page(self):

        # Page is url ends with .html or without extension

        for ext in ('.css', 'js', '.png', '.svg', '.jpg', '.jpeg', '.gif', '.pdf'):

            if self.url.endswith(ext):
                return False

            return True

    def should_follow(self):

        # Which links do we need to follow:
        # Page should not be visited
        # Links with *.domain.com, domain.com which ends with .html or without any extension

        if self.is_followed:
            return False

        if 'dev.by/' in self.url and self.url.endswith('.html'):
            return True


class Task:

    def __init__(self, protocol, domain_name):
        """
        :param protocol: protocol (http or https)
        :param domain_name: domain name (domain.com)
        """
        self.protocol = protocol
        self.domain_name = domain_name

    def site_process(self):

        site_root_url = f'{self.protocol}://{self.domain_name}'  # https://domain.com

        root_page = Page(site_root_url)
        root_page.process()

        root_page_links = root_page.links

        root_page_links_urls = root_page.get_links_urls()

        print(root_page_links_urls)


#############################################################


# manager = Manager()
# manager.add_site_to_be_parsed('https://dev.by/')
# manager.add_site_to_be_parsed('https://tut.by/')
# manager.add_sites_to_be_parsed('https://tut.by/', 'https://dev.by/')

task = Task('https', 'dev.by')
task.site_process()