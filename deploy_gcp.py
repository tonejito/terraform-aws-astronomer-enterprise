#!/usr/bin/env python3

import os
import sys
import json
import psutil
import subprocess
from pprint import pprint
from contextlib import contextmanager

# this is the directory of this file
_dir = os.path.dirname(os.path.realpath(__file__))

def read_outputs_from_tfstate(state_path):
    ''' Parse TF state to find the
    outputs of all modules
    '''
    with open(state_path, "r") as state_file:
        tfstate = json.loads(state_file.read())

    modules = tfstate["modules"]
    # apply root level outputs with highest priority
    modules.reverse()
    outputs = {}
    for module in modules:
        for key, value in module["outputs"].items():
            outputs[key] = value["value"]
    return outputs

def run_terraform(terraform_directory,
                  variables_file,
                  target=None,
                  environment={},
                  state_path=None,
                  destroy=False,
                  refresh=False):
    if not state_path:
        state_path = os.path.join(_dir, "terraform.tfstate")
    subprocess.run("terraform init", cwd=terraform_directory, check=True, shell=True)
    command = ["terraform",
               "apply",
               "--auto-approve",
               f"-var-file={variables_file}"]
    if not refresh:
        command.append("-refresh=false")
    if destroy:
        command[1] = "destroy"
    if target:
        command.append(f"--target={target}")
    if not os.path.isfile(state_path):
        command.append(f"-state-out={state_path}")
    else:
        command.append(f"-state={state_path}")
    command = " ".join(command)
    subprocess.run(command,
                   cwd=terraform_directory,
                   env=environment,
                   check=True,
                   shell=True)
    return read_outputs_from_tfstate(state_path)

def _kill_process(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

@contextmanager
def _background_process(command):
    process = subprocess.Popen(
            command,
            shell=True)
    try:
        yield process
    finally:
        _kill_process(process.pid)

def destroy():
    gcp_dir = os.path.join(_dir, "terraform/")
    vars_file = os.path.join(_dir, "environments/steven-gcp.tfvars")
    # this is needed to create the let's encrypt cert
    outputs = run_terraform(gcp_dir,
                            vars_file,
                            target="module.astronomer_gcp",
                            destroy=True)

def apply():
    gcp_dir = os.path.join(_dir, "terraform/")
    vars_file = os.path.join(_dir, "environments/steven-gcp.tfvars")

    environment = {
        "GOOGLE_APPLICATION_CREDENTIALS": os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    }

    outputs = run_terraform(gcp_dir,
                            vars_file,
                            target="module.astronomer_gcp",
                            environment=environment,
                            refresh=True)
    proxy_command = outputs['bastion_proxy_command']

    outputs = run_terraform(gcp_dir,
                            vars_file,
                            target="local_file.kubeconfig")

    # pprint(outputs)
    environment = {
        # "https_proxy": f"http://127.0.0.1:{outputs['proxy_port']}"
        "https_proxy": f"http://127.0.0.1:1234",
        "http_proxy": f"http://127.0.0.1:1234",
        "HTTPS_PROXY": f"http://127.0.0.1:1234",
        "HTTP_PROXY": f"http://127.0.0.1:1234",
        "HELM_HOME": os.path.realpath(os.path.join(_dir,".helm")),
        "KUBECONFIG": os.path.join(gcp_dir,"kubeconfig")
    }
    with _background_process(proxy_command):
        outputs = run_terraform(gcp_dir,
                                vars_file,
                                target="module.astronomer",
                                environment=environment)

if __name__ == "__main__":
    if "--destroy" in sys.argv:
        destroy()
    else:
        apply()
