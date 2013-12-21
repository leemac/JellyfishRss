var ControlsView = Backbone.View.extend({
	initialize: function(options){		
		this.vent = options.vent;
		this.template = Handlebars.compile($("#controls-template").html());
		this.render();
	},

	events : {
		"click .button-add" : "buttonAddClick",
		"click .button-settings" : "buttonSettingsClick",
		"click .button-logout" : "buttonLogoutClick"
	},

	buttonLogoutClick : function () {
		window.location = "http://" + window.location.host + "/logout"
	},
	buttonSettingsClick: function () 
	{
		this.settingsView.render();
	},
	buttonAddClick: function () 
	{
		this.addSubscriptionView.render();
	},
	
	render: function() {
		var element = this.el;

		this.settingsView = new SettingsView({ el: "#modal"});

		this.addSubscriptionView = new AddSubscriptionView({ vent: this.vent, el: "#modal"});

		var controlsObj = { 
			username: get_userName()
		}

		$(element).html(this.template(controlsObj));

		return this;
	},
});