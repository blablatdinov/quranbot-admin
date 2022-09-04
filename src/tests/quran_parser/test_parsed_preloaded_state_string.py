import json
from pathlib import Path

import pytest

from integrations.umma import ParsedPreloadedStateString, Substring, TrimmedPreloadedStateString, UmmaRuState
from settings import settings


class PreloadedStateStringsMock(Substring):

    async def find(self):
        yield Path(settings.BASE_DIR / 'src' / 'tests' / 'quran_parser' / 'fixtures' / 'preloaded_state_string.txt').read_text()


async def test_trim():
    generator = TrimmedPreloadedStateString(PreloadedStateStringsMock()).find()
    got = await generator.__anext__()
    json.dumps(got)

    assert '[И прося помощи у Господа, удаляюсь от всего сатанинского, исходящего] от джиннов и людей' in got


@pytest.fixture()
def ayat_content():
    return ' '.join([
        'Скажи: «Прибегаю я к Господу людей, Властителю их [и] Богу их, удаляясь от зла [Сатаны] нашептывающего',
        'и отступающего [при упоминании Творца]. Он (Cатана) нашептывает [вносит смуту, смятение, страхи, сомнения]',
        'в сердца [души, умы] людей.',
        '[И прося помощи у Господа, удаляюсь от всего сатанинского, исходящего] от джиннов и людей».'
    ])


async def test_parse(ayat_content):
    generator = ParsedPreloadedStateString(
        TrimmedPreloadedStateString(PreloadedStateStringsMock())
    ).find()

    got = await generator.__anext__()

    assert isinstance(got, UmmaRuState)
    assert got.ayats[0].sura_number == 114
    assert got.ayats[0].ayat_number == '1-6'
    assert got.ayats[0].content == ayat_content
