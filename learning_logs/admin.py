from django.contrib import admin

from .models import Entry, Topic

admin.site.register([Topic, Entry])
