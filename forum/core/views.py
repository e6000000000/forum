from django.views import View
from django.http import HttpResponseServerError, HttpResponse
from django.template.loader import get_template
import traceback

from .exceptions import HttpError


class BaseView():
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except HttpError as e:
            template = get_template('error.html')
            context = {
                'error_type': f'Error {e.code}',
                'text': e.txt,
            }
            return HttpResponse(
                template.render(context, request),
                status=e.code
            )
        except Exception:
            template = get_template('error.html')
            context = {
                'error_type': 'Server error',
                'text': traceback.format_exc(),
            }
            return HttpResponseServerError(
                template.render(context, request)
            )

