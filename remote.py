import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def get_data_container(URL):
    jobs = []
    try:
        result = requests.get(URL, headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        data = soup.find("table", {"id": "jobsboard"}).find_all(
            "tr", {"class": "job"})
        for i in data:
            jobs.append(extract_jobs(i))
    except:
        pass
    return jobs


def extract_jobs(i):
    title = i.find("h2", {"itemprop": "title"})
    if title:
        title = title.get_text()
    company = i.find("h3", {"itemprop": "name"})
    if company:
        company = company.get_text()
    url = i.find("a", {"itemprop": "url"})
    if url:
        url = url.get("href")
        url = "https://remoteok.io"+url
    img_url = i.find("img", {"class": "logo"})
    if img_url:
        try:
            img_url = img_url["src"]
        except:
            img_url = img_url["data-src"]

    return {"title": title, "company": company, "url": url, "img_url": img_url}


def get_jobs(searching_by):
    RJ_url1 = "https://remoteok.io"
    RJ_url2 = f"/remote-{searching_by}-jobs"
    URL = RJ_url1+RJ_url2
    jobs = get_data_container(URL)
    return jobs
