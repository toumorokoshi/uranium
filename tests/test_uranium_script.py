"""
tests for the warmup script
"""
import os


def test_run_warmup(sandbox):
    desired_files = {
        # we're looking for activate because it only exists when
        # <root> is a virtualenv directory.
        'virtualenv': os.path.join(sandbox.root, 'bin', 'activate')
    }

    for name, path in desired_files.items():
        assert os.path.exists(path), "{0} does not exist after warmup".format(name)
