var ControlsView = Backbone.View.extend({
	initialize: function(options){
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

		this.settingsView = new SettingsView({ el: this.el});
		this.addSubscriptionView = new AddSubscriptionView({ el: this.el});

		var controlsObj = { 
			username: get_userName()
		}

		$(element).append(this.template(controlsObj));

		return this;
	},
});