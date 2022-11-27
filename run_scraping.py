import datetime
import os
import sys

import django

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from scraping.parser import work

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
django.setup()

from scraping.models import City, Language, Vacancy, Url, Error

User = get_user_model()


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dct[pair]}
            urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)

jobs, errors = [], []

for data in url_list:
    j, e = work(data['url_data']['rabota'], city=data['city'], language=data['language'])
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        err.data['errors'] = errors
        err.save()
    else:
        Error(data={'errors': errors}).save()
