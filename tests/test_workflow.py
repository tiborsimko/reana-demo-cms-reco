# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from cms_reco.utils import remove_additionally_generated_files, remove_folder
from tests.utils_test import (compare_files, download_existing_file,
                              generate_file)


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
