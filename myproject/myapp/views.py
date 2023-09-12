from django.shortcuts import render

# Create your views here.
import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np

def generate_graph(request):
    if request.method == 'POST':
           selected_team = request.POST.get('teams')
           selected_type = request.POST.get('type')
           selected_filter = request.POST.get('filter')

    teams = ['Detroit Red Wings', 'New York Rangers', 'New York Islanders', 'Chicago Blackhawks']
    types = ['schedule', 'data']
    filters = ['home only', 'away only', 'all']
    # Rest of your code here...
    # Make sure to indent the code properly

    return render(request, 'index.html', {'teams': teams, 'types': types, 'filters': filters})
