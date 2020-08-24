from django.urls import path
from . import views

app_name = 'muay'

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("intro", views.intro),
    path('forum', views.forum),
    path('drills', views.drills),
    path('warm_up', views.warm_up),
    path('media', views.media),
    path('process_message', views.post_mess),
    path('add_comment/<int:id>', views.post_comment),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('edit/<int:id>', views.edit),
    path("logout", views.logout)
]