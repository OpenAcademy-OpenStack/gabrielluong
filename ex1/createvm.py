#!/usr/bin/python
from novaclient.v1_1 import client as nclient
from keystoneclient.v2_0 import client as kclient
from credential import credentials
from datetime import datetime
import glanceclient as gclient


# Authenticate against Keystone and return a valid Keystone client
def getKeystoneClient():
    return kclient.Client(username=credentials["username"],
                          password=credentials["password"],
                          auth_url=credentials["auth_url"],
                          tenant_name=credentials["tenant_name"])


# Returns a Glance client
def getGlanceClient():
    return gclient.Client(
        "1", endpoint=keystone.service_catalog.url_for(service_type="image"),
        token=keystone.auth_token)


# Returns a Nova client
def getNovaClient():
    return nclient.Client(credentials["username"], credentials["password"],
                          credentials["tenant_name"], credentials["auth_url"],
                          service_type="compute")


# Query the list of images for the given name, and create a VM of the matched
# images
def createVM(images, name):
    nova = getNovaClient()

    for image in images:
        if image["name"] == name:
            flavor = nova.flavors.find(name="m1.small")
            nova.servers.create(name="exercise" + datetime.now().microsecond,
                                image=image, flavor=flavor)

if __name__ == "__main__":
    keystone = getKeystoneClient()
    glance = getGlanceClient()

    images = glance.images.list()
    createVM(images, "ubuntu")
