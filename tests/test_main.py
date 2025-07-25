from src.main import get_top_artists
from unittest.mock import MagicMock

def test_get_top_artists():
    sp = MagicMock()
    fake_response = {
    "items": [
        {'name': 'test01'},
        {'name': 'test02'},
        {'name': 'test03'},
        {'name': 'test04'},
        {'name': 'test05'},
        {'name': 'test06'},
        {'name': 'test07'},
        {'name': None},
        {'name': 'test08'},
        {'name': 'test09'}
        ]
    }

    sp.current_user_top_artists.return_value = fake_response

    artists = get_top_artists(sp)

    assert len(artists) == 8
    for artist in artists:
        assert artist["name"] is not None