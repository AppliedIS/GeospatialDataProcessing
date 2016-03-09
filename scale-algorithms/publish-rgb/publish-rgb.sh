#!/bin/bash

echo "Pushing to geoserver: " $1
curl --form "file=@$1;" --form "store=landsat" http://10.4.4.100:3000/mosaic/update
