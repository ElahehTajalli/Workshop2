from django.contrib import admin
from message.models import Conversation, Messages


class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'sender', 'date', 'status')
    search_fields = ('text',)


admin.site.register(Conversation)
admin.site.register(Messages, MessageAdmin)
