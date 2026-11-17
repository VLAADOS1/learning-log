from django.urls import path

from . import views

app_name = "learning_logs"
urlpatterns = [
    path("", views.index, name="index"),
    path("topics/", views.topics, name="topics"),
    path("topics/new/", views.new_topic, name="new_topic"),
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    path("topics/<int:topic_id>/entries/new/", views.new_entry, name="new_entry"),
    path("entries/<int:entry_id>/edit/", views.edit_entry, name="edit_entry"),
]
