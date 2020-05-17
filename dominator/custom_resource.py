from functools import partial


class CustomResource:
    def __init__(self, name, kind_plural, kube_client):
        self.kube_client = kube_client
        self.name = name
        kwargs = dict(version='v1',
                      namespace='default',
                      plural=kind_plural,
                      name=name)
        self.get = partial(self.kube_client.get_namespaced_custom_object, **kwargs)
        self.patch = partial(self.kube_client.patch_namespaced_custom_object, **kwargs)

    @property
    def spec(self):
        return self.get().get('spec', {})

    @property
    def status(self):
        return self.get().get('status', {})
