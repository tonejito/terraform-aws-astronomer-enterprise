#!/usr/bin/env python3

import re
import os
import json
import subprocess
from .utils import git_root

class SituationUnaccountedFor(Exception):
    pass

class EnvironmentError(RuntimeError):
    pass

class TerraformTarget():
    def __init__(self, target, varsfile, statefile, terraform_directory):
        '''
        '''
        self.target = target
        self.varsfile = varsfile
        self.statefile = statefile
        self.terraform_directory = terraform_directory

    def apply(self, refresh=True, environment={}):
        ''' Initialize Terraform
        and apply to the target
        specificed by the extending class,
        returning the outputs specificed
        by the extending class.
        '''
        subprocess.run("terraform init",
                       cwd=self.terraform_directory,
                       check=True,
                       shell=True)
        command = ["terraform",
                   "apply",
                   "--auto-approve",
                   f"-var-file={self.varsfile}",
                   f"--target={self.target}"]
        if not refresh:
            command.append("-refresh=false")
        if not os.path.isfile(self.statefile):
            command.append(f"-state-out={self.statefile}")
        else:
            command.append(f"-state={self.statefile}")
        command = " ".join(command)
        print(f"Running command:\n{command}")
        subprocess.run(command,
                       cwd=self.terraform_directory,
                       env=environment,
                       check=True,
                       shell=True)
        return self._outputs

    @property
    def _outputs(self):
        ''' by default, return all
        '''
        return self._get_output()

    def _get_output(self):
        ''' Parse TF state to find the
        outputs of this target
        '''
        # load the state file and json parse it
        with open(self.statefile, "r") as statefile:
            tfstate = json.loads(statefile.read())

        # get the module name by parsing the target
        module_regex = re.compile("^module\.([^.]*)$")
        matches = module_regex.findall(self.target)
        if len(matches) < 1:
            raise NotImplementedError(
                f"TerraformTarget is only support module targets right now. The target must match {module_regex.pattern} . The target is set to {self.target} .")
        if len(matches) > 1:
            raise SituationUnaccountedFor("Did not expect to find more than one match for the regex {module_regex.pattern}. Applying 'findall' to {self.target}")
        module_name = matches[0]

        # find the appropriate module
        # and return the all outputs
        modules = tfstate["modules"]
        for module in modules:
            if module["path"] == ["root", module_name]:
                outputs = {}
                for k, v in module["outputs"].items():
                    outputs[k] = v['value']
                return outputs
        raise RuntimeError(f"Did not find target {self.target}")

class Astronomer(TerraformTarget):
    def __init__(self, *args, **kwargs):
        ''' Add the Astronomer target
        to the constructor before instantiating
        '''
        target = "module.astronomer"
        super(Astronomer, self).__init__(target,
                                       *args,
                                       **kwargs)
    @property
    def _outputs(self):
        return None

class InfraLayer(TerraformTarget):

    @property
    def _outputs(self):
        ''' All infrastructure layers
        will return a proxy command in the
        output named "bastion_proxy_command"
        and that command will start a proxy
        through the bastion host to the private
        Kubernetes endpoint. The proxy should
        be made available on localhost:1234,
        and it should be an HTTP proxy, not a
        SOCKs proxy, in order to support webhooks
        in helm and kubectl.
        '''
        proxy_command = self._get_output()['bastion_proxy_command']
        https_proxy = "http://127.0.0.1:1234"
        return proxy_command, https_proxy

class GcpInfra(InfraLayer):
    def __init__(self, *args, **kwargs):
        ''' Add the GCP-specific target
        to the constructor before instantiating
        '''
        target = "module.astronomer_gcp"
        super(GcpInfra, self).__init__(target,
                                       *args,
                                       **kwargs)

    def apply(self, *args, **kwargs):
        gcp_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not gcp_creds:
            raise EnvironmentError("For GCP deployments, please set environment variable GOOGLE_APPLICATION_CREDENTIALS as the path to your gcloud cli credentials")
        # create or merge into kwargs['environment']
        if not kwargs.get('environment'):
            kwargs['environment'] = {}
        kwargs['environment']\
            ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_creds
        return super(GcpInfra, self).apply(*args,
                                           **kwargs)

class AwsInfra(InfraLayer):
    def __init__(self, *args, **kwargs):
        ''' Add the AWS-specific target
        to the constructor before instantiating
        '''
        target = "module.astronomer_aws"
        super(AwsInfra, self).__init__(target,
                                       *args,
                                       **kwargs)
