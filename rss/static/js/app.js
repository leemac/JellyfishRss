define([
  'jquery', 
  'underscore',
  'backbone',
  'views/sidebar',
  'views/explorer',
  'views/controls',
  'text!views/templates/app.html'
], function($, _, Backbone, SideBarView, ExplorerView, ControlsView, htmlApp){

	var AppView = Backbone.View.extend({
		el: "#app",

		initialize: function() {
		    this.template = _.template(htmlApp);

		    this.vent = _.extend({}, Backbone.Events);
		          
		    this.render();

		    // View Setup   
		    this.sidebarView = new SideBarView({vent: this.vent, el: "#sidebar" });    
		    this.explorerView = new ExplorerView({vent: this.vent, el: "#content" }); 
			this.controlsView = new ControlsView({vent: this.vent, el: "#controls" });     
		},

		render: function() {
		    $(this.el).html(this.template());
		},
	});

	return AppView;
});