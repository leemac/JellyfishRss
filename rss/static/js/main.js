
require.config({
  baseURl: 'static/js',
  urlArgs: "bust=" + (new Date()).getTime(),
  paths: {
    jquery: 'vendor/jquery.min',    
    underscore: 'vendor/underscore.min',
    backbone: 'vendor/backbone.min',
    text: 'vendor/require.text.min'
  },
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ["underscore", "jquery"],
      exports: "Backbone"
    }
  }
});

require(
	[
      "jquery",
      "underscore",
      "backbone",
  		'app',
	], 
	function($, _, Backbone, app){
      new app();
	}
);
