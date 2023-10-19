from django.contrib import admin
from .models import UploadedFile, ApprovedFileTyps
# Register your models here.

admin.site.register(UploadedFile)
admin.site.register(ApprovedFileTyps)