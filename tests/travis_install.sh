#!/usr/bin/env bash

version = `cat .HA_VERSION`
if [ "$version" = "" ]; then
    pip3 install homeassistant
else
    pip3 install homeassistant==${version}
fi