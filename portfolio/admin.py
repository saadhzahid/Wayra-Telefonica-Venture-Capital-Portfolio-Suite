from django.contrib import admin

from portfolio.models import User, Programme, Company, Individual


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'phone', 'is_active'
    ]


admin.site.register(Programme)
admin.site.register(Company)
admin.site.register(Individual)
