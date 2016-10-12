#!/bin/sh

. ./search.conf

SERVICE_NAME=$SEARCH_SERVICE_NAME
ADMIN_KEY=$SEARCH_API_KEY
API_VER='2015-02-28'
CONTENT_TYPE='application/json'
URL="https://$SERVICE_NAME.search.windows.net/indexes?api-version=$API_VER"

curl -s\
 -H "Content-Type: $CONTENT_TYPE"\
 -H "api-key: $ADMIN_KEY"\
 -XPOST $URL -d'{
    "name": "ocr",
    "fields": [
        { "name":"id", "type":"Edm.String", "key": true, "searchable": false, "filterable":false, "facetable":false },
        { "name":"sessionid", "type":"Edm.String","searchable": false, "filterable":true, "facetable":false },
        { "name":"beginsec", "type":"Edm.Int32", "searchable": false, "filterable":false, "sortable":true, "facetable":false },
        { "name":"begin", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
        { "name":"end", "type":"Edm.String", "searchable": false, "filterable":false, "sortable":false, "facetable":false },
        { "name":"caption", "type":"Edm.String", "searchable": true, "filterable":false, "sortable":false, "facetable":false, "analyzer":"ja.microsoft" }
     ],
     "corsOptions": {
        "allowedOrigins": ["*"],
        "maxAgeInSeconds": 300
    }
}'
