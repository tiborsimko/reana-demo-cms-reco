# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

valid_run_years = ["2010", "2011", "2012"]

datasets = {"DoubleElectron": "'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/RAW/v1/000/160/433/C046161E-0D4E-E011-BCBA-0030487CD906.root'"}

global_tags = {"2011": "FT_53_LV5_AN1"}

cmssw_releases = {"2011": "5_3_32"}

workflow_engines = ["serial", "cwl", "yadage"]


def get_config(year, data):

    return {'directory_name': get_directory_name(year, data),
            'year': validate_year(year),
            'cmssw_version': get_cmssw_release(year),
            'global_tag': get_global_tag(year),
            'dataset_file': get_datafile(data)
            }


def validate_workflow_engine(workflow_engine):
    if workflow_engine in workflow_engines:
        return workflow_engine
    else:
        raise ValueError("Workflow engine {} is not supported."
                         .format(workflow_engine))


def get_directory_name(year, data):
    return "cms-reco-{}-{}".format(data, year)


def get_global_tag(year):
    if year in global_tags:
        return global_tags[year]
    else:
        raise ValueError("The year does not correspond to any global tag")


def get_cmssw_release(year):
    if year in cmssw_releases:
        return cmssw_releases[year]
    else:
        raise ValueError("The year does not correspond to any CMSSW release")


def get_datafile(data):
    if data in datasets:
        return datasets[data]
    else:
        raise ValueError("Data not in data sets")


def validate_year(year):
    if year in valid_run_years:
        return year
    else:
        raise ValueError("Not a valid run year")

