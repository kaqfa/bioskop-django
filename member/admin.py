from django.contrib import admin
from .models import TopUp, Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_full_name', 'user_email', 'phone', 'address']


class TopUpAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'receipt', 'status',
                    'uploaded_at', 'validated_at', 'checked_by']
    fields = ['member', 'amount', 'receipt', 'status']
    readonly_fields = ['member', 'amount', 'receipt']
    actions = ['check_valid', 'check_invalid']

    def save_model(self, request, obj, form, change):
        obj.checked_by = request.user
        super(TopUpAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def check_valid(self, request, queryset):
        queryset.update(status='v', checked_by=request.user)
    check_valid.short_description = "Validasi TopUp"

    def check_invalid(self, request, queryset):
        queryset.update(status='i', checked_by=request.user)
    check_invalid.short_description = "Invalidasi TopUp"


admin.site.register(TopUp, TopUpAdmin)
admin.site.register(Member, MemberAdmin)
