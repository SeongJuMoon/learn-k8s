from __future__ import print_function
from kubernetes import client, config
import yaml

def main():
    
    config.load_kube_config()

    v1 = client.AppsV1Api()

    status = k8s_beta

    print("nginx was serve them")

if __name__ == "__main__":
    main()