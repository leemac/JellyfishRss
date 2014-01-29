define([
  'jquery', 
  'underscore',
  'backbone'
], function($, _, Backbone){

	var SettingsView = Backbone.View.extend({
		initialize: function(options){
			this.vent = options.vent;
			this.template = _.template($("#settings-template").html());
		},

		events : {
			"click .button-save" : "buttonSaveClick",
			"click .button-cancel" : "buttonCancelClick"
		},

		buttonSaveClick: function () 
		{
			alert('save settings!');
		},

		buttonCancelClick: function () 
		{
			$(this.el).find('#window-settings').modal('hide')
		},

		render: function() {

			var element = $(this.el);
			var ref = this;

			element.html(this.template());
			
			$(this.el).find('#window-settings').modal('show')

		    return this;
		},
	});

	return SettingsView;
});