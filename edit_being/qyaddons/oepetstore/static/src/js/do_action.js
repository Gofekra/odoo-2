odoo.define("petstore", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var data = require('web.data');
    var QWeb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;


    var HomePage = Widget.extend({
        template: "HomePage",
        start: function () {
            return $.when(
                new PetToysList(this).appendTo(this.$('.oe_petstore_homepage_left'))

            );
        }
    });


    var PetToysList = Widget.extend({
        template: 'PetToysList',
        events: {
            'click .oe_petstore_pettoy': 'selected_item',
        },
        start: function () {
            var self = this;
            return new Model('product.product')
                .query(['name', 'image'])
                .filter([['categ_id.name', '=', "Pet Toys"]])
                .limit(5)
                .all()
                .then(function (results) {
                    _(results).each(function (item) {
                        self.$el.append(QWeb.render('PetToy', {item: item}));
                    });
                });
        },

        selected_item: function (event) {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'product.product',
                res_id: $(event.currentTarget).data('id'),
                views: [[false, 'form']],
            });
        },
    });


        core.action_registry.add('petstore.homepage', HomePage);
});