from pathlib import Path

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
import ssl

# Use system SSL certs
class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        kwargs['ssl_context'] = context
        context.load_default_certs() # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)


if __name__ == "__main__":
    soup = BeautifulSoup(requests.get("http://opendata.rijksbegroting.nl/", allow_redirects=True).text, "lxml")

    dir_out = Path("opendata-rijksbegroting-excels")
    if not dir_out.exists():
        dir_out.mkdir()

    excels = []
    for a in soup("a"):
        if a.string == "Excel":
            target = a["href"]
            fname = target.split("/")[-1]
            s = requests.Session()
            s.mount(target, SSLContextAdapter())
            excel = s.get(target)
            print(fname)
            with (dir_out / fname).open("wb") as f:
                f.write(excel.content)
