from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from simple_history.admin import SimpleHistoryAdmin
from projects.models import Location, Project, Activity, Leave


class LocationAdmin(SimpleHistoryAdmin):
    list_display = ("title", "comment", "id")


class LeaveAdmin(SimpleHistoryAdmin):
    exclude = ("user",)
    list_display = ("id", "user", "type", "date", "duration", "comment")

    def get_queryset(self, request):
        qs = super(LeaveAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class ActivityAdmin(SimpleHistoryAdmin):
    exclude = ("user",)
    list_display = (
        "id",
        "user",
        "project",
        "date",
        "duration",
        "is_teleworking",
        "is_business_trip",
        "location",
    )

    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class ActivityInline(admin.TabularInline):
    model = Activity
    fields = (
        "id",
        "user",
        "project",
        "date",
        "duration",
        "is_teleworking",
        "is_business_trip",
        "location",
    )
    readonly_fields = fields
    can_delete = False
    extra = 0

    def get_queryset(self, request):
        qs = super(ActivityInline, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


class ProjectAdmin(SimpleHistoryAdmin, DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "comment", "id")
    list_display_links = ("indented_title",)
    inlines = [ActivityInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            print(instance)
            instance.save()
        formset.save_m2m()


admin.site.register(Location, LocationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Leave, LeaveAdmin)
