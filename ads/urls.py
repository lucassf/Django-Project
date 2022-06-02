from django.urls import path, reverse_lazy

from . import views

app_name = 'ads'
urlpatterns = [
    path('', views.AdListView.as_view(), name='all'),
    path('ad/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/create', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/update', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete', views.AdDeleteView.as_view(), name='ad_delete'),
]
