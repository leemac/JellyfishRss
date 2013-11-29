var AppView = Backbone.View.extend({
  el: "#app",
  events: {
    'click ul#perpage span' : 'perpage'
  },

  subscriptionClick : function (ev) {
    var link = $(ev.target);

    var subscriptionid = $(this).attr("js-subscription-id");
    SelectSubscription($(this));

    LoadSubscription(subscriptionid);

  },

  initialize: function() {
      this.render();
  },

  render: function() {

      var vent = _.extend({}, Backbone.Events);

      this.sidebarView = new SideBarView({vent: vent, el: this.el });      
      $(this.el).append(this.sidebarView.el);

      this.explorerView = new ExplorerView({vent: vent, el: this.el, test : "hi" });      
      $(this.el).append(this.explorerView.el);      
  },
});