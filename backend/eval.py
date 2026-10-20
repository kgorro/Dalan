"""Accuracy and latency check.

  python eval.py                 test the keyword router alone (no server, no model)
  python eval.py --server URL    test the full pipeline on a running server, e.g. http://localhost:8000

Add real tourist questions to TESTS as you collect them. Aim for 200+.
"""
import json
import statistics
import sys
import time
from pathlib import Path

from router import KeywordRouter

TESTS = [
    ("how to go to bantayan", "bantayan"), ("malapascua thresher sharks", "malapascua"),
    ("how much whale shark oslob", "oslob"), ("canyoneering price", "kawasan"),
    ("where to buy danggit", "p-danggit"), ("best chicharon", "p-chicharon"),
    ("what pasalubong should i buy", "pasalubong"), ("places in north cebu", "north-overview"),
    ("what to see in the south", "south-overview"), ("airport to city", "airport"),
    ("is it safe", "safety"), ("emergency number", "safety"), ("when is sinulog", "sinulog"),
    ("best month to visit", "best-time"), ("lake danao camotes", "camotes"), ("sardine run", "moalboal"),
    ("highest mountain in cebu", "osmena-peak"), ("osmeña peak", "osmena-peak"),
    ("simala dress code", "dress-code"), ("how much budget per day", "budget"),
    ("dried mangoes", "p-dried-mangoes"), ("vegetables farmers market", "p-mantalongon-veg"),
    ("lechon", "p-lechon"), ("rosquillos liloan", "p-rosquillos"), ("bisaya phrases", "phrases"),
    ("ferry to bohol", "dumaguete-bohol"), ("typhoon ferry cancelled", "typhoon"),
    ("jeepney", "getting-around"), ("temple of leah", "city-uplands"), ("magellan cross", "city-heritage"),
    ("can i bring danggit on the plane", "cargo-food"), ("sim card", "sim"), ("atm in bantayan", "money"),
    ("hablon weaving", "p-hablon"), ("guitar", "p-guitars"), ("3 days itinerary", "itinerary-3d"),
    ("what to eat", "food"), ("hello", "greet"), ("quantum physics", "fallback"),
    ("carbon market", "markets"), ("Asa ko makapalit og danggit?", "p-danggit"),
    ("tablea", "p-sikwate-tablea"), ("mantalongon", "p-mantalongon-veg"),
]


def main():
    kb = json.loads((Path(__file__).resolve().parents[1] / "kb" / "kb.json").read_text(encoding="utf-8"))
    server = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--server" else None
    if server:
        import httpx
        ask = lambda q: httpx.post(f"{server}/chat", json={"question": q}, timeout=60).json()["entry_id"]
    else:
        router = KeywordRouter(kb)
        ask = lambda q: router.route(q)["entry"]["id"]
    ok, times = 0, []
    for q, want in TESTS:
        t0 = time.perf_counter()
        got = ask(q)
        times.append((time.perf_counter() - t0) * 1000)
        ok += got == want
        if got != want:
            print(f"MISS  {q!r} -> {got} (want {want})")
    times.sort()
    print(f"accuracy {ok}/{len(TESTS)} = {ok / len(TESTS):.0%}")
    print(f"latency p50 {statistics.median(times):.3f} ms, p95 {times[int(len(times) * .95) - 1]:.3f} ms")


if __name__ == "__main__":
    main()
