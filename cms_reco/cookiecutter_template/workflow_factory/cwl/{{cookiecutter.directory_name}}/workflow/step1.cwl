class: CommandLineTool
cwlVersion: v1.0

requirements:
  - class: DockerRequirement
    dockerPull: cmsopendata/cmssw_{{cookiecutter.cmssw_version}}

baseCommand:
  - /bin/zsh

inputs:
  - id: reco_tool
    type: File

arguments:
  - position: 0
    prefix: '-c'
    valueFrom: |
      source /opt/cms/cmsset_default.sh ;\
      scramv1 project CMSSW CMSSW_{{cookiecutter.cmssw_version}} ;\
      cd CMSSW_{{cookiecutter.cmssw_version}}/src ;\
      eval `scramv1 runtime -sh` ;\
      ln -sf /cvmfs/cms-opendata-conddb.cern.ch/{{cookiecutter.global_tag}}_RUNA {{cookiecutter.global_tag}} ;\
      ln -sf /cvmfs/cms-opendata-conddb.cern.ch/{{cookiecutter.global_tag}}_RUNA.db {{cookiecutter.global_tag}}_RUNA.db ;\
      ls -l ;\
      ls -l /cvmfs/ ;\
      scp ../../../../$(inputs.reco_tool.basename) . ;\
      cmsRun $(inputs.reco_tool.basename) ;\

outputs:
  - id: DoubleMu.root
    type: File
    outputBinding:
      glob: CMSSW_{{cookiecutter.cmssw_version}}/src/reco_RAW2DIGI_L1Reco_RECO_USER.root
  - id: step1.log
    type: stdout

stdout: step1.log