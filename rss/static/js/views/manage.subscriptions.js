var ManageSubscriptionsView = Backbone.View.extend({

	initialize: function(options){
		this.vent = options.vent;
		this.el = options.el;

		this.template = Handlebars.compile($("#manage-subscriptions-template").html());
	},

	events : {
		"click .button-ok" : "buttonOkClick",
		"click .button-cancel" : "buttonCancelClick"
	},

	buttonOkClick: function () 
	{
		
	},

	buttonCancelClick: function () 
	{
		
	},

	render: function() {
		$(this.el).html(this.template());

	    return this;
	},
});