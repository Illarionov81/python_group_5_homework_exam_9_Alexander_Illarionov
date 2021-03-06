from django.contrib.auth import authenticate, login, logout

from webapp.models import Favorites, Gallery
from .forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView

from accounts.forms import MyUserCreationForm,  ProfileChangeForm
from django.views.generic import CreateView


# def login_view(request):
#     from_url = request.META.get('HTTP_REFERER', 'products')
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('projects')
#         else:
#             context['has_error'] = True
#     return render(request, 'registration/login.html', context=context)
#
# def logout_view(request):
#     from_url = request.META.get('HTTP_REFERER', 'products')
#     logout(request)
#     return redirect(from_url


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_project_by = 5
    paginate_project_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        favorites = Favorites.objects.filter(user=user.pk)
        print(favorites)
        context['gallery'] = favorites
        return context


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})





