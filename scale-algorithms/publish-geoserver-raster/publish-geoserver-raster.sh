#!/bin/bash

echo "Pushing to geoserver: " $1
curl —=form "file=@$1" http://10.4.4.100:9000/importraster/