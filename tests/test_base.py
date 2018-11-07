

async def test_assert(cli):
    resp = await cli.get('/api/v1/')
    assert await resp.json() == {}
