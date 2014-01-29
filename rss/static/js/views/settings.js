define([
  'jquery', 
  'underscore',
  'backbone',
  'text!views/templates/modal.settings.html'
], function($, _, Backbone, htmlSettings){

	var SettingsView = Backbone.View.extend({
		initialize: function(options){
			this.vent = options.vent;
			this.template = _.template(htmlSettings);
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