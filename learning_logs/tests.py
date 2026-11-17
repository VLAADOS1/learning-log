from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Topic


class JournalTests(TestCase):
    def test_registration_and_journal_workflow(self):
        credentials = {"username": "student", "password": "Learn!More5467"}
        response = self.client.post(reverse("users:register"), {
            "username": credentials["username"],
            "password1": credentials["password"],
            "password2": credentials["password"],
        })
        self.assertRedirects(response, reverse("learning_logs:topics"))
        self.assertRedirects(
            self.client.post(reverse("learning_logs:new_topic"), {"text": "Python"}),
            reverse("learning_logs:topics"),
        )
        topic = Topic.objects.get(text="Python")
        self.assertEqual(topic.owner.username, credentials["username"])
        detail = reverse("learning_logs:topic", args=[topic.pk])
        self.assertRedirects(self.client.post(
            reverse("learning_logs:new_entry", args=[topic.pk]), {"text": "Первая запись"}
        ), detail)
        entry = topic.entries.get()
        self.assertRedirects(self.client.post(
            reverse("learning_logs:edit_entry", args=[entry.pk]), {"text": "Новый текст"}
        ), detail)
        self.assertContains(self.client.get(detail), "Новый текст")
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)
        self.assertRedirects(
            self.client.post(reverse("users:logout")), reverse("learning_logs:index")
        )
        self.assertEqual(self.client.get(detail).status_code, 302)
        self.assertRedirects(
            self.client.post(reverse("users:login"), credentials),
            reverse("learning_logs:topics"),
        )

    def test_other_users_cannot_read_or_write_private_entries(self):
        users = get_user_model().objects
        owner = users.create_user(username="owner")
        visitor = users.create_user(username="visitor")
        topic = Topic.objects.create(owner=owner, text="Личная тема")
        entry = Entry.objects.create(topic=topic, text="Личная запись")
        self.client.force_login(visitor)
        self.assertNotContains(self.client.get(reverse("learning_logs:topics")), topic.text)
        for name, pk in [
            ("topic", topic.pk), ("new_entry", topic.pk), ("edit_entry", entry.pk)
        ]:
            url = reverse(f"learning_logs:{name}", args=[pk])
            self.assertEqual(self.client.get(url).status_code, 404)
            self.assertEqual(self.client.post(url, {"text": "Подмена"}).status_code, 404)
        entry.refresh_from_db()
        self.assertEqual(entry.text, "Личная запись")
        self.assertEqual(topic.entries.count(), 1)
