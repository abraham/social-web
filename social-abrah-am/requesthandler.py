"""Modifications for all requests."""


from tornado import gen, web


class RequestHandler(web.RequestHandler):

    @gen.coroutine
    def prepare(self):
        proto = self.request.headers.get('X-Forwarded-Proto', 'http')
        origin = self.request.headers.get('Origin', None)
        referer = self.request.headers.get('Referer', None)
        host = self.request.headers.get('Host', None)
        debug = self.settings['debug']

        directives = [
            "default-src 'self'",
            "connect-src 'self'",
            "font-src 'self' https:",
            "frame-src 'self' https://apis.google.com https://www.youtube.com",
            "img-src 'self' https:",
            "media-src 'none'",
            "script-src 'self' https://www.google.com https://ajax.googleapis.com https://www.google-analytics.com https://s.ytimg.com https://apis.google.com https://ssl.google-analytics.com 'unsafe-eval'",
            "style-src 'self' https://*.googleapis.com https://www.google.com https://s.ytimg.com 'unsafe-inline'",
        ]
        self.set_header('Content-Security-Policy', '; '.join(directives))
        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('X-Content-Type-Options', 'nosniff')
        self.set_header('X-Frame-Options', 'DENY')
        self.set_header('X-UA-Compatible', 'IE=edge, chrome=1')

        if proto.lower() == 'https':
            self.set_header('Strict-Transport-Security', 'max-age="31536000"; includeSubDomains')
