#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of reana.
# Copyright (C) 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
import sys

import click

from cookiecutter.main import cookiecutter

from .utils import validate_workflow_engine, get_config


@click.group()
def cms_reco():
    """Info"""
    pass

@click.option('--workflow_engine',
              help='year the data set was recorded')
@click.option('--nevents',
              help='number of events to be reconstructed')
@click.option('--dataset',
              help='data set to be reconstructed')
@click.option('--year',
              help='year the data set was recorded')
@cms_reco.command()
def create_workflow(year='2011', dataset="DoubleElectron", nevents='1', workflow_engine='serial'):
    workflow_engine = validate_workflow_engine(workflow_engine)
    template_path = "{}/cms_reco/cookiecutter_template/workflow_factory/{}"\
        .format(os.getcwd(), workflow_engine)

    config = get_config(year, dataset)

    print("Created `cms-reco-{}-{}` directory.".format(dataset, year))

    if nevents:
        config['nevents'] = nevents

    cookiecutter(template_path,
                 no_input=True,
                 extra_context=config
                 )
