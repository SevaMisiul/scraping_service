import requests
import codecs

from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           }

url = 'https://rabota.by/vacancies/programmist_python?hhtmFromLabel=rainbow_profession&hhtmFrom=main'
resp = requests.get(url, headers=headers)
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
            description = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
            jobs.append({'title': title.text,
                         'url': title_url,
                         'description': description,
                         'requirement': requirement,
                         'company': company
                         })
    else:
        errors.append({'url': url, 'title': 'Div does not exist'})
else:
    errors.append({'url': url, 'title': 'Page do not response'})

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
