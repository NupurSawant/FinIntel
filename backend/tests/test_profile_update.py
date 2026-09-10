import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
pytestmark = pytest.mark.skip(
    reason="Profile persistence tests require an isolated managed PostgreSQL test database."
)
