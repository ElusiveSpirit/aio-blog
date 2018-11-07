

async def test_user(cli):
    resp = await cli.get('/api/v1/user')
    assert await resp.json() == {'users': []}


async def test_index_page(cli):
    resp = await cli.get('/api/v1/')
    assert await resp.json() == {}
