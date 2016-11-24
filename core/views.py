from django.conf import settings

from django.template.response import TemplateResponse


def index_view(request):

    return TemplateResponse(request, 'index.html', {
        'client_id': settings.SLACK_CLIENT_ID
    })


def success_view(request, team_domain):
    return TemplateResponse(request, 'success.html', {
        'team_domain': team_domain
    })
