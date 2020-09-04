from django.contrib import admin
from .models import Post, Photo, PostView, Comment, Reply

# To add profile in user model in admin page
class PhotoInline(admin.StackedInline):
    model = Photo
    can_delete = False
    verbose_name_plural = 'Photo'
    fk_name = 'post'

class PostAdmin(admin.ModelAdmin):
    # To add the profile model in admin
    inlines = (PhotoInline,)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(PostAdmin, self).get_inline_instances(request, obj)

    list_display = ['foodType', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['foodType']

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'photos']

class PostViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PostView, PostViewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)