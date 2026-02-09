import json
import os
from typing import Callable, List, Literal, Union
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pydantic import BaseModel
from requests.models import HTTPError
import itertools
import string

# USER CONSTS (can be changed)
COOKIE = "F1600A12F246AAE88B3F2EEB831AB3AB~000000000000000000000000000000~YAAQBk4SAikP9SGcAQAAzrRWQx4LLYQvRjGTc86VOK9y+L8DkMlre5P8ykd2HfktRiCfU1i4iyAIRuvEbfoDsQlAvUOa+FpGXvzOggGVxw+y6iNWIsz3d34L8vuSBCyTWkiOv8SzoDna1gUkXC8PZ4foiz+4H++9+Gh0h69GfFA925zvb7RksACTPQqVEfYzlPdXVrBY46dRCam86pN1nmNRk/WIe2KMSieUx1zm7LEuYaD02ZtIAG1PYtbUmVcd99vrTAVgPWtJu3IWaOkGRkv/d8Ni8/maIQtErpj0BX9R7qwUoV7h/pthJU+NXCA1b2g/ZnHljqw8QaOFXId38hlA47nFNRBqOpnD4ticX2nUMj4ylhtg+UnhPpM8B2ylbVzpXUvBjAXJfn1bYLmsDTQ3Pbq7Vohd1Mc3P1H6VJrc00fKSvBlqab1bAKCU46b/LWRccoXgUrjnBXJlpziHT85FbskLAiQhOIBxDHEnpByJHOtEm0yAZDW+ekqflQBH7v4"
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


# database
class RealFile(BaseModel):
    type: Literal["real"] = "real"
    extension: str
    size: int
    downloaded: bool = False


class Attempts(BaseModel):
    type: Literal["attempts"] = "attempts"
    extensions: List[str] = []


Progress = Union[RealFile, Attempts]


class File(BaseModel):
    dataset: str
    name: str
    url: str
    progress: Progress


def save_db(files: list[File]):
    db_path = Path("db.json")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in files], f, indent=2)


def load_db():
    db_path = Path("db.json")

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [File.model_validate(item) for item in data]


# search
def search_url(keys: str, page: int):
    return f"{SEARCH_URL}keys={keys}&page={page}"


def get_search(search: str, page: int):
    url = search_url(search, page)

    return requests.get(
        url=url,
        headers=SEARCH_HEADERS,
        cookies={"ak_bmsc": COOKIE},
    )


def search(term: str):
    search_key = term.replace(" ", "+")
    search_file = term.replace(" ", "_")

    pages = range(1, MAX_PAGES + 1)

    get_search_with_key = partial(get_search, search_key)

    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(get_search_with_key, page): page for page in pages}

        for future in as_completed(futures):
            page = futures[future]

            try:
                response = future.result()
            except Exception as e:
                print(f"PAGE {page} EXCEPTION {e}")
                continue

            file_path = Path(f"./search/{search_file}-page_{page}.json")

            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "wb") as sf:
                sf.write(response.content)

            print(f"PAGE {page}/{MAX_PAGES} DONE")


# parse search
def parse_search_results():
    search_dir = Path("./search")

    data = []
    for file_name in os.listdir(search_dir):
        path = os.path.join(search_dir, file_name)

        with open(path, "r", encoding="utf-8") as f:
            data.append(json.load(f))

    files = []
    for d in data:
        hits = d["hits"]["hits"]

        for hit in hits:
            source = hit["_source"]
            name: str = source["ORIGIN_FILE_NAME"]
            url: str = source["ORIGIN_FILE_URI"]
            key: str = source["key"]
            dataset = key.split("/")[0]

            file = File(
                dataset=dataset,
                name=name.removesuffix(".pdf"),
                url=url,
                progress=Attempts(),
            )
            files.append(file)

    return files


# file find/download
Fn = Callable[[int, File, str], bool]


def find_file(id: int, file: File, ext: str):
    uri = file.url.removesuffix(".pdf") + ext

    with requests.head(
        url=uri, headers=NORMAL_HEADERS, cookies=COOKIES, timeout=(3, 10)
    ) as resp:
        if resp.status_code == 404:
            if isinstance(file.progress, Attempts):
                file.progress.extensions.append(ext)
            print(f"{R}[{id}] NOK - {ext} not found{X}")
            return False

        resp.raise_for_status()

        total_size = int(resp.headers.get("Content-Length", 0))
        file.progress = RealFile(extension=ext, size=total_size)

        print(f"{G}[{id}] OK - found with ext: {ext}, size:{total_size:,}{X}")

    return True


