from os import path
from kubernetes import client, config, utils


def main():
    config.load_kube_config()
    k8s_client = client.ApiClient()
    utils.create_from_yaml(k8s_client,"nginx-deployment.yaml")
    k8s_api = client.ExtensionsV1beta1Api(k8s_client)
    deps = k8s_api.read_namespaced_deployment("nginx_deployment","default")
    print("Deployment {0} created " % deps.metadata.name)

main()
