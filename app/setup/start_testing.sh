#!/bin/sh

cp ./db/pipo.db ./db/pipo_bk.db
mv ./db/pipo.db ./db/pipo_pre_test.db
python3 ./setup/testing.py
