from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cats.models import Cat, Breed


class CatsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cats/cat_list.html', {
            'breed_count': Breed.objects.all().count(),
            'cat_list': Cat.objects.all()
        })


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')


class BreedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cats/breed_list.html', {
            'breed_list': Breed.objects.all()
        })


class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')


class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:cats_all')
