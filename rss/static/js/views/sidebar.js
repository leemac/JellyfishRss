var SideBarView = Backbone.View.extend({

	initialize: function(options){
		this.vent = options.vent;
		this.template = Handlebars.compile($("#sidebar-template").html());
		this.render();
	},

	events: {
		"click .subscription-node" : "clickSubscription"
	},

	clickSubscription: function (ev) {
		this.vent.trigger("clickSubscription", ev.target);
	},

	render: function() {

		var element = this.el;
		$(element).append(this.template());

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

				$("#sidebar").html(html);
			}
		});

	    return this;
	},
});