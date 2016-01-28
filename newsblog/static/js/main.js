var map;

/*
Sample javascript to load markers manually from features and from geoJSON
*/
var geoJsonVectorSource;
var geojsonFeatures = [];
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

   	//Display the layer
    map.addLayer(newLayer);

    /*
    This block loads markers manually from definitions in code
    */

    //initialize an array of features
    var iconFeatures=[];

    //define a start point
    var startPoint = new ol.geom.Point(ol.proj.transform([-72.0704, 46.678], 'EPSG:4326',     
  		'EPSG:3857'))
    //define a feature
	var iconFeature = new ol.Feature({
  		geometry: startPoint,
  		name: 'Null Island',
  		population: 4000,
  		rainfall: 500
	});

	//define a end point
	var endPoint = new ol.geom.Point(ol.proj.transform([-73.1234, 45.678], 'EPSG:4326',     
  		'EPSG:3857'))
	//another feature
	var iconFeature1 = new ol.Feature({
  		geometry: endPoint,
  		name: 'Null Island Two',
  		population: 4001,
  		rainfall: 501
	});
	//put it in the array
	iconFeatures.push(iconFeature);
	iconFeatures.push(iconFeature1);

	//define a vector source using the list of features earlier
	var vectorSource = new ol.source.Vector({
  		features: iconFeatures //add an array of features
	});

	//define a style for the marker
	var iconStyle = new ol.style.Style({
  		image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
    	anchor: [0.5, 46],
    	anchorXUnits: 'fraction',
    	anchorYUnits: 'pixels',
    	opacity: 0.75,
    	src: 'marker-icon.png'
  		}))
	});

	//define the layer using the vectorSource as source and iconStyle as style
	var vectorLayer = new ol.layer.Vector({
  		source: vectorSource,
  		style: iconStyle
	});

	//display the layer
	map.addLayer(vectorLayer);

	/*
	This block draws line with the point defined above
	*/
	//feature array
	var lineFeatures = [];

	//Define the coordinates from the points already defined
	var points = new Array(
			startPoint.getCoordinates(),
			endPoint.getCoordinates()
		);
	
	//define a line feature with a line string geometry using the points array
	var lineFeature = new ol.Feature({
						geometry: new ol.geom.LineString(points)
	});

	//add the line feature to the line array
	lineFeatures.push(lineFeature);

	//style for the line
	var lineStyle = new ol.style.Style({
		stroke: new ol.style.Stroke({
			color: '#ffcc33',
			width: 2
		})
	});

	//define a new source for the line layer
	var lineSource = new ol.source.Vector({
		features: lineFeatures
	});

	//define the layer
	var lineLayer = new ol.layer.Vector({
		source: lineSource,
		style: lineStyle
	});
	
	//display the layer
	map.addLayer(lineLayer);
	/*
	This block loads marker from a geoJSON file
	*/

	//define a geoJSON file as a source of features

	geoJsonVectorSource = new ol.source.Vector({
		url: 'test.geojson',
		format: new ol.format.GeoJSON({
					defaultDataProjection: 'EPSG:4326',
					projection: 'EPSG:3857'
				})
	});

	//define the style for 'Point' features in the geojson file
	var styles = {
		'Point': [iconStyle],
		'LineString': [lineStyle]
	};

	//use function to determine what feature use what style. The mapping is put on the styles dictionary
	var styleFunction = function(feature, resolution) {
  		return styles[feature.getGeometry().getType()];
	};

	//define a vector layer using the geoJsonVectorSource as a source and using the styleFunction as the style
	var geoJsonVectorLayer = new ol.layer.Vector({
		title:'test',
		source: geoJsonVectorSource,
		style: styleFunction
	});


	//display the layer
	map.addLayer(geoJsonVectorLayer);

	/*
	This block renders a line string between the points from geojson.
	The process had to wait for the geojsonsource done loading.
	*/
	geoJsonVectorLayer.getSource().on('change', function(evt){
		var source = evt.target;
		if(source.getState() === 'ready') {
			geojsonFeatures = source.getFeatures();
			var geojsonCoords = [];
			for (var i = geojsonFeatures.length - 1; i >= 0; i--) {
				console.log('Getting coordinates from geojson features');
				geojsonCoords.push(geojsonFeatures[i].getGeometry().getCoordinates())
			};
			// alert('length is ' + geojsonCoords);
			var geojsonLineFeature = new ol.Feature({
					geometry: new ol.geom.LineString(geojsonCoords)
			});
			var geojsonLineFeatures = [];
			geojsonLineFeatures.push(geojsonLineFeature);
			var geojsonLineSource = new ol.source.Vector({
				features: geojsonLineFeatures
			});
			var geojsonLineLayer = new ol.layer.Vector({
				source: geojsonLineSource,
				style: lineStyle
			});
			map.addLayer(geojsonLineLayer);
		}
	});

	
}