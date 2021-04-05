import requests
from bs4 import BeautifulSoup


def get_data_container(URL):
    jobs = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        data = soup.find("article").find_all("li")
        del data[-1]
        for i in data:
            jobs.append(extract_jobs(i))
    except:
        pass
    return jobs


def extract_jobs(i):
    company = i.find("span", {"class": "company"})
    title = i.find("span", {"class": "title"})
    link = i.select_one("li>a")
    img_url = i.find("div", {"class": "flag-logo"})
    if company:
        company = company.get_text()
    if title:
        title = title.get_text()
    if link:
        link = link.get("href")
        link = "https://weworkremotely.com"+link
    if img_url:
        img_url = img_url.get("style")
        img_url = img_url[21:-1]
    return {"title": title, "company": company, "url": link, "img_url": img_url}


def get_jobs(searching_by):
    we_work_URL1 = "https://weworkremotely.com"
    we_work_URL2 = f"/remote-jobs/search?utf8=%E2%9C%93&term={searching_by}"
    URL = we_work_URL1+we_work_URL2
    jobs = get_data_container(URL)
    return jobs
