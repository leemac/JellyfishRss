define([
  'jquery', 
  'underscore',
  'backbone',
  'views/sidebar',
  'views/explorer'
], function($, _, Backbone, SideBarView, ExplorerView){

	var AppView = Backbone.View.extend({
		el: "#app",

		initialize: function() {
		    this.template = _.template($("#app-template").html());

		    this.vent = _.extend({}, Backbone.Events);
		          
		    this.render();

		    // View Setup   
		    this.sidebarView = new SideBarView({vent: this.vent, el: "#sidebar" });    
		    this.explorerView = new ExplorerView({vent: this.vent, el: "#content" });     

		    this.render();
		},

		render: function() {
		    $(this.el).html(this.template());
		},
	});

	return AppView;
});