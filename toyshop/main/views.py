from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from utils.ChartsCreator import ChartsCreator


def welcome_page(request):
    return render(request, 'main/welcome_page.html')


class Statistics(TemplateView):
    template_name = 'main/statistics.html'
    ChartsCreator()
