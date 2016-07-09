import os
import requests


def get_remote_script(url, local_vars=None, cache_dir=None,
                      refresh_cache=False):
    """
    download a remote script, evaluate it, and return a dictionary
    containing all of the globals instantiated.

    this can be VERY DANGEROUS! downloading and executing
    raw code from any remote source can be very insecure.

    if a cache directory is provided, the script will
    """
    body = None
    local_vars = local_vars or {}
    if cache_dir:
        body = _retrieve_script_from_cache(
            url, cache_dir,
            refresh_cache=refresh_cache
        )
    else:
        body = requests.get(url).text
    script_locals = {}
    script_locals.update(local_vars)
    exec(body, script_locals)
    return script_locals


def _retrieve_script_from_cache(url, cache_dir, refresh_cache=False):
    path = url.replace("/", "_").replace("\\", "_")
    path = os.path.join(cache_dir, path)
    if refresh_cache or not os.path.exists(path):
        body = requests.get(url).text
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        with open(path, "w") as fh:
            fh.write(body)
        return body
    with open(path) as fh:
        return fh.read()
