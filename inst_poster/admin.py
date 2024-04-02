from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth.models import User, Group


admin.site.site_header = 'iAp админ-панель'
admin.site.index_title = 'Админ-панель'

class DataCredentialsAdmin(admin.ModelAdmin):
    list_display = ['id', 'login_inst', 'pass_inst', 'login_mail', 'pass_mail', 'timestamp']
    search_fields = ['login_inst']
    list_display_links = ['id', 'login_inst', 'pass_inst', 'login_mail', 'pass_mail', 'timestamp']


class InstPhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'photo']
    list_display_links = ['id', 'category']
    list_filter = ['category']
    search_fields = ['category']
    actions_on_top = True
    actions_on_bottom = True

class ProxyCredentialsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'proxy_ip', 'proxy_login', 'proxy_pass', 'timestamp']
    list_display_links = ['proxy_ip', 'proxy_login', 'proxy_pass']


class ResultsAdminForm(forms.ModelForm):
    class Meta:
        model = Results
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ResultsAdminForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True


class ResultsAdmin(admin.ModelAdmin):
    form = ResultsAdminForm
    list_display = ['id', 'get_login_inst', 'good_link', 'timestamp']
    list_display_links = ['id', 'get_login_inst']
    search_fields = ['data_credentials__login_inst']

    def get_login_inst(self, obj):
        return obj.data_credentials.login_inst if obj.data_credentials else ''
    get_login_inst.short_description = 'Аккаунт'



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_filter = ['title']
    actions_on_top = True
    actions_on_bottom = True


class CaptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'get_category_caption']
    list_display_links = ['id', 'category', 'get_category_caption']
    search_fields = ['category']

    def get_category_caption(self, obj):
        return f'Подписи к категории "{obj.category}"'

    get_category_caption.short_description = 'Подписи к категории'


admin.site.register(Results, ResultsAdmin)
admin.site.register(DataCredentials, DataCredentialsAdmin)
admin.site.register(InstPhotos, InstPhotosAdmin)
admin.site.register(ProxyCredentials, ProxyCredentialsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Captions, CaptionsAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)