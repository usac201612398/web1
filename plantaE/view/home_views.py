from django.shortcuts import render

def plantaEhomepage(request):
    return render(request,'plantaE/home/plantaE_home.html')

def plantaEhomepageger(request):
    return render(request,'plantaE/home/plantaE_homeGerencial.html')
