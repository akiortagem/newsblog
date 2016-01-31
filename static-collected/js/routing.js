var map;
function init(){

	//Initialize map
    map = new ol.Map({
        target:'map',
        renderer:'canvas',
    	view: new ol.View({
    		projection: 'EPSG:3857',
    		center:ol.proj.transform([106.8227, -6.1745], 'EPSG:4326', 'EPSG:3857'),
    		zoom:5
    	})
    });
    //Initialize map layer
    var newLayer = new ol.layer.Tile({
    	source: new ol.source.OSM()
   	});
   	//Display the layers
    map.addLayer(newLayer);
    var fixesLayer = loadFixes();
    map.addLayer(fixesLayer);
    routeLayer = initRouteLayer();
    map.addLayer(routeLayer);
    var coordinates=[];
    var lineSource;
    var features = [];
    var distances = [];
    // lineSource = debug_GetLineSource();
    // routeLayer.setSource(lineSource);
    fixesLayer.getSource().on('change', function(evt){
		var fixesSource = evt.target;
		if(fixesSource.getState() === 'ready') {
			var endpoints = getEndPoints(fixesSource)
			features.push(endpoints.departure)
			coordinates.push(endpoints.departure.getGeometry().getCoordinates())
    		map.on('singleclick', function(evt){
    			var feature = map.forEachFeatureAtPixel(evt.pixel,
    			function(feature, layer){
    				return feature;
    			});
    			if(feature){
    				// alert('from inside');
    				// console.log('coordinate is ' + feature.getGeometry().getCoordinates());
    				features.push(feature);
   					tempCoordinates = getRoutesCoordinates(coordinates, fixesSource, feature.getGeometry().getCoordinates());
   					for (var i = 0; i < tempCoordinates.length; i++) {
   						coordinates.push(tempCoordinates[i]);
   					};
   					console.log('Route summary');
   					var disp = ""
   					for (var i = 0; i < features.length; i++) {
   						disp += features[i].get('name')
   						if(i < features.length - 1){
   							disp += " -> "
   						}
   					};
   					console.log(disp)
   					var distance = getDistance(coordinates[coordinates.length-1], coordinates[coordinates.length-2])
   					distances.push(distance)
   					console.log("Distance between last fixes are : " + distance)
   					console.log('------------------------------------------------');
   					// console.log('coordinates are :')
   					// for (var i = 0; i < coordinates.length; i++) {
   					// 	console.log(coordinates[i])
   					// };
   					// console.log('------------------------------------------------');
					// console.log('coordinate length is ' + coordinates.length);
   					lineSource = getLineSource([
   						coordinates[coordinates.length-1],
   						coordinates[coordinates.length-2]
   						]);
   					map.addLayer(initRouteLayer(lineSource));
   					routeLayer.setSource(lineSource);
   					if (feature.get('name') == 'Arrival'){
   						alert('Routing done!');
   						var geojson = serializeToGeoJson(features);
   						var maxDistance = Math.max.apply(Math, distances);
   						alert('max distance : ' + maxDistance);
   					}
    			}
    		});
		}
	});

}

function loadFixes(){
	//define a geoJSON file as a source of features
	geoJsonVectorSource = new ol.source.Vector({
		url: 'http://54.169.221.217/static/json/jkt-palembang.geojson',
		format: new ol.format.GeoJSON({
					defaultDataProjection: 'EPSG:4326',
					projection: 'EPSG:3857'
				})
	});

	var image = new ol.style.Circle({
  		radius: 5,
  		fill: null,
  		stroke: new ol.style.Stroke({color: 'red', width: 1})
	});

	var endpoint = new ol.style.Circle({
  		radius: 5,
  		fill: new ol.style.Fill({
        	color: '#93a3ce'
      	}),
  		stroke: new ol.style.Stroke({color: 'red', width: 1})
	});

	//define the style for 'Point' features in the geojson file
	var styles = {
		'Point': [new ol.style.Style({
			image: image
		})],
		'EndPoint': [new ol.style.Style({
			image: endpoint
		})]
	};

	//use function to determine what feature use what style. The mapping is put on the styles dictionary
	var styleFunction = function(feature, resolution) {
		var style;
		if (feature.get('name') == 'Arrival' || feature.get('name') == 'Departure'){
			style = styles['EndPoint'];
		} else {
			style = styles['Point'];
		}
  		return style;
	};

	//define a vector layer using the geoJsonVectorSource as a source and using the styleFunction as the style
	var geoJsonVectorLayer = new ol.layer.Vector({
		title:'test',
		source: geoJsonVectorSource,
		style: styleFunction
	});

	//display the layer
	return geoJsonVectorLayer;
}

