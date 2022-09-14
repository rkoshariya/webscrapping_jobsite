import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def extract(link):
    from urllib.request import Request, urlopen
    url=link
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage,'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_='card-apply-content')
    for item in divs:
        title = item.find('div', class_ = 'job-tittle')
        job_title = title.find('a').text.strip()
        title_list.append(job_title)
        company = title.find('span',class_='company-name').text.strip()
        company_list.append(company)
        search_tag = title.find('div',class_ = 'searctag row')
        experience = search_tag.find('div', class_='exp col-xxs-12 col-sm-3 text-ellipsis').text.strip()
        experience_list.append(experience)
        try:
            salary = search_tag.find('div', class_ ='package col-xxs-12 col-sm-4 text-ellipsis hidden-sm').text.strip()
        except:
            salary = 'not specified'
        salary_list.append(salary)
        description_link_tag = title.find('h3', class_='medium')
        description_link = description_link_tag.a['href']
        bs = extract(description_link)
        try:
            job_description = bs.find('div', class_='jd-text').text.strip()
        except:
            job_description = 'job description is not available for this job'
        description_list.append(job_description)
    return

title_list = []
company_list = []
experience_list = []
salary_list = []
description_list = []
skills = ['accounting-jobs','analytics-jobs','animation-jobs','architecture-jobs','banking-jobs','java-jobs','data-science-jobs','marketing-jobs','networking-jobs','online-marketing-jobs','online-marketing-jobs']

for skill in skills:
    title_list.clear()
    company_list.clear()
    experience_list.clear()
    salary_list.clear()
    description_list.clear()
    c =extract(f'https://www.monsterindia.com/search/{skill}')
    transform(c)
    i = 0
    for i in range(2,11):
        c =extract(f'https://www.monsterindia.com/search/{skill}-{i}')
        transform(c)

    header = ["SN","Title", "Company", "Experience","Salary","Description"]
    x = 0

    with open(f"{skill}.csv", 'w',encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        while x < len(title_list):
            writer.writerow([x,title_list[x],company_list[x],experience_list[x],salary_list[x],description_list[x]])
            x += 1