#!/usr/bin/env cwl-runner

# Note that if you are working on the analysis development locally, i.e. outside
# of the REANA platform, you can proceed as follows:
#
#   $ mkdir cwl-local-run
#   $ cd cwl-local-run
#   $ cp -a ../workflow/input.yml .
#   # change path for hte input file, e.g. by using sed
#   $ sed -i 's/reco_cmsdriver2011.py/..\/..\/reco_cmsdriver2011.py/g' input.yml
#   $ cp -a ../reco_cmsdriver2011.py .
#   $ cwltool --quiet --outdir="../results" ../workflow/workflow.cwl input.yml


cwlVersion: v1.0
class: Workflow

inputs:
  reco_tool: File

outputs:
  result.root:
    type: File
    outputSource:
      step1/result.root
  step1.log:
    type: File
    outputSource:
      step1/step1.log


steps:
  step1:
    run: step1.cwl
    in:
      reco_tool: reco_tool
    out: [DoubleMu.root, step1.log]
