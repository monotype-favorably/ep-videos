from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import itertools
import string

import requests

from src.consts import *

URL = "https://www.justice.gov/epstein/files/DataSet 9/EFTA00899090"


def generate_extensions(max_length=3):
    charset = string.ascii_lowercase + string.digits

    start = False
    for length in range(3, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            extension = "." + "".join(combo)
            if start:
                yield extension
            elif extension == ".e1a":
                start = True


GEN_EXTENSIONS = list(generate_extensions(3))

COMMON_EXTENSIONS = [
    ".doc",
    ".txt",
    ".docx",
    ".ppt",
    ".pptx",
    ".log",
    ".zip",
    ".tar",
    ".xml",
    ".swf",
]


def try_extension(url: str, ext: str):
    url = url + ext

    with requests.head(
        url=url, headers=NORMAL_HEADERS, cookies=COOKIES, timeout=(3, 10)
    ) as resp:
        if resp.status_code == 404:
            if resp.headers["server"] == "AkamaiNetStorage":
                print(f"{R}NOK - {ext} not found{X}")
                return False
            print(f"{R}ACCESS DENIED{X}")
            raise Exception("FUCK")
        if resp.status_code == 401:
            print(f"UNAUTHORIZED")
            raise Exception("FUCK")

        resp.raise_for_status()

        total_size = int(resp.headers.get("Content-Length", 0))

        print(f"{G}OK - found with ext: {ext}, size:{total_size:,}{X}")
        return True


def try_all_extensions(url: str):
    print(f"Processing {url}")

    partial_try_extension = partial(try_extension, url=url)

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(partial_try_extension, ext=ext) for ext in GEN_EXTENSIONS
        ]

        try:
            for future in as_completed(futures):
                found = future.result()
                if found:
                    pool.shutdown(wait=False, cancel_futures=True)
                    return id
        except Exception as e:
            print(f"huh? {e}")
            pool.shutdown(wait=False, cancel_futures=True)

    print(f"{R}NOTHING FOUND{X}")


def main():
    try_all_extensions(URL)


if __name__ == "__main__":
    main()
