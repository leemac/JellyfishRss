define([
  'jquery', 
  'underscore',
  'backbone',
  'text!views/templates/explorer.html',
  'text!views/templates/explorer.row.all.html',
  'text!views/templates/explorer.row.none.html'
], function($, _, Backbone, htmlExplorer, htmlRowAll, htmlRowNone){

	var ExplorerView = Backbone.View.extend({
		initialize: function(options, el){
			this.vent = options.vent;
			this.el = options.el;

			this.vent.bind("subscription:selected", this.clickSubscription, this);
			this.vent.bind("sidebarLoaded", this.sidebarLoaded, this);

			this.template = _.template(htmlExplorer);

			this.render();
		},

		events : {
			"click .subscription-explorer-node" : "openItem",
			"click .button-mark-all-read" : "markAllAsRead",
			"click .button-unsubscribe" : "unsubscribe"
		},

		unsubscribe: function () {
			var ref = this;

			var exploreElement = $(this.el).find(".feed");
			var titleElement = $(this.el).find(".title");

			$.ajax({
				type: "POST",
				url : "http://localhost:8000/api/unsubscribe",
				data : {
					csrfmiddlewaretoken: getCSRF(),
					subscription_id: ref.subscriptionId,
					user_id: window.get_userId()
				},
				beforeSend: function (){
					exploreElement.html("");
					exploreElement.html("<div class='loading'>Unsubscribing...<br/><br/><img src='/static/images/explorer_loading.gif' /></div>");
				},
				success: function (msg) {
					ref.vent.trigger("subscription:unsubscribe");
				}
			});
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
					subscription_id: ref.subscriptionId,
					user_id: window.get_userId()
				},
				beforeSend: function (){
					exploreElement.html("");
					exploreElement.html("<div class='loading'><img src='/static/images/explorer_loading.gif' /></div>");
				},
				success: function (msg) {
					exploreElement.html("");
					titleElement.html(ref.subscriptionTitle);

					var template;

					if(msg.length === 0)
					{
						template = _.template(htmlRowNone);
						var html = template();
						exploreElement.html(html);

						return;
					}
					else
					{
						template = _.template(htmlRowAll);
					}		

					for(var i = 0; i < msg.length; i ++)
					{		
						var html = template({ data : msg[i] });

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
			// TODO: Open viewer 
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

	return ExplorerView;
});