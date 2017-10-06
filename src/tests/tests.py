import sys
import os

# Add this directory to python path (contains nosetest_config)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from biothings.tests.tests import BiothingTests
from biothings.tests.settings import BiothingTestSettings

ns = BiothingTestSettings()

# *****************************************************************************
#  TODO:  Fix the BiothingTests
# *****************************************************************************
# class HumanPPITests(BiothingTests):
#     __test__ = True
#
#     # Add extra nosetests here
#     pass
