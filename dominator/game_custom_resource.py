from dominator.custom_resource import CustomResource


class GameCustomResource(CustomResource):
    def __init__(self, name, kube_client):
        super().__init__(name, 'games', kube_client)
