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
			url : "http://localhost:8000/api/get_subscriptions",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				user_id: window.get_userId()
			},
			beforeSend: function (){
				
			},
			success: function (msg) {
				var source   = $("#subscription-node-template").html();
				var template = Handlebars.compile(source);

				var html = "";
				for(var i = 0; i < msg.length; i ++)
				{		
					html += template(msg[i]);
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