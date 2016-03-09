# landsat-hotspots.py
# Description: Detect and output TIR anomalies from Landsat 8 band 11
# Author: Tony Wolf and Chris Dickman, Applied Information Sciences
# Date: January 2016

import sys
import os
import struct
import osgeo.gdal as gdal
import json
from datetime import datetime

# Open the input dataset
infname = sys.argv[1]
base, ext = os.path.splitext(os.path.basename(infname))
outfname = os.path.join(sys.argv[2],"%s_hotspots%s" % (base, ext))

starttime = datetime.utcnow()

dataset = gdal.Open(infname)
print ">>Dataset Loaded                    OK"

# Create the output dataset
driver = gdal.GetDriverByName( "GTiff" )
print ">>Generated Output File to Memory   OK"
# Get the spatial information from the input file
geoTransform=None
geoProjection=None

try:
    geoTransform = dataset.GetGeoTransform()
except:
    print "Unable to load geotransform"
try:
    geoProjection = dataset.GetProjection()
except:
    print "Unable to load projection"

print ">>Retrieving Spatial Transforms     OK"

# Create an output file of the same size as the inputted
# image but with only 1 output image band.
newDataset = driver.Create(outfname, dataset.RasterXSize, dataset.RasterYSize,1, gdal.GDT_Float32)
print ">>Creating Output Image             OK"

# Set spatial information of the new image.
if geoTransform:
    newDataset.SetGeoTransform(geoTransform)
if geoProjection:
    newDataset.SetProjection(geoProjection)
if newDataset is None:
    print "ERROR: Could not create output image"

# Get the TIR band
tir_band = dataset.GetRasterBand(1) # TIR BAND

print ">>Reading Bands                     OK"
print ">>Exploiting TIR Anomalies..."

# Loop through each line in turn.
numLines = tir_band.YSize
for line in range(numLines):
    # Define variable for output line.
    outputLine = ''
    # Read in data for the current line from the TIR file
    tir_scanline = tir_band.ReadRaster( 0, line, tir_band.XSize, 1, tir_band.XSize, 1, gdal.GDT_Float32)
    # Unpack the line of data to be read as floating point data
    tir_tuple = struct.unpack('f' * tir_band.XSize, tir_scanline)

    # Loop through the columns within the image
    for i in range(len(tir_tuple)):
        # Get the intensity for the current pixel.
        hotspots = (tir_tuple[i])

        pixel = 0
        # Be careful of zero divide
        if hotspots == 0 or hotspots < 24000 or hotspots > 24500 :
            pixel = 0
        else:
            pixel = hotspots
        # Add the current pixel to the output line
        outputLine = outputLine + struct.pack('f', pixel)
    # Write the completed line to the output image
    newDataset.GetRasterBand(1).WriteRaster(0, line, tir_band.XSize, 1, outputLine, buf_xsize=tir_band.XSize, buf_ysize=1, buf_type=gdal.GDT_Float32)
    # Delete the output line following write
    del outputLine

print ">>TIR Analysis Complete"
print ">>Writing Data to Cube              OK"
newDataset.FlushCache()
vsiFile=gdal.VSIFOpenL(outfname,"r")
i=0
while gdal.VSIFSeekL(vsiFile,0,os.SEEK_END)>0:
    i+=1
fileSize=gdal.VSIFTellL(vsiFile)
gdal.VSIFSeekL(vsiFile,0,os.SEEK_SET)
outputs=gdal.VSIFReadL(fileSize,1,vsiFile)

print ">>Processing Completed Successfully"

endtime = datetime.utcnow()

# Create results manifest for Scale
results = { "version": "1.1",
            "output_data": [{
                "name": "hotspots",
                "file": {
                    "path": outfname,
                    "geo_metadata": {
                        "data_started": "%sZ" % starttime.isoformat(),
                        "data_ended": "%sZ" % endtime.isoformat()
                    }
                }
            }]
            }

json.dump(results, open(os.path.join(sys.argv[2],"results_manifest.json"), "w"))
