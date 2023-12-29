from django.contrib import admin
from dashboard.models import *


admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Driver)
admin.site.register(Citizen)
admin.site.register(Complaint)
