#!/bin/bash
# z_make_distribution.sh
# 2018-08-15 david.montaner@gmail.com
# prepare pip distribution

# virtualenv venv --system-site-packages
# venv/bin/activate

rm -r fds_tools.egg-info   # some cache seems to be here
# rm -r dist
python3 setup.py sdist      # build distribution file

cd dist

latest=`ls *.tar.gz | tail -n 1`  # latest tar.gz
datest="${latest%.tar.gz}"        # name of the extracted dir

tar -xzf $latest
tree     $datest
rm -r    $datest
# tar -xzOf $latest | tree   # this does not work
