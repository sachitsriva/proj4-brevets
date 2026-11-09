import acp_times
import arrow

def test_start_times():
    ## The starting control closes one hour after the start
    start = arrow.get("2026-11-08T00:00:00+00:00")
    assert acp_times.open_time(0, 200, start.isoformat()) == start.isoformat()
    assert acp_times.close_time(0, 200, start.isoformat()) == start.shift(hours=1).isoformat()


def test_early_control():
    ## Controls below 60 
    start = arrow.get("2026-11-08T00:00:00+00:00")
    assert acp_times.open_time(40, 200, start.isoformat()) == start.shift(hours=1, minutes=11).isoformat()
    assert acp_times.close_time(40, 200, start.isoformat()) == start.shift(hours=3).isoformat()


def test_multiple_segments():
    ## Opening times across different segments
    start = arrow.get("2026-11-08T00:00:00+00:00")
    assert acp_times.open_time(350, 400, start.isoformat()) == start.shift(hours=10, minutes=34).isoformat()
    assert acp_times.close_time(350, 400, start.isoformat()) == start.shift(hours=23, minutes=20).isoformat()


def test_finish_limits():
    ## Finishing limits differ from control times
    start = arrow.get("2026-11-08T00:00:00+00:00")
    assert acp_times.close_time(200, 200, start.isoformat()) == start.shift(hours=13, minutes=30).isoformat()
    assert acp_times.close_time(200, 400, start.isoformat()) == start.shift(hours=13, minutes=20).isoformat()
    assert acp_times.close_time(400, 400, start.isoformat()) == start.shift(hours=27).isoformat()


def test_longer_route():
    ## Controls beyond the normal distance
    start = arrow.get("2026-11-08T00:00:00+00:00")
    assert acp_times.open_time(205, 200, start.isoformat()) == start.shift(hours=5, minutes=53).isoformat()
    assert acp_times.close_time(205, 200, start.isoformat()) == start.shift(hours=13, minutes=30).isoformat()

