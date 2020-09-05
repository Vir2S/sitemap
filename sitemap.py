import re


class Manager:

    def __init__(self, site_url):
        """
        :param site_url: protocol and domain name (https://domain.com)
        """
        self.site_url = site_url

    def site_process(self):
        pass


class Page:

    URL_PATTERN = re.compile(r'href="([%.\w/-]+)"')

    def __init__(self, path):

        self.links = []
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

