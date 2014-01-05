var SideBarView = Backbone.View.extend({

	initialize: function(options){
		this.vent = options.vent;

		this.vent.bind("subscriptionAdded", this.subscriptionAdded, this);

		this.template = Handlebars.compile($("#sidebar-template").html());
		this.render();

		this.controlsView = new ControlsView({vent: this.vent, el: "#controls" });   
	},

	events: {
		"click .subscription-node" : "clickSubscription"
	},

	clickSubscription: function (ev) {
		this.vent.trigger("clickSubscription", ev.target);
	},

	subscriptionAdded: function () {
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
				csrfmiddlewaretoken: getCSRF(),
				user_id: window.get_userId()
			},
			beforeSend: function (){
				
			},
			success: function (msg) {
				var source   = $("#folder-template").html();
				var folderTemplate = Handlebars.compile(source);

				var source   = $("#subscription-template").html();
				var subscriptionTemplate = Handlebars.compile(source);

				var html = "";

				html += folderTemplate({ id: 0, title: "All Items"});

				for(var i = 0; i < msg.length; i ++)
				{		
					html += folderTemplate(msg[i]);

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