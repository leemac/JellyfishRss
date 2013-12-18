var ManageSubscriptionsView = Backbone.View.extend({

	initialize: function(options){
		this.vent = options.vent;
		this.el = options.el;

		this.template = Handlebars.compile($("#manage-subscriptions-template").html());
	},

	events : {
		"click .button-ok" : "buttonOkClick",
		"click .button-cancel" : "buttonCancelClick",
	},

	buttonEditClick: function (ev) {
		var row = $(ev.target).parents(".row");

		row.find("input").show();
		row.find("label").hide();
	},

	buttonSaveClick: function (ev) {
		var row = $(ev.target).parents(".row");

		row.find("input").hide();
		row.find("label").show();
	},

	buttonOkClick: function () 
	{
		
	},

	buttonCancelClick: function () 
	{
		
	},

	refreshItems : function ()
	{
		var element = $(this.el).find("#manage-grid");

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
				var source   = $("#subscription-manage-node-template").html();
				var template = Handlebars.compile(source);

				var html = "";
				for(var i = 0; i < msg.length; i ++)
				{		
					element.append(template(msg[i]));
				}

				$(".btn-manage-edit").click(ref.buttonEditClick);
			}
		});

	},

	render: function() {
		$(this.el).html(this.template());

		this.refreshItems();

	    return this;
	},
});