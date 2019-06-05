#!/usr/bin/env python3

import os
import sys
from python_terraform import Terraform
import subprocess
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)
root_logger = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
root_logger.addHandler(ch)

_dir = os.path.dirname(os.path.realpath(__file__))
gcp_dir = os.path.join(_dir, "terraform/gcp")
state_path = os.path.join(_dir, "terraform.tfstate")
kubeconfig_path = os.path.join(_dir, "kubeconfig")

def run_terraform(directory, variables):
    tf_client = Terraform(
        working_dir=directory,
        state=state_path,
        variables=variables)
    subprocess.run("terraform init", cwd=directory, shell=True)
    tf_client.apply(capture_output=False,
                    skip_plan=True)
    modules = tf_client.tfstate.modules
    outputs = {}
    # root
    module = modules[0]
    for key, value in module["outputs"].items():
        outputs[key] = value["value"]
    return outputs

variables = {
    "project": "astronomer-cloud-dev-236021",
    "region": "us-east4",
    "zone": "us-east4-a",
    "acme_server": "https://acme-v02.api.letsencrypt.org/directory",
    "bastion_admin_emails": ["steven@astronomer.io"],
    "bastion_user_emails": ["steven@astronomer.io"],
    "deployment_id": "steven",
    "dns_managed_zone": "steven-zone",
    "write_kubeconfig_to": kubeconfig_path
}

outputs = run_terraform(gcp_dir, variables)

variables = {
    "db_connection_string": outputs["db_connection_string"],
    "tls_key": outputs["tls_key"],
    "tls_cert": outputs["tls_cert"],
    "kubeconfig_path": outputs["kubeconfig_path"]
}

start_proxy_command = outputs['bastion_socks5_proxy_command']
proxy_proc = subprocess.Popen(start_proxy_command, shell=True)
try:
    print("running")
    sleep(100)
    # run_terraform(astronomer, variables)
finally:
    proxy_proc.terminate()
