class Place(object):
    def __init__(self, path, title, audio=None, items=()):
        self.path = path
        self.title = title
        self.audio = audio
        self.items = items
