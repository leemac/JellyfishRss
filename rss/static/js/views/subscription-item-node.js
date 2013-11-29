var SubscriptionItemView = Backbone.View.extend({
	tagName:  "div",

	initialize: function(){
		this.template = Handlebars.compile($("#item-template").html());
		this.render();
	},

	render: function() {
	  this.$el.html(this.template(this.model));
	  return this;
	},
});