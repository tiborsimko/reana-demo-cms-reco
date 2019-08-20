# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import filecmp
import os
import subprocess as sp
import urllib.request as ur

from cms_reco.utils import remove_additionally_generated_files, remove_folder


def generate_file(recid=46, directory='test'):
    """Generate the reana.yaml using the workflow factory."""
    _cms_reco_client = "cms-reco"

    sp.call("{0} load-config --recid {1} "
            "&& {0} create-workflow --directory {2} "
            .format(_cms_reco_client, recid, directory),
            shell=True)
    workflow_file = "{0}/reana.yaml".format(directory)
    if os.path.isfile(workflow_file):
        return workflow_file
    else:
        return None


def download_existing_file(url, local_file_name='reference.yaml'):
    """Get a well known and working reana.yaml workflow file."""
    ur.urlretrieve(url, local_file_name)
    return local_file_name


def compare_files(ref_file, gen_file):
    """Compare two files for their content."""
    return filecmp.cmp(ref_file, "{0}".format(gen_file), shallow=False)


def test_workflow_2011():
    """Test for the year 2011."""
    ref_file = download_existing_file(
        'https://raw.githubusercontent.com/dprelipcean/'
        'reana-demo-cms-reco/reana_example_2011/reana.yaml')

    tmp_folder = "test"
    gen_file = generate_file(recid=46, directory=tmp_folder)

    assert compare_files(ref_file, gen_file)

    remove_additionally_generated_files(ref_file)
    remove_folder(tmp_folder)
