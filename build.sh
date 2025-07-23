#!/bin/bash
source ~/miniforge3/etc/profile.d/conda.sh  # adjust path to match your install
conda activate stairs_app_env
which python
pyinstaller windows-app.spec
read -p "Press any key to continue..."