from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class InstPosterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inst_poster'
    verbose_name = "Instagram autoposter"

    def ready(self):
        from inst_poster.models import ProxyCredentials
        from scripts.proxy import ProxyZipper
        from . import signals
        @receiver(post_save, sender=ProxyCredentials)
        def update_zip_on_proxy_credentials_change(sender, instance, **kwargs):
            if kwargs.get('created') or kwargs.get('update_fields'):
                pass