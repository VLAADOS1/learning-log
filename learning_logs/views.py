from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request):
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("-date_added", "-pk")
    return render(request, "learning_logs/topics.html", {"topics": topics})


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    entries = topic.entries.order_by("-date_added", "-pk")
    return render(request, "learning_logs/topic.html", {"topic": topic, "entries": entries})


@login_required
def new_topic(request):
    form = TopicForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.owner = request.user
        topic.save()
        return redirect("learning_logs:topics")
    return render(request, "learning_logs/form.html", {"form": form, "title": "Новая тема"})


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    form = EntryForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.topic = topic
        entry.save()
        return redirect("learning_logs:topic", topic_id=topic.pk)
    return render(request, "learning_logs/form.html", {
        "form": form, "topic": topic, "title": "Новая запись",
    })


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(
        Entry.objects.select_related("topic"), pk=entry_id, topic__owner=request.user
    )
    form = EntryForm(request.POST if request.method == "POST" else None, instance=entry)
    if form.is_valid():
        form.save()
        return redirect("learning_logs:topic", topic_id=entry.topic_id)
    return render(request, "learning_logs/form.html", {
        "form": form, "topic": entry.topic, "title": "Редактирование записи",
    })
