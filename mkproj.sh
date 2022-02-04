#!/bin/bash

# Author: Vikram Bhagavatula
# Date: 2022-02-03
# Description: Simple shell script to make project/hw directories with the following structure:
#
#       homework-3/
#       ├── Makefile
#       ├── defaults.yaml
#       ├── hw3.md
#       ├── pdfs/
#       └── src/


mkdir "$1";
cp './Makefile' "$1";
cp './defaults.yaml' "$1";
cd "$1";
touch "$1.md";
mkdir pdfs;
mkdir src;