def download_file(id: int, file: File, ext: str):
    file_name_new = file.name + ext
    download_path = Path(f"./videos/{file.dataset}/{file_name_new}")

    if download_path.exists():
        file_size = download_path.stat().st_size
        file.progress = RealFile(extension=ext, size=file_size, downloaded=True)
        print(f"{Y}[{id}] SKIP - file downloaded{X}")
        return True

    print(f"[{id}] Trying to find {ext} and download")

    uri = file.url.removesuffix(".pdf") + ext

    with requests.get(
        url=uri,
        headers=NORMAL_HEADERS,
        cookies=COOKIES,
        stream=True,
        timeout=(3, 10),
    ) as video:
        if video.status_code == 404:
            if isinstance(file.progress, Attempts):
                file.progress.extensions.append(ext)
            print(f"{R}[{id}] NOK - {ext} not found{X}")
            return False

        video.raise_for_status()

        total_size = int(video.headers.get("Content-Length", 0))
        file.progress = RealFile(extension=ext, size=total_size)

        if total_size > FILE_SIZE_LIMIT:
            print(f"{Y}[{id}] SKIP - too large: {total_size:,}B{X}")
            return True

        download_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"{G}[{id}] Downloading... {file_name_new} (size:{total_size}){X}")
        with open(download_path, "wb") as vf:
            for chunk in video.iter_content(1024 * 1024):
                if not chunk:
                    continue

                vf.write(chunk)

        file.progress.downloaded = True

        print(f"{G}[{id}] OK - dowloaded with ext: {ext}, size:{total_size:,}{X}")

    return True


def download_or_find_file(file: File, id: int, fn: Fn, ext: str) -> bool:
    if isinstance(file.progress, RealFile):
        file_extension = file.progress.extension
        # print(f"{Y}[{id}] SKIP - {file_extension} already found{X}")
        return True

    if ext in file.progress.extensions:
        # print(f"{Y}[{id}] SKIP - {ext} already tried{X}")
        return False

    try:
        return fn(id, file, ext)
    except HTTPError as e:
        if e.response.status_code == 403:
            print(f"{R}ACCESS DENIED - stopping{X}")
            raise Exception("ACCESS DENIED")

        print(f"{R}[{id}] EXCEPTION {e}{X}")
        return False


def generate_extensions(max_length=3):
    charset = string.ascii_lowercase + string.digits

    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield "." + "".join(combo)


all_extensions = list(generate_extensions(3))


def uncover_file(fn: Fn, id: int, file: File):
    # print(f"[{id}] Processing {file.dataset}/{file.name}")

    partial_download_or_find_file = partial(
        download_or_find_file, file=file, id=id, fn=fn
    )

    with ThreadPoolExecutor(max_workers=EXTENSION_THREADS) as pool:
        futures = [
            pool.submit(partial_download_or_find_file, ext=ext)
            for ext in all_extensions
        ]

        for future in as_completed(futures):
            found = future.result()
            if found:
                return id

    print(f"{R}[{id}] NOTHING FOUND{X}")

    return id


def uncover(files: List[File], download: bool):
    if download:
        fn = download_file
    else:
        fn = find_file

    uncover_file_with_fn = partial(uncover_file, fn)

    with ThreadPoolExecutor(max_workers=FILE_THREADS) as pool:
        futures = [
            pool.submit(uncover_file_with_fn, id, file) for id, file in enumerate(files)
        ]

        for future in as_completed(futures):
            _ = future.result()
            save_db(files)

    return files


# for fuck ups with code...
def reset_attempts(files: List[File]):
    for file in files:
        if isinstance(file.progress, Attempts):
            file.progress.extensions = []

    return files


def get_cookies():
    session = requests.session()

    resp = session.get(SITE_URL)

    cookies = session.cookies.get_dict()

    print(json.dumps(cookies, indent=4))


def main():
    # search("no images produced")
    # db = parse_search_results()
    # save_db(db)
    db = load_db()
    # db = reset_attempts(db)
    try:
        db = uncover(db, False)
    except:
        print("STOPPING AND SAVING DB")

    save_db(db)


if __name__ == "__main__":
    main()
