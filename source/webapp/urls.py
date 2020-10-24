from django.urls import path

from webapp.views import PhotoView, OnePhotoView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView

app_name = 'webapp'


urlpatterns = [
    path('', PhotoView.as_view(), name='photos'),
    path('photo/<int:pk>/', OnePhotoView.as_view(), name='one_photo_view'),
    path('photo/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),

]