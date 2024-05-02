import time

import pytest
from playwright.sync_api import Page, expect

# pytestmark = [pytest.mark.django_db]


def test(page: Page, live_server):
    page.goto(f'{live_server.url}/messages')
    time.sleep(60)
