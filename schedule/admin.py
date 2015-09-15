from django.contrib import admin

from schedule.models import Calendar, Event, CalendarRelation, Rule

class CalendarAdminOptions(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdminOptions(admin.ModelAdmin):

	exclude = ['creator','calendar']

	def save_model(self, request, obj, form, change):
		obj.creator = request.user
		obj.calendar = Calendar.objects.get(name='calendario')
		obj.save()

admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event,EventAdminOptions)
