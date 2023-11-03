#!/bin/bash
#
# This file is part of REANA.
# Copyright (C) 2019, 2023 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

check_script () {
    shellcheck run-tests.sh
}

check_pydocstyle () {
    pydocstyle cms_reco
}

check_pytest () {
    python setup.py test
}

check_all () {
    check_script
    check_pydocstyle
    check_pytest
}

if [ $# -eq 0 ]; then
    check_all
    exit 0
fi

for arg in "$@"
do
    case $arg in
        --check-shellscript) check_script;;
        --check-pydocstyle) check_pydocstyle;;
        --check-pytest) check_pytest;;
        *)
    esac
done
