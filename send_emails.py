import os
import sys
import datetime

import django

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()

from scraping.models import Vacancy, Error, Url, City, Language
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
empty = '<h2> Сегодня новых вакансий нет </h2>'
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий за {today}'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

for q in qs:
    users_dct.setdefault((q['city'], q['language']), [])
    users_dct[(q['city'], q['language'])].append(q['email'])

if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for city, language in users_dct.keys():
        params['city_id__in'].append(city)
        params['language_id__in'].append(language)
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for q in qs:
        vacancies.setdefault((q['city_id'], q['language_id']), [])
        vacancies[(q['city_id'], q['language_id'])].append(q)
    for key, emails in users_dct.items():
        rows = vacancies.get(key, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["company"]}</p>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["requirement"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = f'{today} '
text_content = f'{today} '
to = ADMIN_USER
html = ''
if qs.exists():
    errors = qs.first()
    data = errors.data
    for dct in data:
        html += f'<p><a href="{dct["url"]}">Error: {dct["title"]}</a></p>'
    subject += f'Scraping errors '
    text_content += f'Scraping errors '

qs = Url.objects.all().values('city', 'language')
urls_dct = {(q['city'], q['language']): True for q in qs}
url_errors = ''
for key in users_dct.keys():
    if key not in urls_dct:
        name = City.objects.filter(id=key[0]).first().name
        language = Language.objects.filter(id=key[1]).first().name
        url_errors += f'<p>Отсутсвует URL для города {name} и языка {language}</p>'
if url_errors:
    subject += 'Missing urls'
    text_content += 'Missing urls'
    html += url_errors

if html:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()
