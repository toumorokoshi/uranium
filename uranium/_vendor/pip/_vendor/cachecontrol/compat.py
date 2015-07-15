try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


try:
    import cPickle as pickle
except ImportError:
    import pickle


from uranium._vendor.pip._vendor.requests.packages.urllib3.response import HTTPResponse
from uranium._vendor.pip._vendor.requests.packages.urllib3.util import is_fp_closed
