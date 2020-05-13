from dominator.custom_resource import CustomResource


class PlayerCustomResource(CustomResource):
    def __init__(self, name, kube_client):
        super().__init__(name, 'players', kube_client)

    @property
    def playerType(self):
        return self.spec['playerType']


