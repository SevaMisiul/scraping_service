from datetime import datetime

from django.shortcuts import render


def home(request):
    date = datetime.now().date()
    name = 'Seva'
    context = {
        'date': date,
        'name': name
    }
    return render(request, 'base.html', context)
