define([
  'jquery',
  'underscore',
  'backbone',
  'views/sidebar',
  'views/explorer',
  'views/add.subscription',
  'text!views/templates/app.html'
], function($, _, Backbone, SideBarView, ExplorerView, AddSubscriptionView, htmlApp){

	var AppView = Backbone.View.extend({
		el: "#app",

		initialize: function() {
		    this.template = _.template(htmlApp);

		    this.vent = _.extend({}, Backbone.Events);

		    this.render();

		    // View Setup
		    this.sidebarView = new SideBarView({vent: this.vent, el: "#sidebar" });
		    this.explorerView = new ExplorerView({vent: this.vent, el: "#content" });
		},
        events : {
            "click .button-add" : "addSubscription"
        },
        addSubscription: function () {
            this.modalView = new AddSubscriptionView({vent: this.vent, el: "#app-modal" });
        },
		render: function() {
		    $(this.el).html(this.template());
		}
	});

	return AppView;
});