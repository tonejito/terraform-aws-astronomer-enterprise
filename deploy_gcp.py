#!/usr/bin/env python3

import os
import json
import psutil
import subprocess
from contextlib import contextmanager

# this is the directory of this file
_dir = os.path.dirname(os.path.realpath(__file__))

def read_outputs_from_tfstate(path):
    ''' Parse TF state to find the
    outputs of the root module
    '''
    with open(path, "r") as state_file:
        tfstate = json.loads(state_file.read())

    modules = tfstate["modules"]
    outputs = {}
    # root
    module = modules[0]
    for key, value in module["outputs"].items():
        outputs[key] = value["value"]
    return outputs

def run_terraform(terraform_directory,
                  variables_file,
                  target=None,
                  environment={},
                  state_path=None):
    if not state_path:
        state_path = os.path.join(_dir, "terraform.tfstate")
    subprocess.run(["/usr/local/bin/terraform", "init"], cwd=terraform_directory, check=True)
    command = ["/usr/local/bin/terraform",
               "apply",
               "--auto-approve",
               f"-var-file={variables_file}"]
    if target:
        command.append(f"--target={target}")
    if not os.path.isfile(state_path):
        command.append(f"-state-out={state_path}")
    else:
        command.append(f"-state={state_path}")
    subprocess.run(command,
                   cwd=terraform_directory,
                   env=environment,
                   check=True)
    return read_outputs_from_tfstate(state_path)

def _kill_process(self, proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

@contextmanager
def _background_process(self, command):
    process = subprocess.Popen(
            command,
            shell=True)
    yield process
    self._kill_process(process.pid)

def main():
    gcp_dir = os.path.join(_dir, "terraform/")
    vars_file = os.path.join(_dir, "environments/steven-gcp.tfvars")
    outputs = run_terraform(gcp_dir,
                            vars_file,
                            target="module.astronomer_gcp")
    environment = {
        "https_proxy": f"socks5://127.0.0.1:{outputs['proxy_port']}"
    }
    with _background_process(outputs['bastion_socks5_proxy_command']):
        outputs = run_terraform(gcp_dir,
                                "environments/steven-gcp.tfvars",
                                target="module.astronomer_gcp",
                                environment=environment)

if __name__ == "__main__":
    main()
