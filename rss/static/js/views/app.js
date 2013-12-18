var AppView = Backbone.View.extend({
  el: "#app",
 
  initialize: function() {

      this.template = Handlebars.compile($("#app-template").html());

      this.vent = _.extend({}, Backbone.Events);
      
      this.vent.bind("manageSubscription", this.manageSubscription, this);

      this.explorerView = new ExplorerView({vent: this.vent, el: "#content" });    
      this.manageView = new ManageSubscriptionsView({vent: this.vent, el: "#content" });      

      this.mainView = new Array();

      this.mainView[0] = this.explorerView;
      this.mainView[1] = this.manageView;

      this.currentViewIndex = 0;

      this.render();

      // View Setup
      this.controlsView = new ControlsView({vent: this.vent, el: "#controls" });      
      this.sidebarView = new SideBarView({vent: this.vent, el: "#sidebar" });      

  },

  manageSubscription: function () {
      this.currentViewIndex = 1;

      this.mainView[this.currentViewIndex].render();
  },

  viewSubscriptionItem: function () {
    console.log('view!')
      this.currentViewIndex = 0;
      this.mainView[this.currentViewIndex].render();
  },

  render: function() {
      $(this.el).html(this.template());

      this.mainView[this.currentViewIndex].render();
  },
});