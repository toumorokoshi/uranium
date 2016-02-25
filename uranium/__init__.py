# an import is required to support this encoding in
# libraries such as requests
import encodings.idna

# we import setuptools to ensure it's provided
# when attempting to use uranium within a sandbox.
import setuptools
# same with markerlib
import _markerlib

from .remote import get_remote_script
from .decorators import task_requires
from .rules import rule
from .app_globals import current_build

__all__ = ["get_remote_script", "task_requires", "rule", "current_build"]
