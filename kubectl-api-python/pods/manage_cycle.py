from os import path

import yaml

from kubernetes import client, config

namespace = 'default' # str | object name and auth scope, such as for teams and projects

DEPLOYMENT_NAME = "nginx-deployment"

# def create_deployment_object():
#     # config pod template container

#     container = client.V1Container(
#         name="nginx",
#         image="nginx:1.7.9",
#         ports=[client.V1ContainerPort(container_port=80)])

#     template = client.V1PodTemplateSpec(
#         # metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
#         # spec=client.V1PodSpec(containers=[container])
#         metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
#         spec=client.V1PodSpec(containers=[container]))

#     # spec = client.ExtensionsB1beta1DeploymentSpec(
#     #     replicas=3,
#     #     template = template)
    
#     spec = client.ExtensionsV1beta1DeploymentSpec(
#         replicas=3,
#         template=template)


#     deployment = client.ExtensionsV1beta1Deployment(
#         api_version="extensions/v1beta1",
#         kind="Deployment",
#         metadata=client.V1ObjectMeta(namespace="default")
#     )

#     return deployment

def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="nginx",
        image="nginx:1.7.9",
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment

def create_deployment(api_instance,deployment):
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default"
    )

    print("Deployment created status %s " % str(api_response.status))

def delete_deployment(api_instance):
    api_response = api_instance.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status %s" % str(api_response.status))

def update_deployment(api_instance, deployment):
    deployment.spec.template.spec.containers[0].image = "nginx:1.9.1"
    api_response = api_instance.patch_namespaced_deployment(
        name = DEPLOYMENT_NAME,
        namespace = "default",
        body = deployment
    )
    print("Deployment updated. status = %s" % str(api_response.status))

def main():
    config.load_kube_config()

    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    deployment = create_deployment_object()

    try:
        create_deployment(extensions_v1beta1, deployment)

        update_deployment(extensions_v1beta1, deployment)
    except:
        delete_deployment(extensions_v1beta1)

if __name__ == '__main__':
    main() 
else:
    print(__name__) 
    main()

# custom config!!