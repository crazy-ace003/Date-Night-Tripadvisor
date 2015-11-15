// We need this to build our post string
var querystring = require('querystring');
var http = require('http');
var fs = require('fs');

function PostCode(lat, lon, subcat, distance) {
  // Build the post string from an object
  if(subcat){
  	var post_data = querystring.stringify({
  		'subcategory':subcat,
  		'distance':distance
  	});
  }
  else{
	  var post_data = querystring.stringify({
	  	'distance':distance
	  });
	}

  // An object of options to indicate where to post to
  var post_options = {
      host: 'api.tripadvisor.com/api/partner',
      port: '80',
      path: '/2.0/map/' + lat + ',' lon + '/attractions?key=567d3eed-93f9-4cbf-abd4-79d10281a58e',
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(post_data)
      }
  };

  var result = null;

  // Set up the request
  var post_req = http.request(post_options, function(res) {
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
          result = chunk;
      });
  });

  // post the data
  post_req.write(post_data);
  post_req.end();

}
