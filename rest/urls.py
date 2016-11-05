# -*- coding: utf-8 -*-

from rest_framework import routers

from rest.views import MarvelViewSet

router = routers.SimpleRouter()
router.register(r'marvel', MarvelViewSet)
urlpatterns = router.urls
