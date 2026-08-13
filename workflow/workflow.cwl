#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  reco_tool: File

outputs:
  result.root:
    type: File
    outputSource: step1/result.root
  step1.log:
    type: File
    outputSource: step1/step1.log

steps:
  step1:
    run: step1.cwl
    in:
      reco_tool: reco_tool
    out: [result.root, step1.log]
