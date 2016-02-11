#!/bin/bash -x

echo "Running landsat_parse.sh " $*
mkdir /tmp/data
tar -C /tmp/data -zxvf $1
NM=$(basename -s _MTL.txt /tmp/data/*_MTL.txt)
cp /tmp/data/${NM}* $2/

# write results manifest
DATE_STARTED=$(grep DATE_ACQUIRED /tmp/data/${NM}_MTL.txt | awk '{print $3}')T$(grep TIME /tmp/data/${NM}_MTL.txt | awk '{print $3}' | tr -d '"')

cat > $2/results_manifest.json << EOF
{ "version": "1.1",
  "output_data": [{
    "name": "b1-coastal",
    "file": {
        "path": "$2/${NM}_B1.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }, {
    "name": "b2-blue",
    "file": {
        "path": "$2/${NM}_B2.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }, {
    "name": "b3-green",
    "file": {
        "path": "$2/${NM}_B3.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }, {
    "name": "b4-red",
    "file": {
       "path": "$2/${NM}_B4.TIF",
       "geo_metadata": {
           "data_started": "${DATE_STARTED}"
       }
    }
  }, {
    "name": "b5-nir",
    "file": {
      "path": "$2/${NM}_B5.TIF",
      "geo_metadata": {
          "data_started": "${DATE_STARTED}"
      }
    }
  }, {
     "name": "b6-swir1",
     "file": {
         "path": "$2/${NM}_B6.TIF",
         "geo_metadata": {
             "data_started": "${DATE_STARTED}"
         }
     }
  }, {
    "name": "b7-swir2",
    "file": {
      "path": "$2/${NM}_B7.TIF",
      "geo_metadata": {
          "data_started": "${DATE_STARTED}"
      }
    }
  }, {
    "name": "b8-panchromatic",
    "file": {
        "path": "$2/${NM}_B8.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }, {
    "name": "b9-cirrus",
    "file": {
     "path": "$2/${NM}_B9.TIF",
     "geo_metadata": {
         "data_started": "${DATE_STARTED}"
     }
    }
  }, {
    "name": "b10-tir1",
    "file": {
        "path": "$2/${NM}_B10.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }, {
    "name": "b11-tir2",
    "file": {
        "path": "$2/${NM}_B11.TIF",
        "geo_metadata": {
            "data_started": "${DATE_STARTED}"
        }
    }
  }],
  "parse_results": [{
    "filename": "$1",
    "file-types": ["landsat","msi","pan","tir"],
    "geo_metadata": {
        "data_started": "${DATE_STARTED}"
    }}
  ]
}
EOF
cat -n $2/results_manifest.json

rm -rf /tmp/data
