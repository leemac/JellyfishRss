define([
  'jquery', 
  'underscore',
  'backbone',
  'views/controls'
], function($, _, Backbone, ControlsView){

	var view = Backbone.View.extend({
		initialize: function(options){
			this.vent = options.vent;

			this.vent.bind("subscriptionAdded", this.subscriptionAdded, this);
			this.vent.bind("subscription:unsubscribe", this.subscriptionUnsubscribed, this);

			this.template = _.template($("#sidebar-template").html());
			this.render();

			this.controlsView = new ControlsView({vent: this.vent, el: "#controls" });   
		},
		events: {
			"click .subscription" : "clickSubscription"
		},
		clickSubscription: function (ev) {
			this.vent.trigger("clickSubscription", ev.target);
		},
		subscriptionAdded: function () {
			this.refreshItems();
		},
		subscriptionUnsubscribed: function () {
			this.refreshItems();		
		},
		refreshItems : function ()
		{
			var element = $(this.el);

			var ref = this;
			
			$.ajax({
				type: "POST",
				url : "http://localhost:8000/api/get_folders",
				data : {
					csrfmiddlewaretoken: window.getCSRF(),
					user_id: window.get_userId()
				},
				success: function (msg) {
					var source   = $("#folder-template").html();
					var folderTemplate = _.template(source);

					var source   = $("#subscription-template").html();
					var subscriptionTemplate = _.template(source);

					var html = "";

					html += folderTemplate({ id: 0, title: "All Items"});

					for(var i = 0; i < msg.length; i ++)
					{		
						// Todo: Temporary (may be omitted for MVP)
						// html += folderTemplate(msg[i]);

						var subscriptions = msg[i].subscriptions;

						for(var n = 0; n < subscriptions.length; n++)
						{
							html += subscriptionTemplate(subscriptions[n])
						}
					}

					element.find(".sidebar-content").html(html);

					ref.vent.trigger("sidebarLoaded");
				}
			});

		},

		render: function() {

			var element = $(this.el);
			var ref = this;

			element.html(this.template());

			this.refreshItems();

		    return this;
		},
	});

	return view;
});

