
class WebCrawlException(Exception):
    pass

class AuthorNotFoundException(WebCrawlException):
    pass

class DatePublishedNotFoundException(WebCrawlException):
    pass

class TitleNotFoundException(WebCrawlException):
    pass

class UrlNotFoundException(WebCrawlException):
    pass
