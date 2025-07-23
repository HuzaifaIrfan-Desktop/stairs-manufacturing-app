#!/bin/bash
source ~/miniforge3/etc/profile.d/conda.sh  # adjust path to match your install
conda activate stairs_app_env
which python
python main.py
read -p "Press enter to continue"