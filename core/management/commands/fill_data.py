# -*- coding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand
from rest.models import MarvelDatabase


class Command(BaseCommand):
    help = 'Fill the MarvelDatabase model.'
    file_name = 'core/management/commands/data/marvel-data.csv'
    columns = [
        'page_id',
        'name',
        'url_slug',
        'identity_status',
        'align',
        'eye_color',
        'hair_color',
        'sex',
        'gsm',
        'alive',
        'appearances',
        'first_appearance',
        'year',
    ]

    def handle(self, *args, **options):
        with open(self.file_name, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|',
                                dialect=csv.excel_tab)
            rows = []
            reader.next()  # skip first row;
            for row in reader:
                data = dict(zip(self.columns, row))
                rows.append(
                    MarvelDatabase(
                        **data
                    )
                )

                if len(rows) == 1000:
                    MarvelDatabase.objects.bulk_create(rows)
                    rows = []
            if rows:
                MarvelDatabase.objects.bulk_create(rows)
