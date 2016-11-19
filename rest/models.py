from __future__ import unicode_literals

from urlparse import urljoin

from django.conf import settings
from django.db import models

# Create your models here.


class MarvelDatabase(models.Model):
    page_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    url_slug = models.CharField(max_length=200)
    identity_status = models.CharField(max_length=200)
    align = models.CharField(max_length=200)
    eye_color = models.CharField(max_length=200)
    hair_color = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    gsm = models.CharField(max_length=200)
    alive = models.CharField(max_length=200)
    appearances = models.CharField(max_length=200)
    first_appearance = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    is_well_known = models.BooleanField(default=False)

    def __str__(self):
        return "[{}-{}]".format(self.name, self.align)

    def get_url(self):
        return urljoin(settings.MARVEL_WIKIA, self.url_slug.replace('\\', ''))
