from django.conf import settings

# Create your views here.
from django.template.response import TemplateResponse


def index_view(request):

    return TemplateResponse(request, 'index.html', {
        'client_id': settings.SLACK_CLIENT_ID
    })
