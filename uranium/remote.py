import requests


def get_remote_script(url, **params):
    """
    download a remote script, evaluate it, and return a dictionary
    containing all of the globals instantiated.

    this can be VERY DANGEROUS! downloading and executing
    raw code from any remote source can be very insecure.
    """
    resp = requests.get(url)
    script_locals = {}
    script_locals.update(params)
    exec(resp.text, script_locals)
    return script_locals
