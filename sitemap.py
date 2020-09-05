class Page:

    def __init__(self, path):
        self.links = []
        self.name = path
        self.title = ''
        self.body = ''
        self.is_visited = False

    def __str__(self):
        return f'Page {self.name} has {len(self.links)}. Visited: {self.is_visited}'

    def get_page_links(self):
        pass
