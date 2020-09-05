import re
import requests


def download_page_body(url):

    try:
        response = requests(url)

    except Exception as e:
        print(f'Error {e}')
        return ''

    return response.text


class Manager:

    def __init__(self, protocol, domain_name):
        """
        :param protocol: protocol (http or https)
        :param domain_name: domain name (domain.com)
        """
        self.protocol = protocol
        self.domain_name = domain_name

    def site_process(self):
        site_url = f'{self.protocol}://{self.domain_name}'  # https://domain.com


class Page:

    URL_PATTERN = re.compile(r'href="([%.\w/-]+)"')
    TITLE_PATTERN = re.compile('<title>([\w\s-]+)</title>')

    def __init__(self, site_url, path):

        self.__site_url = site_url  # https://domain.com
        self.___path = path  # /path/to/page.html
        self.__body = ''

        self.page_url = f'{site_url}/{path}'  # https://domain.com/path/to/page.html
        self.links = []
        self.title = ''
        self.is_visited = False

    def __str__(self):
        return f'Page {self.name} has {len(self.links)}. Visited: {self.is_visited}'

    def __get_page_links(self):

        if not self.__body:
            print(f'Body page {self.___path} is empty. Will not process')
            return

        result = re.findall(self.URL_PATTERN, self.__body)

        if not result:
            print(f'No links found on page {self.name}')

        else:
            print(f'Found {len(result)} on page {self.name}')
            self.links = result

    def __get_page_body(self):

        self.__body = download_page_body(self.page_url)

    def __get_page_title(self):

        if not self.__body:
            print(f'Body page {self.___path} is empty. Will not process')
            return

        result = re.findall(self.TITLE_PATTERN, self.__body)

        if result:
            self.title = result[0]
            print(f'Page {self.___path} have a title {self.title}')
            return

        else:
            print(f'Page {self.___path} have no title')

    def process(self):

        self.__get_page_body()
        self.__get_page_title()
        self.__get_page_links()
