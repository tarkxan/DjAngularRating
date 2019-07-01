from django.contrib import admin

# from .models import CSV_Data, Owner, Pet, Sitter, Stay
from .models import Owner, Pet, Sitter, Stay

# admin.site.register(CSV_Data)
admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(Sitter)
admin.site.register(Stay)