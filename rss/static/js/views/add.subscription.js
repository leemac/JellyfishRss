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

            this.render();
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

			var alertBox = $(this.el).find(".alert");

			var value = $(this.el).find('.input-add-subscription').val();
			if(value === "")
            {
				alertBox.addClass("alert-danger");
				alertBox.removeClass("alert-success");

				alertBox.html("<strong>Empty Feed:</strong> Please enter a valid feed URL.");
				alertBox.show();

                return;
            }

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
				url : "/api/add_subscription",
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

					buttons.attr("disabled", false);
				}
			});
		},
        destroy_view: function() {
            this.undelegateEvents();

            this.$el.removeData().unbind();

            //Remove view from DOM
            this.remove();
            Backbone.View.prototype.remove.call(this);
        },
		buttonCancelClick: function () 
		{
			$(this.el).find('#window-add-subscription').modal('hide')
            this.destroy_view();
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
		}
	});

	return AddSubscriptionView;

});