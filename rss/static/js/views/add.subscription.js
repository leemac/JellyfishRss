var AddSubscriptionView = Backbone.View.extend({

	initialize: function(options){
		this.vent = options.vent;
		this.template = Handlebars.compile($("#add-subscription-template").html());
	},

	events : {
		"click .button-ok" : "buttonOkClick",
		"click .button-cancel" : "buttonCancelClick"
	},

	buttonOkClick: function () 
	{
		alert('subscription added!');
	},

	buttonCancelClick: function () 
	{
		$(this.el).find('#window-add-subscription').modal('hide')
	},

	render: function() {

		var element = $(this.el);
		var ref = this;

		element.append(this.template());

		$(this.el).find('#window-add-subscription').modal('show')

	    return this;
	},
});