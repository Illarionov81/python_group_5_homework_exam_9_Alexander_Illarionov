from django.urls import path

from webapp.views import PhotoView, OnePhotoView, PhotoCreateView

app_name = 'webapp'


urlpatterns = [
    path('', PhotoView.as_view(), name='photos'),
    path('photo/<int:pk>/', OnePhotoView.as_view(), name='one_photo_view'),
    path('photo/create/', PhotoCreateView.as_view(), name='photo_create'),

]