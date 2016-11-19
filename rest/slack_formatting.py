# -*- coding: utf-8 -*-
from urlparse import urljoin

from django.conf import settings


class SlackFormatter(object):

    def format(self, serialized_data):
        name = serialized_data['name'].replace('(Earth-616)', '').strip()
        url = urljoin(settings.MARVEL_WIKIA, serialized_data['url_slug'].replace('\\', ''))
        return {
            "attachments": [
                {
                    "fallback": name,
                    "pretext": "Your sprint name is",
                    "title": name,
                    "title_link": url,
                    "text": "{}. {}.".format(
                        "Alive" if serialized_data["alive"] == "Living Characters" else "Dead",
                        serialized_data["align"],
                    ),
                    "color": "#7CD197"
                }
            ]
        }
