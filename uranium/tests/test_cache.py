import os
import shutil
import tempfile
from nose.tools import ok_, raises
from uranium.cache import Cache
from uranium.exceptions import CacheException


class _TestCache(object):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_ensure_directory(self):
        cache_dir = os.path.join(self.temp_dir, '.cache')
        cache = Cache(cache_dir)
        cache.ensure_directory()
        ok_(os.path.isdir(cache_dir))

    def test_ensure_directory_already_exists(self):
        cache_dir = os.path.join(self.temp_dir, '.cache')
        os.makedirs(cache_dir)
        cache = Cache(cache_dir)
        cache.ensure_directory()
        ok_(os.path.isdir(cache_dir))

    @raises(CacheException)
    def test_ensure_directory_with_file(self):
        """
        if a file exists where the cache directory
        should be, raise an exception.
        """
        cache_dir = os.path.join(self.temp_dir, '.cache')
        open(cache_dir, 'w+').close()
        cache = Cache(cache_dir)
        cache.ensure_directory()
