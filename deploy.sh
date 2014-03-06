#!/bin/bash
virtualenv cveenv
script_dir=`dirname $0`
cd $script_dir
/bin/bash -c ". ../cve/cveenv/bin/activate && python setup.py install; exec /bin/bash -i"

