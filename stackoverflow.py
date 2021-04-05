import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find(
        "h3", {"class": "mb4"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)

    job_id = html['data-jobid']
    img_url = html.find("div", {"class": "grid--cell"}).find("img")
    if img_url:
        img_url = img_url.get("src")

    return{'title': title, 'company': company,
           "url": f"https://stackoverflow.com/jobs/{job_id}", "img_url": img_url}


def extract_jobs(last_page, URL):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(URL)
    jobs = extract_jobs(last_page, URL)
    return jobs
