from django.shortcuts import render

# Create your views here.
import requests
import pandas
import matplotlib.pyplot as plt
import numpy as np


def click_submit(request):
    if request.method == 'POST':
           selected_team = request.POST.get('teams')
           selected_type = request.POST.get('type')
           selected_filter = request.POST.get('filter')
    import sqlite3

    # Connect to the hockey_data database
    conn = sqlite3.connect('myproject/hockey_data.sqlite3')
    cursor = conn.cursor()

    # Retrieve all team names from the nhl_team table
    cursor.execute("SELECT name FROM nhl_team")
    teams = [row[0] for row in cursor.fetchall()]
    teams.sort()

    # Close the database connection
    cursor.close()
    conn.close()
    
    types = ['schedule', 'data']
    filters = ['home only', 'away only', 'all']
    # Rest of your code here...
    # Make sure to indent the code properly

    return render(request, 'index.html', {'teams': teams, 'types': types, 'filters': filters})
