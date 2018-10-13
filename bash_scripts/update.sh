#!/bin/bash

## DESCRIPTION: Updates HA in a virtual environment
## AUTHOR: Jon Bullen (Source: https://gist.github.com/sytone/ed33774edc25846782913319bfdb7df6)
## Modifications: Rohan Kapoor

declare -r SCRIPT_NAME=$(basename "$BASH_SOURCE" .sh)

## exit the shell(default status code: 1) after printing the message to stderr
bail() {
    echo -ne "$1" >&2
    exit ${2-1}
}

## help message
## help message
declare -r HELP_MSG="Usage: $SCRIPT_NAME [OPTION]... [ARG]...
  -h    display this help and exit
  -u    Update HA with the specified version.
  version
Example:
  bash ./updatehs.sh -u

"


## print the usage and exit the shell(default status code: 2)
usage() {
    declare status=2
    if [[ "$1" =~ ^[0-9]+$ ]]; then
        status=$1
        shift
    fi
    bail "${1}$HELP_MSG" $status
}

while getopts ":hu" opt; do
    case $opt in
        h)
            usage 0
            ;;
        \?)
            usage "Invalid option: -$OPTARG \n"
            ;;
        u)
            shift
            version=$1
            echo "Updating Home Assistant"
            cd /etc/homeassistant
            source /srv/homeassistant/bin/activate
            if [ "$version" = "" ]; then
                pip3 install --upgrade homeassistant
            else
                pip3 install homeassistant==${version}
            fi
            ;;

    esac
done