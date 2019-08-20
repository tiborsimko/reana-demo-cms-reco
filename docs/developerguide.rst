.. _developerguide:

Developer guide
===============

Using latest ``cms-reco`` version
-------------------------------------

If you want to use the latest bleeding-edge version of ``cms-reco``, without
cloning it from GitHub, you can use:

.. code-block:: console

    $ # create new virtual environment
    $ virtualenv ~/.virtualenvs/myreana
    $ source ~/.virtualenvs/myreana/bin/activate
    $ # install reana-commons and reana-client
    $ pip install git+git://github.com/reanahub/reana-demo-cms-reco.git@master#egg=cms-reco
