#!/usr/bin/env python3

import re
import os
import json
import subprocess
from pprint import pprint
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

    def _get_resource(self, _type, _name):
        ''' Parse TF state to find the
        outputs of this target
        '''
        # load the state file and json parse it
        with open(self.statefile, "r") as statefile:
            tfstate = json.loads(statefile.read())

        for resource in tfstate['resources']:
            if resource['type'] == _type and \
                    resource['name'] == _name:
                pprint(resource)
                return resource

        raise RuntimeError(f"Did not find {_type} {_name}")

class Astronomer(TerraformTarget):
    def __init__(self, *args, **kwargs):
        ''' Add the Astronomer target
        to the constructor before instantiating
        '''
        target = "module.astronomer"
        super(Astronomer, self).__init__(target,
                                       *args,
                                       **kwargs)

class SystemComponents(TerraformTarget):
    def __init__(self, *args, **kwargs):
        ''' Add the target
        to the constructor before instantiating
        '''
        target = "module.system_components"
        super(SystemComponents, self).__init__(target,
                                       *args,
                                       **kwargs)

class InfraLayer(TerraformTarget):
    pass

class GcpInfra(InfraLayer):
    def __init__(self, *args, **kwargs):
        ''' Add the GCP-specific target
        to the constructor before instantiating
        '''
        target = "module.gcp"
        super(GcpInfra, self).__init__(target,
                                       *args,
                                       **kwargs)

    def _proxy_command(self):
        zone = self._get_resource("google_compute_instance", "bastion")['instances'][0]['zone']
        name = self._get_resource("google_compute_instance", "bastion")['instances'][0]['name']
        return f"gcloud beta compute ssh --zone {zone} {name} --tunnel-through-iap --ssh-flag='-L 1234:127.0.0.1:8888 -C -N'"

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
        target = "module.aws"
        super(AwsInfra, self).__init__(target,
                                       *args,
                                       **kwargs)
