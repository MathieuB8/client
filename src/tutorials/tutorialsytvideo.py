from PyQt5.QtCore import QUrl
class TutorialsVideo():
    link=None
    description=''

    def __init__(self,link,description):
        self.link=QUrl(link)
        self.description=description
