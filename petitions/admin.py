from django.contrib import admin
from .models import Petition, Vote

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ('user', 'vote_type', 'created_at')

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'created_by', 'created_at', 'get_yes_votes', 'get_no_votes')
    list_filter = ('created_at', 'created_by')
    search_fields = ('movie_title', 'description')
    readonly_fields = ('created_at',)
    inlines = [VoteInline]

class VoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('petition__movie_title', 'user__username')

admin.site.register(Petition, PetitionAdmin)
admin.site.register(Vote, VoteAdmin)
