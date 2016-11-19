# -*- coding: utf-8 -*-
import json

from django.core.management.base import BaseCommand

from rest.models import MarvelDatabase


class Command(BaseCommand):
    help = 'Mark marvel heroes as well known.'
    hero_f_name = 'core/management/commands/data/well_known/heroes.json'
    villians_f_name = 'core/management/commands/data/well_known/villians.json'

    def handle(self, *args, **options):

        def get_list(f_name):
            with open(f_name, 'r') as f:
                return json.loads(f.read())

        def find_and_mark(hero_list):
            for hero_name in hero_list:
                hero_db = MarvelDatabase.objects.filter(name__icontains=hero_name).first()
                if hero_db:
                    hero_db.is_well_known = True
                    hero_db.save()

                else:
                    # try to find other way
                    try:
                        first_name, last_name = hero_name.split(' ', 1)
                    except ValueError:
                        continue
                    if first_name and last_name:
                        hero_db = MarvelDatabase.objects.filter(name__icontains=last_name).first() or \
                                    MarvelDatabase.objects.filter(name__icontains=first_name).first()
                        if hero_db:
                            hero_db.is_well_known = True
                            hero_db.save()

        heroes = get_list(self.hero_f_name)
        villians = get_list(self.villians_f_name)

        find_and_mark(heroes)
        find_and_mark(villians)
