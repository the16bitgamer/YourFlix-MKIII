import urllib3

def CheckPypi():
    return CheckFromURL('https://pypi.org')

def CheckGitHub():
    return CheckFromURL('http://github.com')

def CheckGoogle():
    return CheckFromURL('https://google.com')

def CheckFromURL(URL_STRING):
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', URL_STRING, timeout=1)
    except:
        return False
    return True