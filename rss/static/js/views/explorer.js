var ExplorerView = Backbone.View.extend({
	initialize: function(options, el){
		this.vent = options.vent;
		this.el = options.el;

		this.vent.bind("clickSubscription", this.clickSubscription, this);

		this.template = Handlebars.compile($("#explorer-template").html());
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

		this.render();
		
		var exploreElement = $(this.el).find("#explorer");

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/get_subscription_items",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				subscription_id: subscriptionid
			},
			beforeSend: function (){
				exploreElement.html("");
				exploreElement.html("<img src='/static/images/explorer_loading.gif' />");
			},
			success: function (msg) {
				exploreElement.html("");

				// Todo, fix with proper view
				var source   = $("#item-template").html();
				var template = Handlebars.compile(source);

				for(var i = 0; i < msg.length; i ++)
				{		
					var html = template(msg[i]);

					exploreElement.append(html);
				}
			}
		});
	},

	render: function() {
		var element = this.el;
		$(element).html(this.template());

		return this;
	},
});