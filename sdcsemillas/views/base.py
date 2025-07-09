# views/base.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class BaseListView(ListView):
    template_name = 'list.html'

class BaseCreateView(CreateView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')  # cambiar luego

class BaseUpdateView(UpdateView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')

class BaseDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('home')