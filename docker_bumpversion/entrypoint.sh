#!/bin/sh


git config --global user.email "bumpversion@hudya.io" &&  git config --global user.name "Bumpversion"

echo "Cd Bumpversion"
cd /etc/bump/src/

echo "Dry run"
bumpversion $1 --dry-run --verbose

echo "Bumpversion"
bumpversion $1