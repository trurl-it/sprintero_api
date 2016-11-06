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
                    "pretext": "Sprintero gives you names",
                    "title": name,
                    "title_link": url,
                    "text": "Character is {}. And is in the {} group.".format(
                        "still alive" if serialized_data["alive"] == "Living Characters" else "dead",
                        serialized_data["align"],
                    ),
                    "color": "#7CD197"
                }
            ]
        }
