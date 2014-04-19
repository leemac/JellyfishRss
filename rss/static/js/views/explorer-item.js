define([
  'jquery', 
  'underscore',
  'backbone'
], function($, _, Backbone){

	var ExplorerItemView = Backbone.View.extend({
        tagName: "div",
		initialize: function(options, el){
			this.vent = options.vent;
			this.el = options.el;
            this.template = options.template;
            this.model = options.model;

			this.render();
		},

		events : {

		},
		render: function() {

			this.$el.append(this.template({ data : this.model }));

			return this;
		}
	});

	return ExplorerItemView;
});