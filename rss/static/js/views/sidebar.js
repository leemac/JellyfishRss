define([
  'jquery', 
  'underscore',
  'backbone',
  'views/controls',
  'text!views/templates/sidebar.html',
  'text!views/templates/sidebar.folder.html',
  'text!views/templates/sidebar.item.html'
], function($, _, Backbone, ControlsView, htmlSidebar, htmlFolder, htmlItem){

	var view = Backbone.View.extend({
		initialize: function(options){
			this.vent = options.vent;

			this.vent.bind("subscriptionAdded", this.subscriptionAdded, this);
			this.vent.bind("subscription:unsubscribe", this.subscriptionUnsubscribed, this);

			this.template = _.template(htmlSidebar);

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
					var folderTemplate = _.template(htmlFolder);
					var subscriptionTemplate = _.template(htmlItem);

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
			this.$el.html(this.template());

			this.refreshItems();

		    return this;
		},
	});

	return view;
});

