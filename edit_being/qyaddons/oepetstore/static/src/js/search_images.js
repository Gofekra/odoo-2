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
                new PetToysList(this).appendTo(this.$('.oe_petstore_homepage_left')),
                new MessageOfTheDay(this).appendTo(this.$('.oe_petstore_homepage_right'))
            );
        }
    });
    core.action_registry.add('petstore.homepage', HomePage);

    var MessageOfTheDay = Widget.extend({
        template: 'MessageOfTheDay',
        start: function () {
            var self = this;
            return new Model('oepetstore.message_of_the_day')
                .query(["message"])
                .order_by('-create_date', '-id')
                .all()
                .then(function (result) {
                    console.log(result)
                    self.$(".oe_mywidget_message_of_the_day").text(result.message);
                    //    self.$el.append(QWeb.render('MessageOfTheDay', {item: result}));
                });

        }
    });

    var PetToysList = Widget.extend({
        template: 'PetToysList',
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
        }
    });
});