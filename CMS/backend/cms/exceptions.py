import logging

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import JsonResponse
from django.views import defaults

logger = logging.getLogger(__name__)

DEFAULT_ERROR_MESSAGES = {
    400: 'Invalid request',
    401: 'Authentication required',
    403: 'Permission denied',
    404: 'Not found',
    405: 'Method not allowed',
    500: 'Internal server error',
}


def _is_api_request(request):
    return request.path.startswith('/api/')


def _api_error(message, status):
    return JsonResponse({'error': message, 'status': status}, status=status)


class ApiExceptionMiddleware:
    """Return consistent, non-sensitive JSON errors for unexpected API failures."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if (
                _is_api_request(request)
                and response.status_code >= 400
                and 'application/json' not in response.get('Content-Type', '')
            ):
                return _api_error(
                    DEFAULT_ERROR_MESSAGES.get(response.status_code, 'Request failed'),
                    response.status_code,
                )
            return response
        except PermissionDenied:
            if _is_api_request(request):
                return _api_error('Permission denied', 403)
            raise
        except SuspiciousOperation:
            logger.warning('Bad request to %s', request.path, exc_info=True)
            if _is_api_request(request):
                return _api_error('Invalid request', 400)
            raise
        except Exception:
            logger.exception('Unhandled error while processing %s', request.path)
            if _is_api_request(request):
                return _api_error('Internal server error', 500)
            raise


def api_bad_request(request, exception=None):
    if _is_api_request(request):
        return _api_error('Invalid request', 400)
    return defaults.bad_request(request, exception)


def api_permission_denied(request, exception=None):
    if _is_api_request(request):
        return _api_error('Permission denied', 403)
    return defaults.permission_denied(request, exception)


def api_not_found(request, exception=None):
    if _is_api_request(request):
        return _api_error('Not found', 404)
    return defaults.page_not_found(request, exception)


def api_server_error(request):
    if _is_api_request(request):
        return _api_error('Internal server error', 500)
    return defaults.server_error(request)
