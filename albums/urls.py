from django.urls import path
from .views import (
    AlbumListView,
    AlbumDetailView,
    AlbumCreateView,
    AlbumUpdateView,
    AlbumDeleteView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    SignUpView,
)

urlpatterns = [
    path('albums/', AlbumListView.as_view(), name='album-list'),
    path('albums/create/', AlbumCreateView.as_view(), name='album-create'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('albums/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album-edit'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album-delete'),
    path('albums/<int:album_pk>/photos/add/', PhotoCreateView.as_view(), name='photo-add'),
    path('albums/<int:album_pk>/photos/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo-edit'),
    path('albums/<int:album_pk>/photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
