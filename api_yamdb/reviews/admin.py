from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    inlines = (GenreTitleInline,)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'genres', 'year'
    )
    list_editable = (
        'category',
    )
    inlines = (GenreTitleInline,)

    def genres(self, instance):
        return [genre.name for genre in instance.genre.all()]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
    )
