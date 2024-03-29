#!/usr/bin/env sh

version=`cat .HA_VERSION`
if [ "$version" = "" ]; then
    python3 -m pip install --disable-pip-version-check homeassistant
else
    python3 -m pip install --disable-pip-version-check homeassistant==${version}
fi
