#!/usr/env/bin python3

import os
from random import randint
from shutil import copytree, rmtree

from lib.layers import TerraformTarget

def temporary_directory(func):
    _dir = os.path.realpath(os.path.dirname(__file__))
    terraform_dir = os.path.join(_dir, "terraform")
    temp_dir = os.path.join(_dir, f"terraform-tmp-test-{randint(0,10000000)}")
    def wrapper():
        try:
            copytree(terraform_dir, temp_dir)
            func(temp_dir)
        finally:
            rmtree(temp_dir)
    return wrapper

@temporary_directory
def test_get_output(dirname):
    state_file = os.path.join(dirname,
                              "terraform.tfstate")
    vars_file = os.path.join(dirname,
                             "terraform.tfvars")
    with open(vars_file, "w") as f:
        f.write('content = "sample-content"')
    target = TerraformTarget("module.fake_module",
                             vars_file,
                             state_file,
                             dirname)
    outputs = target.apply()
    assert outputs['file_content'] == "sample-content"
