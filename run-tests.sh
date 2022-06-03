#!/bin/sh
#
# This file is part of REANA.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#ToDo: use the branches for different years as tests cases

pydocstyle cms_reco && \
python setup.py test
