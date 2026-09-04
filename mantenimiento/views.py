from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from django.shortcuts import get_object_or_404, redirect
import pandas as pd
import pytz
import datetime

# Create your views here.

def index(request):
    return render(request, 'mantenimiento/login.html')