from random import randint

import requests
import codecs

from bs4 import BeautifulSoup as BS

headers = [{'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"},
           {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"},
           {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}]


def work(url, city, language):
    resp = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='a11y-main-content')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
            for div in div_list:
                title = div.find('h3')
                title_url = title.a['href']
                try:
                    description = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                except AttributeError:
                    description = ''
                try:
                    requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                except AttributeError:
                    requirement = ''
                company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                jobs.append({'title': title.text,
                             'url': title_url,
                             'description': description,
                             'requirement': requirement,
                             'company': company,
                             'city_id': city,
                             'language_id': language,
                             })
        else:
            errors.append({'url': url, 'title': 'Div does not exist'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    h = codecs.open('../work.txt', 'w', 'utf-8')
    # h.write(str(jobs))
    h.close()
