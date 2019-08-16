from django.core.management import base

from guess import models


class Command(base.BaseCommand):
    help = 'Start a new Lucky Call contest'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str)

    def handle(self, *args, **options):
        keyword = options['keyword']
        self.stdout.write(
            'Starting a new contest with keyword: {}'.format(keyword)
        )
        models.LuckyCallContest.objects.create(keyword=keyword)
        self.stdout.write('Created! New contest begins.')
