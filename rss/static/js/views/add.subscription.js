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
		var value = $(this.el).find('.input-add-subscription').val();
		if(value === "")
			return;

		var viewRef = this;

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/add_subscription",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				url: value,
				user_id: window.get_userId()
			},
			beforeSend: function (){
				
			},
			success: function (msg) {
				viewRef.vent.trigger("subscriptionAdded");
				$(viewRef.el).find('#window-add-subscription').modal('hide')
			},
			error: function () {
				console.log('error!');
			}
		});
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
		$(this.el).find('.input-add-subscription').text("");
		$(this.el).find('.input-add-subscription').focus();
	    return this;
	},
});