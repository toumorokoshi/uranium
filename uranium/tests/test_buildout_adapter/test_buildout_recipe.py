import os
from uranium.tests.utils import BaseBuildoutTest
from nose.plugins.attrib import attr
from nose.tools import ok_

BUILDOUT_SCRIPT_TEXT = "./bin/nosetests -a '!full' --with-coverage --cover-package=sprinter"


@attr(full=True)
class TestBuildoutRecipe(BaseBuildoutTest):

    config = {
        'phases': {
            'after-eggs': ['unit']
        },
        'parts': {
            'unit': {
                'recipe': 'yt.recipe.shell',
                'script': BUILDOUT_SCRIPT_TEXT,
                'name': 'unit'
            }
        }
    }

    def test_run_buildout_recipe(self):
        self.uranium.run()
        # yt.recipe.shell installs a script
        script_path = os.path.join(self.root, 'bin', 'unit')
        ok_(os.path.exists(script_path))
        with open(script_path) as fh:
            ok_(BUILDOUT_SCRIPT_TEXT in fh.read())
