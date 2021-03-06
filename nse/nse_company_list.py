import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import os
import warnings
import sqlite3


def get_csv_link():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,la;q=0.6",
        "Scheme": "https",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Authority": "www.nseindia.com",
        "Cache-Control": "max-age=0",
    }
    NSE_COMPANY_LIST_URL = "https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies"
    res = requests.get(
        NSE_COMPANY_LIST_URL,
        headers=headers,
    )
    res.raise_for_status()

    soup = bs4(res.content, features="lxml")
    divHolders = soup.find_all("div", {"class": "mt-3"})
    for div in divHolders:
        if div.find("a", {"data-entity-type": "file"}):
            element = div.find("a", {"data-entity-type": "file"})
            return element["href"]


def get_company_list():
    url = get_csv_link()
    if not url:
        return []
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,la;q=0.6",
        "Scheme": "https",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Authority": "www.nseindia.com",
        "Cache-Control": "max-age=0",
    }
    res = requests.get(
        url,
        headers=headers,
    )
    res.raise_for_status()
    with open("nse_company_list.xlsx", "wb") as f:
        f.write(res.content)
    xlsx_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "nse_company_list.xlsx"
    )
    if not os.path.exists(xlsx_path):
        warnings.warn("Cannot download file from NSE")
        return []
    df = pd.read_excel(xlsx_path)
    df = df[["Symbol", "Company Name"]]
    df = df.dropna()
    data = df.to_dict('records')
    return data


company_list = get_company_list()


#Adding the data to the db
conn=sqlite3.connect('companies.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS companies (exchange text,code text,company text)"
c.execute(create_table)
add_data_to_db="INSERT INTO companies VALUES (?,?,?)"

for company in company_list:
    c.execute(add_data_to_db,('NSE',company['Symbol'],company['Company Name']))

conn.commit()
conn.close()
