import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
