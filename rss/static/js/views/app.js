var AppView = Backbone.View.extend({
    el: "#app",

    initialize: function() {

        this.template = Handlebars.compile($("#app-template").html());

        this.vent = _.extend({}, Backbone.Events);

        this.render();

        // View Setup
        this.sidebarView = new SideBarView({vent: this.vent, el: "#sidebar" });
        this.explorerView = new ExplorerView({vent: this.vent, el: "#content" });

    },

    render: function() {
        $(this.el).html(this.template());
    }
});