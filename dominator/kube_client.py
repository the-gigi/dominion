from kubernetes import client, config

config.load_kube_config()
kube_client = client.CustomObjectsApi()
