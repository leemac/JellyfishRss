var SubscriptionItemView = Backbone.View.extend({
	initialize: function(options, el){
		this.vent = options.vent;
		this.el = options.el;

		this.vent.bind("clickSubscription", this.clickSubscription, this);
		this.vent.bind("sidebarLoaded", this.sidebarLoaded, this);

		this.template = Handlebars.compile($("#explorer-template").html());

		this.render();
	},

	events : {
		"click .subscription-explorer-node" : "openItem",
		"click .button-mark-all-read" : "markAllAsRead"
	},

	sidebarLoaded : function () {
		this.subscriptionId = 0;
		this.subscriptionTitle = "All Items";

		$(".subscription").removeClass("selected");
		$(".subscription").first().addClass("selected");

		this.loadItems();
	},

	markAllAsRead : function () {
		var ref = this;

		var exploreElement = $(this.el).find(".feed");
		var titleElement = $(this.el).find(".title");

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/mark_subscription_read",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				subscription_id: ref.subscriptionId
			},
			beforeSend: function (){
				exploreElement.html("");
				exploreElement.html("<div class='loading'>Marking all as read...<br/><br/><img src='/static/images/explorer_loading.gif' /></div>");
			},
			success: function (msg) {
				exploreElement.html("");
				titleElement.html(ref.subscriptiontitle);
				
				ref.loadItems();
			}
		});
	},

	loadItems: function ()
	{		
		var exploreElement = $(this.el).find(".feed");
		var titleElement = $(this.el).find(".title");

		var ref = this;

		$.ajax({
			type: "POST",
			url : "http://localhost:8000/api/get_subscription_items",
			data : {
				csrfmiddlewaretoken: getCSRF(),
				subscription_id: ref.subscriptionId
			},
			beforeSend: function (){
				exploreElement.html("");
				exploreElement.html("<div class='loading'><img src='/static/images/explorer_loading.gif' /></div>");
			},
			success: function (msg) {
				exploreElement.html("");
				titleElement.html(ref.subscriptionTitle);

				// Todo, fix with proper view
				if(msg.length === 0)
				{
					var source   = $("#item-template-none").html();
					var template = Handlebars.compile(source);
					var html = template();
					exploreElement.html(html);

					return;
				}
				else if(ref.subscriptionId == 0)
					templateName = "item-template-all";
				else
					templateName = "item-template";

				var source   = $("#" + templateName).html();
				var template = Handlebars.compile(source);

				for(var i = 0; i < msg.length; i ++)
				{		
					var html = template(msg[i]);

					exploreElement.append(html);
				}

				$(".button-favorite").click(function () {
					alert("favorite marked..")
				});
				//$("abbr.timeago").timeago();
			}
		});
	},

	openItem: function (e) {
		var target = e.target;
		// Todo, fix with proper view
		var url = $(target).parents(".subscription-explorer-node").attr("js-item-link");
		
		window.location = url;
	},
	clickSubscription: function (target) {
		var thisLinkElement = $(target);

		var subscriptionid = thisLinkElement.attr("js-subscription-id");
		if(subscriptionid === undefined)
			return;

		$(".subscription").removeClass("selected");
		thisLinkElement.addClass("selected");

		this.subscriptionId = subscriptionid
		this.subscriptionTitle = thisLinkElement.attr("js-subscription-title");

		this.loadItems();
	},

	render: function() {
		var element = this.el;
		$(element).html(this.template());

		return this;
	},
});