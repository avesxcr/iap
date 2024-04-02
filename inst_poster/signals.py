from django.db.models.signals import post_save
from django.dispatch import receiver
from inst_poster.models import ProxyCredentials
from scripts.proxy import ProxyZipper


@receiver(post_save, sender=ProxyCredentials)
def change_proxy_data(sender, instance, **kwargs):
    bot = ProxyZipper()
    bot.main()