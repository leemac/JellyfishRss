define([
  'jquery', 
  'underscore',
  'backbone',
  'text!views/templates/modal.add.html'
], function($, _, Backbone, htmlAdd){

	var AddSubscriptionView = Backbone.View.extend({

		initialize: function(options){
			this.vent = options.vent;
			this.template = _.template(htmlAdd);
		},

		events : {
			"click .button-ok" : "buttonOkClick",
			"click .button-cancel" : "buttonCancelClick"
		},

		buttonOkClick: function () 
		{
			this.addNewUrl();
		},

		addNewUrl: function () {

		},

		buttonCancelClick: function () 
		{
			$(this.el).find('#window-add-subscription').modal('hide')
		},

		render: function() {

			var element = $(this.el);
			var ref = this;

			element.html(this.template());

			$(this.el).find('#window-add-subscription').modal('show')
			$(this.el).find('.input-add-subscription').val("");
			$(this.el).find('.input-add-subscription').focus();
			$(this.el).find(".alert").hide();

			$(this.el).find('.input-add-subscription').keyup(function (e) {
				if(e.which === 13) {	
					console.log('adding...');
	    			ref.addNewUrl();
	  			}	
			});
		    return this;
		},
	});

	return AddSubscriptionView;

});