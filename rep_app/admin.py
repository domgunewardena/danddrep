from django.contrib import admin
from rep_app.models import Review, Note, Manager
# Register your models here.
admin.site.register(Manager)
admin.site.register(Review)
admin.site.register(Note)
