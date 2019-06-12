#!/usr/bin/env python3

import os
import sys
from lib.astronomer_deployment import AstronomerDeployment

def apply(vars_file, state_path):
    astronomer = AstronomerDeployment(vars_file,
                                      state_path)
    astronomer.deploy()

def main():
    # This code is temporary, used for
    # testing before we build the CLI
    _dir = os.path.dirname(os.path.realpath(__file__))
    # vars_file = input("path to vars file: ")
    vars_file = os.path.join(
        _dir,
        "environments/google/steven-gcp.tfvars")
    state_file = os.path.join(
        _dir,
        "states",
        "terraform.tfstate")
    apply(vars_file, state_file)


if __name__ == "__main__":
    main()
