from django.views.generic import TemplateView
from fitnessApp.models import *
from fitnessApp.forms import *

class ExploreView(TemplateView):
    template_name = "explore.html"