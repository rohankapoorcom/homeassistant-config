#!/bin/bash
/usr/bin/ssh -o StrictHostKeyChecking=accept-new -i /srv/homeassistant/.ssh/id_ed25519 lprint@001-lprint-01.dev.rohankapoor.com "convert -size 673x378 -background white -fill black -font 'AvantGarde-Book' -gravity Center label:'$1' label.png;/snap/bin/lprint -d 'DYMO LabelWriter 450 DUO Label' label.png -n '$2'"