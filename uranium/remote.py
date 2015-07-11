import uranium._vendor.requests as requests


def get_remote_script(url):
    """
    download a remote script, evaluate it, and return it.

    this can be VERY DANGEROUS! downloading and executing
    raw code from any remote source can be very insecure.
    """
    resp = requests.get(url)
    script_locals = {}
    exec(resp.text, script_locals)
    return script_locals
