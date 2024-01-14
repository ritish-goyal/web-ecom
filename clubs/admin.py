from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Club)
admin.site.register(ClubChat)
admin.site.register(ClubMember)
admin.site.register(ClubElections)
admin.site.register(Candidate)
admin.site.register(Voter)