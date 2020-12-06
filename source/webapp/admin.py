from django.contrib import admin

from webapp.models import Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'photo', 'author', 'signature',)


admin.site.register(Gallery, GalleryAdmin)
