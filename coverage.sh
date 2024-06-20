#!/bin/bash

open_report() {
    case "$OSTYPE" in
        "linux-gnu"*)
            xdg-open $1
            ;;
        "darwin"*)
            open $1
            ;;
        *)
            start $1
            ;;
    esac
}

print_red() {
    echo -e "\033[41;37m$1\033[0m"
}

print_red "Running unit tests for Django"
rm -rf htmlcov
coverage run --source='.' manage.py test
coverage report -m
coverage html
rm .coverage
open_report htmlcov/index.html

print_red "Running unit tests for JavaScript"
rm -rf coverage
npm run test
open_report coverage/lcov-report/index.html

cd htmlcov || exit
rm .gitignore