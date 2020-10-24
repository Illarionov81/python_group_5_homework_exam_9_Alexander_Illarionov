from django.urls import path

from webapp.views import PhotoView, OnePhotoView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView
from webapp.views import FavoritesAddView, FavoritesDeleteView

app_name = 'webapp'


urlpatterns = [
    path('', PhotoView.as_view(), name='photos'),
    path('photo/<int:pk>/', OnePhotoView.as_view(), name='one_photo_view'),
    path('photo/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('favorites/add/<int:pk>/', FavoritesAddView.as_view(), name='favorites_add'),
    path('favorites/delete/<int:pk>/', FavoritesDeleteView.as_view(), name='favorites_delete'),
]