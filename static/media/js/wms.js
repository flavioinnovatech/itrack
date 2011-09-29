function load_wms() {

	var wms = new OpenLayers.Layer.Google("Google Streets", // the default
	{
		layers: "map",
		numZoomLevels : 20
	});


	return wms;
}
