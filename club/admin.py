from django.contrib import admin
from .models import Profile, Ride, Poll, PollChoice, Vote


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


class RideRidersInline(admin.TabularInline):
    model = Ride.riders.through
    extra = 1


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_time', 'start_point', 'end_point', 'completed', 'created_by']
    search_fields = ['title', 'description', 'start_point', 'end_point']
    list_filter = ['completed', 'date_time', 'created_at']
    list_editable = ['completed']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['riders']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'date_time')
        }),
        ('Location', {
            'fields': ('start_point', 'end_point')
        }),
        ('Media', {
            'fields': ('header_photo', 'gpx_file')
        }),
        ('External Links', {
            'fields': ('calimoto_url', 'relive_url')
        }),
        ('Participants', {
            'fields': ('created_by', 'riders')
        }),
        ('Status', {
            'fields': ('completed',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_by', 'created_at', 'closes_at']
    search_fields = ['title', 'description']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at']
    inlines = [PollChoiceInline]


@admin.register(PollChoice)
class PollChoiceAdmin(admin.ModelAdmin):
    list_display = ['poll', 'text', 'vote_count']
    search_fields = ['text', 'description']
    list_filter = ['poll']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'choice', 'voted_at']
    search_fields = ['user__username']
    list_filter = ['voted_at', 'choice__poll']
    readonly_fields = ['voted_at']
