#!/bin/bash

if [[ `uname` == 'Darwin' || `uname` == 'Linux' ]]; then
    dropdb insider_test
    createdb insider_test
else
    dropdb -U postgres insider_test
    createdb -U postgres insider_test
fi

source sync_and_migrate.sh
