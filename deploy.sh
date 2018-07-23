#!/usr/bin/env bash

echo "deploy 시작 및 전체 파일 staged로 만듬"
git     add -A
git     add -f ./.secrets/
git     status
eb      deploy --profile wps-yapen --staged
echo "deploy 완료"
git     reset head ./.secrets/
git     reset head ./requirements.txt
echo "secrets,requ파일 재외"
git     status
echo "확인바람"