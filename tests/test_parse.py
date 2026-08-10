from src.ingest.receiver import parse_packet

def test_good_packet():
    result = parse_packet(b'{"channel": "rpm", "value": 5000}')
    assert result == {"channel": "rpm", "value": 5000}


def test_bad_packet():
    result = parse_packet(b'this not a valid JSON')
    assert result is None