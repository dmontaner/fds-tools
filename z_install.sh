#!/bin/bash
# z_make_install.sh
# 2018-08-15 david.montaner@gmail.com
# install from tar.gz

echo "BORRANDO"
sudo -H pip3 uninstall fds-tools

echo "INSTALANDO"
cd dist
fichero=`ls *.tar.gz | tail -n 1`  # latest tar.gz
# sudo -H pip3 install --upgrade $fichero
sudo -H pip3 install --upgrade --no-deps $fichero
