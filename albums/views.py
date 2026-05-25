from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, FormView

from .forms import AlbumForm, PhotoForm, SignUpForm
from .mixins import OwnerOrAdminMixin
from .models import Album, Photo


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AlbumListView(ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'
    paginate_by = 12


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['can_edit'] = self.object.can_edit(self.request.user)
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.object.pk})


class AlbumUpdateView(OwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(OwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=kwargs['album_pk'])
        if not self.album.can_edit(request.user):
            return redirect('album-detail', pk=self.album.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.album.pk})


class PhotoUpdateView(OwnerOrAdminMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.object.album.pk})


class PhotoDeleteView(OwnerOrAdminMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('album-detail')

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.object.album.pk})
