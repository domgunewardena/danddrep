from django.contrib import admin
from rep_app.models import Review, Note, Tag, Manager, OpsDirector, Restaurant
# Register your models here.
admin.site.register(Manager)
admin.site.register(OpsDirector)
admin.site.register(Restaurant)

admin.site.register(Review)
admin.site.register(Note)
admin.site.register(Tag)
