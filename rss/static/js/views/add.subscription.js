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
		this.addNewUrl();
	},

	addNewUrl: function () {
		var value = $(this.el).find('.input-add-subscription').val();
		if(value === "")
			return;

		var alertBox = $(this.el).find(".alert");

		if(value.indexOf("http://") === -1)
		{
			alertBox.addClass("alert-danger");
			alertBox.removeClass("alert-success");

			alertBox.html("<strong>Invalid Feed:</strong> Please enter a valid feed URL.");
			alertBox.show();
			return;
		}

		var viewRef = this;

		var buttons = $(viewRef.el).find(".button-ok, .button-cancel");

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/add_subscription",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				url: value,
				user_id: window.get_userId()
			},
			beforeSend: function (){
				alertBox.removeClass("alert-danger");
				alertBox.addClass("alert-success");

				alertBox.html("<strong>Importing Feed...</strong>");
				alertBox.show();

				buttons.attr("disabled", false);
			},
			success: function (msg) {
				viewRef.vent.trigger("subscriptionAdded");
				$(viewRef.el).find('#window-add-subscription').modal('hide')
				
				buttons.attr("disabled", true);
			},
			error: function () {
				alertBox.addClass("alert-danger");
				alertBox.removeClass("alert-success");

				alertBox.html("<strong>Error Importing Feed:</strong> Please try again!");
				alertBox.show();

				buttons.attr("disabled", true);
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