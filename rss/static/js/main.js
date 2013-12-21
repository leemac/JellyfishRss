
require.config({
  paths: {
    jquery: 'jquery.min',    
    underscore: 'underscore.min',
    backbone: 'backbone.min',
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
  		'app',
	], 
	function(App){
		App.initialize();
	}
);
