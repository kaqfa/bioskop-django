from django.contrib import admin
from .models import Genre, Movie


class GenreAdmin(admin.ModelAdmin):
    pass

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover', 'show_genres', 'posted_by', "show_status",
                    'show_from', 'show_until', 'created_at')
    fields = ('title', 'cover', 'description', 'show_from', 'show_until', 'genres')

    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        super(MovieAdmin, self).save_model(request, obj, form, change)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
