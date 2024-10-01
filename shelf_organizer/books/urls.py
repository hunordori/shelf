from django.urls import path
from . import views

urlpatterns = [
    path('reorder/', views.reorder_books, name='reorder_books'),
]
