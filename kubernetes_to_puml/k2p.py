#!/usr/bin/env python
import sys

from kubernetes import client, config

_EXCLUDE_NAMESPACES = [
    "kube-system",
    "cattle-dashboards",
    "cattle-monitoring-system",
    "cattle-system",
    "default",
    "fleet-system",
    "kube-node-lease",
    "kube-public",
    "kube-system",
    "security-scan",
]

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

core_v1 = client.CoreV1Api()
networking_v1 = client.NetworkingV1Api()

# Nodes, indexed by name
nodes = {}
print("NODES")
response = core_v1.list_node()
for item in response.items:
    name = item.metadata.name
    cpu = item.status.capacity["cpu"]
    memory = item.status.capacity["memory"]
    print(f" {name}: {cpu} cores, {memory}")
    nodes[name] = item

# Namespaces
namespaces = []
print("NAMESPACES")
response = core_v1.list_namespace()
for item in response.items:
    name = item.metadata.name
    if name not in _EXCLUDE_NAMESPACES:
        print(f" {name}")
        namespaces.append(name)

# Pods, indexed by namespace
pods = {}
for namespace in namespaces:
    response = core_v1.list_namespaced_pod(namespace)
    if response.items:
        print(f"PODS in {namespace}")
    for item in response.items:
        name = item.metadata.name
        print(f" {name}")
        pods[name] = item

# Ingress, indexed by namespace
ingresses = {}
for namespace in namespaces:
    response = networking_v1.list_namespaced_ingress(namespace)
    if response.items:
        print(f"INGRESSES in {namespace}")
    for item in response.items:
        name = item.metadata.name
        print(f" {name}")
        ingresses[name] = item