function getEndPoints(geoJsonVectorSource){
	geojsonFeatures = geoJsonVectorSource.getFeatures();
	for (var i = geojsonFeatures.length - 1; i >= 0; i--) {
		if(geojsonFeatures[i].get('name') == 'Departure'){
			var departure = geojsonFeatures[i];
		}
		if(geojsonFeatures[i].get('name') == 'Arrival'){
			var arrival = geojsonFeatures[i];
		}
	}
	var endpoints = {
		departure: departure,
		arrival: arrival
	};
	return endpoints;
}

function getRoutesCoordinates(coordList, geoJsonVectorSource, clickedCoordinates){

	var routeCoordinates=[];
	// if(coordList.length == 0){
	// 	// console.log('coordinates in route is zero adding departure coordinates');
	// 	geojsonFeatures = geoJsonVectorSource.getFeatures();
	// 	for (var i = geojsonFeatures.length - 1; i >= 0; i--) {
	// 		if(geojsonFeatures[i].get('name') == 'Departure'){
	// 			var departure = geojsonFeatures[i];
	// 		}
	// 		if(geojsonFeatures[i].get('name') == 'Arrival'){
	// 			var arrival = geojsonFeatures[i];
	// 		}
	// 	}
	// 	var departureArrival = {
	// 		departure: departure,
	// 		arrival: arrival
	// 	};
	// 	routeCoordinates.push(departureArrival.departure.getGeometry().getCoordinates());
	// }
	// console.log('routeCoordinates are :')
	// for (var i = 0; i < routeCoordinates.length; i++) {
	// 	console.log(routeCoordinates[i])
	// };
	// console.log('------------------------------------------------');
	routeCoordinates.push(clickedCoordinates);
	// console.log('routeCoordinates are :')
	// for (var i = 0; i < routeCoordinates.length; i++) {
	// 	console.log(routeCoordinates[i])
	// };
	// console.log('------------------------------------------------');	
	// console.log('added new coordinates in routes, is now : ' + routeCoordinates);
	return routeCoordinates;
}

function initRouteLayer(source){
	var lineStyle = new ol.style.Style({
		stroke: new ol.style.Stroke({
			color: '#ffcc33',
			width: 2
		})
	});

	var features = []
	if(!source){
		var source = new ol.source.Vector({
			features: features
		});
	}

	var layer = new ol.layer.Vector({
		source: source,
		style: lineStyle
	});
	return layer;
}

function getLineSource(coordinates){
	// console.log('in getLineSource');
	var lineFeatures = [];
	// var line = new ol.geom.LineString(coordinates, 'XY');
	// console.log('after creating line');
	for (var i = 0; i < coordinates.length - 1; i++) {
		// console.log('starting point is now ' + coordinates[i]);
		var tempLine = new ol.Feature({
			geometry: new ol.geom.LineString(
				[coordinates[i], coordinates[i+1]], 'XY'
				)
		});
		// console.log('drawing line from ' + coordinates[i] + ' to ' + coordinates[i+1]);
		lineFeatures.push(tempLine);
	};
	// var lineFeature = new ol.Feature({
	// 	geometry: line
	// });
	// // console.log('after creating lineFeature');
	// lineFeatures.push(lineFeature);
	var source = new ol.source.Vector({
		features: lineFeatures
	});
	// console.log('after creating source');
	return source;
}

function serializeToGeoJson(features){
	var geojson = new ol.format.GeoJSON;
	var json = geojson.writeFeatures(features);
	return json;
}

function getDistance(point1, point2){
	var wgs84Sphere = new ol.Sphere(6378137);
	distance = wgs84Sphere.haversineDistance(point1, point2)
	return distance;
	// point1 = new ol.geom.Point(point1).transform("EPSG:3857", "EPSG:4326");
	// point2 = new ol.geom.Point(point2).transform("EPSG:3857", "EPSG:4326");
	// return point1.distanceTo(point2);
}

function debug_GetLineSource(){
	var coordinates = new Array(
			[ 11891155.6162683, -688544.7507928677 ],
			[ 11811661.106851716, -632287.0979749772 ],
			[ 11789647.242705585, -557684.5583686454 ],
			[ 11724828.642719757, -500203.913098194 ],
			[ 11680800.914427495, -451284.21499567933 ],
			[ 11667347.997449301, -399918.53198804124 ],
			[ 11660010.042733926, -332653.9470970863 ]
		);
	var lineFeatures = [];
	for (var i = 0; i < coordinates.length - 1; i++) {
		// console.log('starting point is now ' + coordinates[i]);
		var tempLine = new ol.Feature({
			geometry: new ol.geom.LineString(
				[coordinates[i], coordinates[i+1]], 'XY'
				)
		});
		// console.log('drawing line from ' + coordinates[i] + ' to ' + coordinates[i+1]);
		lineFeatures.push(tempLine);
	};
	// var lineFeature = new ol.Feature({
	// 	geometry: line
	// });
	// // console.log('after creating lineFeature');
	// lineFeatures.push(lineFeature);
	var source = new ol.source.Vector({
		features: lineFeatures
	});
	// console.log('after creating source');
	return source;
}