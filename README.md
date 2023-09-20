# proxy-scraper-checker
A python software which scrapes proxies from a list of other sources and checks them.

# OS Supported
- Linux 
- Windows
- Mac 

# Features
- Proxy Scraping at a high speed (concurrent)
- Proxy Checking at a super speed (concurrent, multi-threaded)
- HTTP/s protocol (adding socks protocol soon)
- Region Filter USA/EUROPE/ALL
- Accurate proxy checking, try the good proxies at [CheckerProxy.net](https://checkerproxy.net)


# Sources 
- If you'd like to scrape more proxies to check more, you can directly just add the source links in `proxy_sources.txt`

# How to run
- Install [Python](https://python.org/) , pick latest , add to PATH (windows)
- Install all dependencies inside `requirements.txt` using pip/pip3 `pip install -r requirements.txt`
- Execute this command in shell inside the directory (Windows: `py main.py`) | (Linux: `python3 main.py`) | (macOS: `python3 main.py`)
