#!/bin/sh
#
# This file is part of REANA.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#ToDo: use the branches for different years as tests cases

pydocstyle cms_reco && \
isort -rc -c -df **/*.py && \
cms-reco --help > cmd_list.txt && \
diff -q -w docs/cmd_list.txt cmd_list.txt  && \
rm cmd_list.txt && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test && \
sphinx-build -qnNW -b doctest docs docs/_build/doctest