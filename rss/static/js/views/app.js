var AppView = Backbone.View.extend({
  el: "#app",
 
  initialize: function() {
      this.render();
  },

  render: function() {

      var vent = _.extend({}, Backbone.Events);

      this.controlsView = new ControlsView({vent: vent, el: this.el });      
      $(this.el).append(this.controlsView.el);      

      this.sidebarView = new SideBarView({vent: vent, el: this.el });      
      $(this.el).append(this.sidebarView.el);


      this.explorerView = new ExplorerView({vent: vent, el: this.el });      
      $(this.el).append(this.explorerView.el);      
  },
});