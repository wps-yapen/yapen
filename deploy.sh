#!/usr/bin/env bash

git     add -A

git     add -f ./.secrets/

eb      deploy --profile fc-8th-eb --staged

git     reset HEAD ./.secrets/