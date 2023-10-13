from django.contrib import admin
from .models import Expense, Category, Image, Document,DocumentUpload

# Register your models here.


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'category', 'date')
    search_fields = ('amount', 'description', 'owner', 'category', 'date')


admin.site.register(Expense, ExpensesAdmin)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Document)
admin.site.register(DocumentUpload)
