# USER CONSTS (can be changed)
COOKIE = "501CC0448552275008680E21D632D131~000000000000000000000000000000~YAAQzbMUAhc0gx6cAQAABsP3Qx4LRILvuIPgTki4apFLP9rU0KMgB4LQVRydbxnYXxTjbH/1OjG31sNO6bhrtUN1CeR98UH7TNAMsytsWms4VRVNzR2g3tKqgoEaXN/YZWb7nXXUad6nBU328wkFuNQ2bBSgz8ZgkYVTycxDrbFewFm0AO5tBKED7uESgfxHw33Zt2bXqSyrGL7mYbJeQ6qS5TIvzK+WUOxfijbpisFNXcdpKl5OZt5PsD/+KOPL/SnOO1SE6QgTuO6BIxoEcXRGhDauHn0BXkvCOxjc+tYMdobLMbT11+TZxAaXIysrpelXi8l+GnDzQ8W+DnoROnzTXG3O4fwomCOA+Opbv+P0ZMRup/16IWtawO3t42OrlCI73b3yHufZ+DfCjgJauQYEQZVePDkqslTMysW8vNbjRQG/Y0uKOPA+3oMFPljwZF/AOY8FrkOu/4pS3oC1UT2p1GLIvhg="
AUTH_1 = "A879935CDA7DD9EA9709330639827956DDE3CB176F9D15D762E2D9F5D95737F7"
AUTH_2 = "FB0079B45F0C237358D0C81D33615F3E272D185542968441A624CAFA35CA93B6"
FILE_SIZE_LIMIT = 200_000_000
EXTENSIONS = [
    ".mp4",
    ".mov",
    ".m4v",
    ".vob",
    ".wmv",
    ".avi",
    ".ts",
    ".opus",
    ".mp3",
    ".m4a",
    ".wav",
    ".xlsx",
    ".xls",
    ".3gp",
    ".amr",
    # ".flv",
    # ".amv",
    # ".qt",
    # ".ogg",
    # ".drc",
    # ".viv",
    # ".f4v",
    # ".webm",
    # ".mkv",
    # ".ogv",
    # ".gifv",
    # ".rm",
    # ".rmvb",
    # ".asf",
    # ".mpg",
    # ".mpeg",
    # ".dat",
    # ".asf",
    # ".ogm",
    # ".m2ts",
    # ".divx",
    # ".f4a",
    # ".m4p",
    # ".f4p",
    # ".aac",
    # ".aiff",
    # ".alac",
    # ".flac",
    # ".mp1",
    # ".mp2",
    # ".wma",
    # ".raw",
    # ".ra",
    # ".vox",
    # ".dss",
]
FILE_THREADS = 1
EXTENSION_THREADS = 10


# SITE CONSTS (should probably not be changed)
SITE_URL = "https://www.justice.gov/epstein"
SEARCH_URL = "https://www.justice.gov/multimedia-search?"
MAX_PAGES = 381  # might change in future?
NORMAL_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Alt-Used": "www.justice.gov",
    "Connection": "keep-alive",
    "Host": "www.justice.gov",
    # "If-Modified-Since": "Fri, 06 Feb 2026 01:20:33 GMT",
    # "If-None-Match": "\"1770340833-gzip\"",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?!",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
}
SEARCH_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Alt-Used": "www.justice.gov",
    "Connection": "keep-alive",
    "Host": "www.justice.gov",
    "Priority": "u=0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "x-queueit-ajaxpageurl": "https%3A%2F%2Fwww.justice.gov%2Fepstein",
}
COOKIES = {
    "ak_bmsc": COOKIE,
    "justiceGovAgeVerified": "true",
    # "authorization_1": AUTH_1,
    # "authorization_2": AUTH_2,
}

R = "\033[31m"
Y = "\033[33m"
G = "\033[32m"
X = "\033[0m"
