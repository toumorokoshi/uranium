# an import is required to support this encoding in
# libraries such as requests
import encodings.idna

# we import setuptools to ensure it's provided
# when attempting to use uranium within a sandbox.
import setuptools

from .remote import get_remote_script
