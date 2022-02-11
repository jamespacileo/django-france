from django.core.management.base import BaseCommand
from django.contrib.sitemaps import ping_google


class Command(BaseCommand):
    help = "Ping Google with an updated sitemap, pass optional url of sitemap"

    def execute(self, *args, **options):
        sitemap_url = args[0] if len(args) == 1 else None
        ping_google(sitemap_url=sitemap_url)

