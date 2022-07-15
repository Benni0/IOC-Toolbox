import requests
import urllib.parse
import re

class UrlTracingException(Exception):
    def __init__(self, message: str):
        self.message = message

def trace_url(url):

    if re.search("^https://eur04\.safelinks\.protection\.outlook\.com\/?\?url=.*$", url):
        original_url = re.findall('url=(.*?)&', url)
        if len(original_url)==1:
            url = urllib.parse.unquote(original_url[0])
            print(f"new url: {url}")

    called_urls = []

    try:
        request_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        return [(url, 408)]
    except Exception as e:
        raise UrlTracingException(f"Error occured during web server access: {e}")

    if(re.search("https?://[^/]*safelinks.protection.outlook.com/.*", request_result.url)):
        match = re.findall('mark.*?(https?://[^\s<]+)', str(request_result.content))
        if(len(match) > 0):
            return trace_url(match[0])

    for result in request_result.history:
        called_urls.append((result.url, result.status_code))
    called_urls.append((request_result.url, request_result.status_code))
    return called_urls
