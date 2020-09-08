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

    def __init__(self, page_url):

        self.__body = ''

        self.page_url = page_url
        self.links = []
        self.title = ''
        self.is_visited = False

    def __str__(self):
        return f'Page {self.page_url} has {len(self.links)} links. Visited: {self.is_visited}'

    def __get_page_links(self):

        if not self.__body:
            print(f'Body page {self.page_url} is empty. Will not process')
            return

        result = re.findall(self.URL_PATTERN, self.__body)

        if not result:
            print(f'No links found on page {self.page_url}')

        else:
            print(f'On page {self.page_url} found {len(result)} links.')
            self.links = [Link(el[0]) for el in result if not el[0].startswith('mailto')]

    def __get_page_body(self):

        self.__body = download_page_body(self.page_url)

    def __get_page_title(self):

        if not self.__body:
            print(f'Body page {self.page_url} is empty. Will not process')
            return

        result = re.findall(self.TITLE_PATTERN, self.__body)

        if result:
            self.title = result[0]
            print(f'Page {self.page_url} has a title {self.title}')
            return

        else:
            print(f'Page {self.page_url} has no title')

    def process(self):

        self.__get_page_body()
        self.__get_page_title()
        self.__get_page_links()

    def get_links_urls(self):
        return tuple(link.url for link in self.links)

    def get_links_to_be_followed(self):
        return set(link for link in self.links if link.should_follow())


class Link:

    def __init__(self, url):

        self.url = url
        self.is_followed = False
        self.__domain_name = f'{url.split("//")[1].split("/")[0]}'

    def __is_page(self):

        # Page is url ends with .html or without extension

        for ext in ('.css', 'js', '.png', '.svg', '.jpg', '.jpeg', '.gif', '.pdf'):

            if self.url.endswith(ext):
                return False

        if '/' not in self.url:
            return False

        return True

    def __is_internal_page(self):
        return True if self.__domain_name in self.url else False

    def should_follow(self):

        # Which links do we need to follow:
        # Page should not be visited
        # Links with *.domain.com, domain.com which ends with .html or without any extension

        if self.is_followed or not self.__is_page():
            return False

        if not self.__is_internal_page():
            return False

        return True


class Task:

    def __init__(self, site_url):

        self.site_url = site_url

        self.sitemap = {
            site_url: {}
        }

    def site_process(self):

        root_page = Page(self.site_url)  # https://domain.com
        root_page.process()

        root_page_links = root_page.links

        for link in root_page_links:
            self.sitemap[link] = {}

        root_page_links_to_be_followed = root_page.get_links_to_be_followed()


#############################################################


# manager = Manager()
# manager.add_site_to_be_parsed('https://dev.by/')
# manager.add_site_to_be_parsed('https://tut.by/')
# manager.add_sites_to_be_parsed('https://tut.by/', 'https://dev.by/')

task = Task('https://dev.by')
task.site_process()