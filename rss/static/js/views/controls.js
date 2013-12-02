var ControlsView = Backbone.View.extend({
	initialize: function(options){
		this.template = Handlebars.compile($("#controls-template").html());
		this.render();
	},

	events : {
		"click .button-settings" : "buttonSettingsClick"
	},

	buttonSettingsClick: function () 
	{
		this.settingsView.render();
	},
	
	render: function() {
		var element = this.el;

		this.settingsView = new SettingsView({ el: this.el});

		var controlsObj = { 
			username: get_userName()
		}

		$(element).append(this.template(controlsObj));

		return this;
	},
});