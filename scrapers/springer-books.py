import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_links(fname):
    with open(fname) as f:
        for line in f:
            yield line


def soup_select(soup):
    def select(css):
        return soup.select(css)[0]
    return select


if __name__ == "__main__":
    dir_out = Path.cwd() / "boeken"
    if not dir_out.is_dir():
        dir_out.mkdir()

    for n, url in enumerate(get_links("boeken.txt")):
        try:
            soup = BeautifulSoup(requests.get(url, allow_redirects=True).text, "lxml")
            select_one = soup_select(soup)
            title = select_one(".page-title > h1:nth-child(1)").text
            if not Path(dir_out / f"{title.replace(' ', '_')}.pdf").exists():
                print(f"{n}. {title}")
                try:
                    link = select_one(".cta-button-container__item > div:nth-child(1) > a:nth-child(1)")["href"]
                except IndexError:
                    link = select_one("div.cta-button-container:nth-child(2) > div:nth-child(1) > a:nth-child(1)")["href"]
                book = requests.get(f"https://link.springer.com/{link}", allow_redirects=True)
                with open(Path(f"boeken/{title.replace(' ', '_')}.pdf"), "wb") as f:
                    f.write(book.content)
        except Exception as e:
            print(f"{e.__class__.__name__}: {url}")
            prob_file = Path("problematic_urls.txt")
            if not prob_file.exists():
                prob_file.touch()
            with prob_file.open("r+") as f:
                line = f"{n}, {title}, {url.strip()}, {e.__class__.__name__}\n"
                if line not in f.read():
                    f.write(line)
            continue
