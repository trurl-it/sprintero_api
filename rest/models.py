from __future__ import unicode_literals

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
