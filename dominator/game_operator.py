import kopf


@kopf.on.create('dominion.org', 'v1', 'games')
def create_fn(body, **kwargs):
    print(f"A handler is called with body: {body}")
