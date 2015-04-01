try:
    # For Python 2
    from urlparse import urlparse, urlunparse
except ImportError:
    # For Python 3
    from urllib.parse import urlparse, urlunparse
from flask import request, redirect
from bnd import create_app
app = create_app(__name__)


@app.before_request
def redirect_www():
    """Redirect www requests to non-www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc.startswith('www.'):
        urlparts_list = list(urlparts)
        urlparts_list[1] = urlparts_list[1][len('www.'):]
        return redirect(urlunparse(urlparts_list), code=301)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
