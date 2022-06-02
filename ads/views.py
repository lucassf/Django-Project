from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from ads.models import Ad
from ads.owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class AdListView(ListView):
    model = Ad
    context_object_name = 'ad_list'


class AdDetailView(DetailView):
    model = Ad
    context_object_name = 'ad'


class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    success_url = reverse_lazy('ads:all')


class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    success_url = reverse_lazy('ads:all')


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:all')
