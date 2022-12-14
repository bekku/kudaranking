from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

class RedirectHostMiddleware(MiddlewareMixin):

    def process_request(self, request):
        host = request.get_host()
        if host and host.startswith('www.'):
            redirect_url = '%s://%s%s' % (
                request.scheme, host[4:], request.get_full_path()
            )
            return HttpResponsePermanentRedirect(redirect_url)