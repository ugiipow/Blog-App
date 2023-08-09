from django.contrib import admin

# Register your models here.
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'status', 'posted_on', 'is_deleted')
  list_filter = ('status', 'posted_on', 'is_deleted')
  search_fields = ['title', 'content']
  prepopulated_fields = {"slug": ("title",)}
  summernote_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "post", "posted_on", "active")
    list_filter = ("active", "posted_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Admin kullanıcılar için tüm postları göster
            return qs
        # Diğer kullanıcılar için sadece is_deleted=False olanları göster
        return qs.filter(is_deleted=False)

    def delete_model(self, request, obj):
        # is_deleted alanını True olarak işaretle
        obj.is_deleted = True
        obj.save()


admin.site.register(Post, PostAdmin)