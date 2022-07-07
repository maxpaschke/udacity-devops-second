#!/usr/bin/env bash

git clone git@github.com:maxpaschke/udacity-devops-second.git
cd udacity-devops-second/
make all
az webapp up --name udacityWebApp123467 --resource-group Azuredevops --runtime "PYTHON:3.7"