import pytest
from django.template.loader import render_to_string


@pytest.mark.parametrize('template', ['admin_layout.html', 'base.html'])
def test(template):
    render_to_string(template)
