(function () {
var nav = navigator.appVersion;
var navverif = "" + nav.split(";")[1];
var IE6 = false;
var flagImgProcess = false;
OpenLayers.Layer.WorldWind = OpenLayers.Class.create();
OpenLayers.Layer.WorldWind.prototype = OpenLayers.Class.inherit(OpenLayers.Layer.Grid, {
DEFAULT_PARAMS: {}, isBaseLayer: true,
lzd: null,
zoomLevels: null,
t: null,
initialize: function (name, url, lzd, zoomLevels, params, options, t) {
this.lzd = lzd;
this.zoomLevels = zoomLevels;
this.t = t;
var newArguments = new Array();
newArguments.push(name, url, params, options);
OpenLayers.Layer.Grid.prototype.initialize.apply(this, newArguments);
this.params = (params ? params : {});
if (params) {
OpenLayers.Util.applyDefaults(this.params, this.DEFAULT_PARAMS);
}
}, addTile: function (bounds, position) {
if (this.map.getResolution() <= (this.lzd / 512) && this.getZoom() <= this.zoomLevels) {
var url = this.getURL(bounds);
return new OpenLayers.Tile.Image(this, position, bounds, url, this.tileSize);
} else {
return new OpenLayers.Tile.Image(this, position, bounds, OpenLayers.Util.getImagesLocation() + "blank.gif", this.tileSize);
}
}, getZoom: function () {
var zoom = this.map.getZoom();
var extent = this.map.getMaxExtent();
zoom = zoom - Math.log(this.maxResolution / (this.lzd / 512)) / Math.log(2);
return zoom;
}, getURL: function (bounds) {
var zoom = this.getZoom();
var extent = this.map.getMaxExtent();
var deg = this.lzd / Math.pow(2, this.getZoom());
var x = Math.floor((bounds.left - extent.left) / deg);
var y = Math.floor((bounds.bottom - extent.bottom) / deg);
if (this.map.getResolution() <= (this.lzd / 512) && this.getZoom() <= this.zoomLevels) {
return this.getFullRequestString({
L: zoom,
X: x,
Y: y,
T: this.t
});
} else {
return OpenLayers.Util.getImagesLocation() + "blank.gif";
}
}, CLASS_NAME: "OpenLayers.Layer.WorldWind"
});
