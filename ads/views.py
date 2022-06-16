from django.views.generic import ListView, DetailView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from ads.models import Ad, Comment, Favorite
from ads.owner import OwnerDeleteView
from ads.forms import CreateForm, CommentForm


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ad_list'

    def get(self, request):
        ads = Ad.objects.all()
        favorites = []
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')
            favorites = [row['id'] for row in rows]
        return render(request, self.template_name, {
            self.context_object_name: ads,
            'favorites': favorites
        })


class AdDetailView(DetailView):
    template_name = 'ads/ad_detail.html'
    model = Ad
    context_object_name = 'ad'

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': ad, 'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        form.save_m2m()

        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()
        form.save_m2m()

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy('ads:all')


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(
            text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        fav = Favorite(user=request.user, ad=ad)
        try:
            fav.save()
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        ad = get_object_or_404(Ad, id=pk)
        try:
            Favorite.objects.get(user=request.user, ad=ad).delete()
        except Favorite.DoesNotExist:
            pass
        return HttpResponse()
