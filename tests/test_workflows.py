# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from tests.utils_test import workflow_test


def test_2011_doubleelectron_serial():
    reference_repo = 'https://raw.githubusercontent.com/' \
                     'dprelipcean/reana-demo-cms-reco/' \
                     'reana_example_2011/workflow/reana.yaml'

    workflow_test(recid=46, reference_repo=reference_repo,
                  local_file_name="reana_cwl.yaml",
                  workflow_engine="serial",
                  to_delete=True)


def test_2011_doubleelectron_cwl():
    reference_repo = 'https://raw.githubusercontent.com/' \
                     'dprelipcean/reana-demo-cms-reco/' \
                     'reana_example_2011/workflow/reco.cwl'

    workflow_test(recid=46, reference_repo=reference_repo,
                  local_file_name="reana_cwl.yaml",
                  workflow_engine="cwl",
                  to_delete=True)


