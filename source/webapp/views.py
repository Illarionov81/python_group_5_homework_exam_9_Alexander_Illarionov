from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Gallery


class PhotoView(ListView):
    template_name = 'photo/photos_view.html'
    context_object_name = 'gallery'
    model = Gallery
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 0


class OnePhotoView(DetailView):
    template_name = 'photo/photo_view.html'
    model = Gallery
    paginate_review_by = 5
    paginate_review_orphans = 0

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     gallery = Gallery.objects.get(pk=self.kwargs.get('pk'))
    #     print(gallery.favorites)
    #     context['user'] = gallery.favorites
    #     return context


class PhotoCreateView(CreateView):
    model = Gallery
    template_name = 'photo/photo_create.html'
    form_class = PhotoForm
    # permission_required = 'webapp.add_product'

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.author = self.request.user
        photo.save()
        return redirect('webapp:one_photo_view', pk=photo.pk)

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class PhotoUpdateView(UpdateView):
    template_name = 'photo/photo_update.html'
    form_class = PhotoForm
    model = Gallery
    # permission_required = 'webapp.change_article'

    def get_success_url(self):
        return reverse('webapp:one_photo_view', kwargs={'pk': self.object.pk})


# UserPassesTestMixin,
class PhotoDeleteView( DeleteView):
    template_name = 'photo/photo_delete.html'
    model = Gallery
    success_url = reverse_lazy('webapp:photos')

    # def test_func(self):
    #     return self.request.user.has_perm('webapp.delete_article') or \
    #         self.get_object().author == self.request.user
