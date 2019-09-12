# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Reana workflow factory helper functions."""


import json
import logging
import os
import shutil
import subprocess as sp
import traceback
import urllib.request as ur
from random import randint

import jq

try:
    validation_file = open(f"{os.getcwd()}/cms_reco/cod-validation.json")
except FileNotFoundError:
    validation_file = open(f"{os.getcwd()}/../cms_reco/cod-validation.json")

logging.debug("Fetching validation data from {0}".format(validation_file))
validation_data = json.load(validation_file)

valid_run_years = validation_data["years"]
valid_workflow_engines = validation_data["workflow_engines"]
valid_compute_backends = validation_data["compute_backends"]
valid_file_selection = validation_data["file_selection"]

validation_file.close()


def get_config_from_json(file_selection):
    """Get the needed configuration variables from the COD client config."""
    try:
        config_file = open(f"{os.getcwd()}/cms_reco/cms-reco-config.json")
    except FileNotFoundError:
        config_file = open(f"{os.getcwd()}/../cms_reco/cms-reco-config.json")

    logging.debug("Fetching config data from {0}".format(config_file))

    data = json.load(config_file)
    conf = {'error': None}

    try:
        conf['directory_name'] = custom_directory_name(data)
        conf['year'] = get_year(data)
        conf['cmssw_version'] = get_cms_release(data)
        conf['global_tag'] = get_global_tag(data)
        conf['dataset_file'] = get_dataset(data, file_selection)
    except Exception as e:
        conf['error'] = "Cannot retrieve config due to: {0}".format(e)
        traceback.print_exc()

    return conf


def get_global_tag(data):
    """Get the global tag for the CMS cond db."""
    return jq.jq(".metadata.system_details.global_tag").transform(data)


def get_cms_release(data):
    """Get the CMS SW release version."""
    # The slicing is needed to keep only the version number
    return jq.jq(".metadata.system_details.release").transform(data)[6:]


def download_index_file(data, local_file_name, file_format):
    """Download the index file from COD platform."""
    recid = get_recid(data)
    url = get_index_file_name(data, recid, file_format)
    if not os.path.isfile(local_file_name):
        ur.urlretrieve(url, local_file_name)
        return local_file_name


def remove_additionally_generated_files(file):
    """Remove files that the end user does not need."""
    if os.path.isfile(file):
        os.remove(file)


def remove_folder(mydir):
    """Remove folder."""
    shutil.rmtree(mydir)


def get_index_file_name(data, recid, file_format):
    """Get the dataset specific index file name."""
    if file_format == "json":
        index_file = jq.jq(".metadata._files").transform(data)[0]["key"]
    elif file_format == "txt":
        index_file = jq.jq(".metadata._files").transform(data)[1]["key"]
    else:
        index_file = None

    url = "http://opendata.cern.ch/record/{0}//files/{1}" \
        .format(recid, index_file)
    return url


def get_dataset(data, file_selection, local_file_name="./index",
                file_format="json"):
    """Get a data set file name from the index file."""
    local_file_name += f".{file_format}"
    logging.debug(f"Fetching data set as {local_file_name}")

    download_index_file(data, local_file_name, file_format)
    dataset = choose_dataset_from_file(file_selection, local_file_name)

    remove_additionally_generated_files(local_file_name)

    return dataset


def choose_dataset_from_file(file_selection, local_file_name):
    """Chose a specific data set from file."""
    if ".txt" in local_file_name:
        logging.debug("Fetching .txt format.")

        # File selection is not supported in the .txt format, as there is no
        # information stored about the size of the data files
        with open("{0}/{1}".format(os.getcwd(), local_file_name)) as file:
            # use the first dataset in the index file
            dataset = file.readline()
    elif ".json" in local_file_name:
        logging.debug("Fetching .json format.")

        with open("{0}/{1}".format(os.getcwd(), local_file_name)) as file:
            index_data = json.load(file)
            logging.debug("File selection is: {}".format(file_selection))

            if file_selection == "first":
                dataset = index_data[0]['uri']
            elif file_selection == "smallest":
                # This sorts by file size, with smallest first
                index_data = sorted(index_data, key=lambda i: i['size'])
                dataset = index_data[0]['uri']
            elif file_selection == "largest":
                # This sorts by file size, with smallest first
                index_data = sorted(index_data, key=lambda i: i['size'])
                dataset = index_data[-1]['uri']
            elif file_selection == "random":
                dataset_number = randint(0, len(index_data))
                dataset = index_data[dataset_number]['uri']
            elif file_selection == "all":
                raise NotImplementedError
            else:
                dataset = None
    else:
        dataset = None

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


def get_template(workflow_engine):
    """Get the template directory."""
    dir_path = os.getcwd()
    if 'tests' in dir_path:
        dir_path = dir_path.replace("/tests", "")

    return f"{dir_path}/cms_reco/cookiecutter_template/" \
           f"workflow_factory/{workflow_engine}"
