var azureSearchAccount="<Azure Search Account Name>";
var azureSearchQueryApiKey = "<Azure Search API Admin Key>";
var indexNameCaptions="<Azure Search Index Name>";
var contentid = "<Batch Name>";

var inSearch = false;
function init()
{
	var searchAPI = "https://" + azureSearchAccount + ".search.windows.net/indexes/" + indexNameCaptions + "/docs?$top=1000&$select=id,contentid,beginsec,begin,end,caption&$count=true&$orderby=beginsec&api-version=2015-02-28&$filter=contentid%20eq%20%27" + contentid + "%27";
	inSearch= true;

    $.ajax({
        url: searchAPI,
        beforeSend: function (request) {
            request.setRequestHeader("api-key", azureSearchQueryApiKey);
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("Accept", "application/json; odata.metadata=none");
        },
        type: "GET",
        success: function (data) {
			$( "#colcontainer2" ).html('');
			$( "#colcontainer2" ).append('<ul class="list-group">');
			for (var item in data.value)
			{
				var id = data.value[item].id;
                var caption = data.value[item].caption;
				var beginsec = data.value[item].beginsec;
				var begin = data.value[item].begin;
				var end = data.value[item].end;

                if (caption !='' ) {
                    $( "#colcontainer2" ).append( 
                        '<li>[<a href="#" id="hoge" onclick=\"restart(' + beginsec + ');\">'
                        + begin + ' - ' +  end + '</a>] ' + caption + '</li>');
			    }
			}
            $( "#colcontainer2" ).append('</ul>');
			inSearch= false;
        }
    });
}

function execSearch()
{
	var q = encodeURIComponent($("#q").val());
	var searchAPI = "https://"+ azureSearchAccount +".search.windows.net/indexes/" + indexNameCaptions + "/docs?$top=1000&$select=id,contentid,beginsec,begin,end,caption&$count=true&$orderby=beginsec&highlight=caption&api-version=2015-02-28&$filter=contentid%20eq%20%27" + contentid + "%27&search=" + q;
	inSearch= true;

    $.ajax({
        url: searchAPI,
        beforeSend: function (request) {
            request.setRequestHeader("api-key", azureSearchQueryApiKey);
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("Accept", "application/json; odata.metadata=none");
        },
        type: "GET",
        success: function (data) {
			$( "#hits2" ).html('');
            $( "#hits2" ).append( 'hits: ' + data['@odata.count']);
			$( "#colcontainer2" ).html('');
			$( "#colcontainer2" ).append('<ul class="list-group">');
			for (var item in data.value)
			{
				var id = data.value[item].id;
                var caption = data.value[item].caption;
                if ( '@search.highlights' in data.value[item] ){
				    caption = data.value[item]['@search.highlights'].caption;
                }
				var beginsec = data.value[item].beginsec;
				var begin = data.value[item].begin;
				var end = data.value[item].end;

                $( "#colcontainer2" ).append( 
                    '<li>[<a href="#" id="hoge" onclick=\"restart(' + beginsec + ');\">'
                    + begin + ' - ' +  end + '</a>] ' + caption + '</li>');
			}
            $( "#colcontainer2" ).append('</ul>');
			inSearch= false;
        }
    });


}
