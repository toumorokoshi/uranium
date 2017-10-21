"""
this is a forked activation script for virtualenv.

By using execfile(this_file, dict(__file__=this_file)) you will
activate this virtualenv environment.
"""

try:
    __file__
except NameError:
    raise AssertionError(
        "You must run this like execfile('path/to/activate_this.py', dict(__file__='path/to/activate_this.py'))"
    )
import sys
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _get_site_packages():
    """
    try a variety of site package directories, finding one that works.
    """
    paths_to_try = [
        # typically win32
        os.path.join(base, 'Lib', 'site-packages'),
        # standard
        os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages'),
        # typically pypy
        os.path.join(base, 'site-packages'),
    ]
    for p in paths_to_try:
        if os.path.isdir(p):
            return p
    return os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')


old_os_path = os.environ.get('PATH', '')
os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + old_os_path
prev_sys_path = list(sys.path)
site_packages = _get_site_packages()
import site
site.addsitedir(site_packages)
if not hasattr(sys, "real_prefix"):
    sys.real_prefix = sys.prefix

sys.prefix = base
# Move the added items to the front of the path:
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

if not hasattr(sys, "real_executable"):
    sys.real_executable = sys.executable

sys.executable = os.path.join(base, "bin", "python")
