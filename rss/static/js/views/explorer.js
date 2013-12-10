var ExplorerView = Backbone.View.extend({
	initialize: function(options){
		this.setElement( this.el );
		this.vent = options.vent;

		this.vent.bind("clickSubscription", this.clickSubscription);

		this.template = Handlebars.compile($("#explorer-template").html());
		this.render();
	},

	events : {
		"click .subscription-explorer-node" : "openItem"
	},

	openItem: function (e) {
		var target = e.target;
		// Todo, fix with proper view
		var url = $(target).parents(".subscription-explorer-node").attr("js-item-link");
		
		window.location = url;
	},
	clickSubscription: function (target) {
		var subscriptionid = $(target).attr("js-subscription-id");

		if(subscriptionid === undefined)
			return;

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/get_subscription_items",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				subscription_id: subscriptionid
			},
			beforeSend: function (){
				$("#explorer").html("");
				$("#explorer").html("<img src='/static/images/explorer_loading.gif' />");
			},
			success: function (msg) {
				$("#explorer").html("");

				// Todo, fix with proper view
				var source   = $("#item-template").html();
				var template = Handlebars.compile(source);

				for(var i = 0; i < msg.length; i ++)
				{		
					var html = template(msg[i]);

					$("#explorer").append(html);
				}
			}
		});
	},

	render: function() {
		var element = this.el;
		$(element).append(this.template());

		return this;
	},
});