from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import itertools
import json
import string

import requests

from src.consts import *

URL = "https://www.justice.gov/epstein/files/DataSet 8/EFTA00016339"


def generate_extensions(max_length=3):
    charset = string.ascii_lowercase + string.digits

    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield "." + "".join(combo)


all_extensions = list(generate_extensions(3))


def try_extension(url: str, ext: str):
    url = url + ext

    with requests.head(
        url=url, headers=NORMAL_HEADERS, cookies=COOKIES, timeout=(3, 10)
    ) as resp:
        print(resp.request.url)
        print(resp.status_code)
        print(json.dumps(dict(resp.headers), indent=4))
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

    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = [
            pool.submit(partial_try_extension, ext=ext) for ext in all_extensions
        ]

        for future in as_completed(futures):
            found = future.result()
            if found:
                return id

    print(f"{R}NOTHING FOUND{X}")


def main():
    try_all_extensions(URL)


if __name__ == "__main__":
    main()
