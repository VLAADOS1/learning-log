from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.user.is_authenticated:
        return redirect("learning_logs:topics")
    form = UserCreationForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        login(request, form.save())
        return redirect("learning_logs:topics")
    return render(request, "learning_logs/form.html", {
        "form": form, "title": "Регистрация", "submit": "Создать аккаунт",
    })
