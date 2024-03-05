import pytest

from server.apps.main import models

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'model',
    [
        models.Sura,
        models.City,
        models.Ayat,
        models.File,
    ],
)
def test(model, mixer):
    str(mixer.blend(model))


def test_message(mixer):
    str(mixer.blend(models.Message, message_json={}))


def test_user_action(mixer):
    str(mixer.blend(models.UserAction, user__referrer_id=None))


def test_callback_data(mixer):
    str(mixer.blend(models.CallbackData, json={}, user__referrer_id=None))


def test_user(mixer):
    str(mixer.blend(models.User, referrer_id=None))
