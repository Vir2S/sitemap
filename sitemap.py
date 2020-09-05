import re
import requests


def download_page_body(url):
    response = requests(url)
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

    def __init__(self, site_url, path):

        self.links = []
        self.site_url = site_url
        self.name = path
        self.title = ''
        self.body = ''
        self.is_visited = False

    def __str__(self):
        return f'Page {self.name} has {len(self.links)}. Visited: {self.is_visited}'

    def get_page_links(self):

        result = re.findall(self.URL_PATTERN, self.body)

        if not result:
            print(f'No links found on the page {self.name}')

        else:
            print(f'Found {len(result)} on the page {self.name}')
            self.links = result

    def get_page_body(self):
        pass