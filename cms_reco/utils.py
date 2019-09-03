# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Reana workflow factory helper functions."""

import json
import os
import sys
import shutil
import subprocess as sp
import urllib.request as ur

import jq

with open("{0}/cms_reco/validation.json".format(os.getcwd())) \
        as validation_file:
    validation_data = json.load(validation_file)

    valid_run_years = validation_data["years"]
    workflow_engines = validation_data["workflow_engines"]
    compute_backends = validation_data["compute_backends"]


def get_config_from_json():
    """Get the needed configuration variables from the COD client config."""
    with open('{0}/cms_reco/cms-reco-config.json'.format(os.getcwd())) \
            as config_file:
        data = json.load(config_file)
        conf = {'error': None}

        try:
            conf['directory_name'] = custom_directory_name(data)
            conf['year'] = get_year(data)
            conf['cmssw_version'] = get_cms_release(data)
            conf['global_tag'] = get_global_tag(data)
            conf['dataset_file'] = get_dataset(data)
        except Exception as e:
            conf['error'] = "Cannot retrieve config due to: {0}".format(e)

        return conf


def get_global_tag(data):
    """Get the global tag for the CMS cond db."""
    return jq.jq(".metadata.system_details.global_tag").transform(data)


def get_cms_release(data):
    """Get the CMS SW release version."""
    # keep only the version number
    return jq.jq(".metadata.system_details.release").transform(data)[6:]


def download_index_file(data, local_file_name, file_format="txt"):
    """Download the index file from COD platform."""
    recid = get_recid(data)
    url = get_index_file_name(data, recid, file_format)
    if not os.path.isfile(local_file_name):
        ur.urlretrieve(url, local_file_name)
        return local_file_name


def remove_additionally_generated_files(files):
    """Remove files that the end user does not need."""
    if os.path.isfile(files):
        os.remove(files)


def remove_folder(mydir):
    """Remove folder."""
    shutil.rmtree(mydir)


def get_index_file_name(data, recid, file_format):
    """Get the dataset specific index file name."""
    if file_format == "txt":
        index_file = jq.jq(".metadata._files").transform(data)[1]["key"]
        url = "http://opendata.cern.ch/record/{0}//files/{1}" \
            .format(recid, index_file)
        return url


def get_dataset(data, local_file_name="./index.txt"):
    """Get a data set file name from the index file."""

    download_index_file(data, local_file_name)
    dataset = choose_dataset_from_file(local_file_name)

    remove_additionally_generated_files(local_file_name)

    return dataset


def choose_dataset_from_file(local_file_name):
    """Chose a specific dataset from file."""
    with open("{0}/{1}".format(os.getcwd(), local_file_name)) as file:
        # use the first dataset in the index file
        dataset = file.readline()
    return dataset


def get_recid(data):
    """Get the record id."""
    return jq.jq(".id").transform(data)


def get_title(data):
    """Get the data set title."""
    return jq.jq(".metadata.title").transform(data)


def get_year(data):
    """Get creation year for the data set."""
    return jq.jq(".metadata.date_created").transform(data)[0]


def get_name_from_title(title):
    """Get the data set name from the title."""
    return os.path.dirname(os.path.dirname(title))[1:]


def custom_directory_name(data):
    """Return a custom directory name based on the title."""
    return "cms-reco-{}-{}".format(get_name_from_title(get_title(data)),
                                   get_year(data))


def load_config_from_cod(recid, config_file):
    """Get the config file using cern open data client."""
    _cod_client = "cernopendata-client"
    _get_config_cmd = "get-record --recid"
    sp.call("{0} {1} {2} | tee {3}"
            .format(_cod_client, _get_config_cmd, recid, config_file),
            shell=True)


def run_analysis(directory_name):
    """Run the analysis on reana."""
    sp.call("cd {0} && reana-client run reana.yaml"
            .format(directory_name),
            shell=True)


def run_pipeline(recid, directory):
    """Run the full pipeline."""
    _cms_reco_client = "cms-reco"
    sp.call("{0} load-config --recid {1} "
            "&& {0} create-workflow --directory {2} "
            "&& {0} run-reco --directory {2}"
            .format(_cms_reco_client, recid, directory),
            shell=True)
