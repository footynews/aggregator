
class WebCrawlException(Exception):
    def __init__(self, message, tag):
        self.message = message
        self.tag = tag


class AuthorNotFoundException(WebCrawlException):
    pass


class DatePublishedNotFoundException(WebCrawlException):
    pass


class TitleNotFoundException(WebCrawlException):
    pass


class UrlNotFoundException(WebCrawlException):
    pass
