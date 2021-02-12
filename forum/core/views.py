from django.views import View
from django.http import HttpResponseServerError, HttpResponse
from django.template.loader import get_template
import traceback
import logging

from .exceptions import HttpError


logger = logging.getLogger(__name__)


class BaseView():
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except HttpError as e:
            logger.warning('HttpError: ' + e.__str__())
            template = get_template('error.html')
            context = {
                'error_type': f'Error {e.code}',
                'text': e.txt,
            }
            return HttpResponse(
                template.render(context, request),
                status=e.code
            )
        except Exception as e:
            print(e)
            error_text = traceback.format_exc()
            logger.error(error_text)
            template = get_template('error.html')
            context = {
                'error_type': 'Server error',
                'text': error_text,
            }
            return HttpResponseServerError(
                template.render(context, request)
            )

