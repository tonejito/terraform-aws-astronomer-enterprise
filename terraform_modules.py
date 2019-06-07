import re
import subprocess

class SituationUnaccountedFor(Exception):
    pass

class TerraformTarget():
    def __init__(self, target, varsfile, statefile):
        '''
        '''
        self.target = target
        self.varsfile = varsfile
        self.statefile = statefile

    def apply(self, refresh=False):
        ''' Initialize Terraform
        and apply to the target
        specificed by the extending class,
        returning the outputs specificed
        by the extending class.
        '''
        subprocess.run("terraform init",
                       cwd=self._terraform_directory,
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
        subprocess.run(command,
                       cwd=terraform_directory,
                       env=environment,
                       check=True,
                       shell=True)
        return self._outputs

    @property
    def _terraform_directory(self):
        ''' Defaults to:
        <git_root>/terraform
        '''
        git_root = subprocess.check_output(
            "git rev-parse --show-toplevel",
            shell=True).decode('utf-8').strip()
        return os.path.join(git_root,"terraform")

    @property
    def _outputs(self):
        raise NotImplementedError()

    def _get_output(self, output):
        ''' Parse TF state to find the
        specific output of this target
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
        # and return the matching output
        modules = tfstate["modules"]
        found_output_keys = []
        for module in modules:
            if module["path"] == ["root", module_name]:
                for k, v in module["outputs"].items():
                    found_output_keys.append(k)
                    if k == output:
                        return v['value']
        raise RuntimeError(f"Did not find output '{output}'. We found the following outputs in the target {self.target}: {found_output_keys}")

class Astronomer(TerraformTarget):
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
        proxy_command = self._get_output(
            "bastion_proxy_command")
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

class AwsInfra(InfraLayer):
    def __init__(self, *args, **kwargs):
        ''' Add the AWS-specific target
        to the constructor before instantiating
        '''
        target = "module.astronomer_aws"
        super(GcpInfra, self).__init__(target,
                                       *args,
                                       **kwargs)
