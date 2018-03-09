odoo.define('ct_base_import_export', function (require) {
    var core = require('web.core');
    var Model = require('web.Model');
    var ListView = require('web.ListView');
    var Sidebar = require('web.Sidebar');
    var _t = core._t;

    ListView.include({
        load_list: function() {
            var model = new Model('res.users'),
                elem = this.__parentedParent.$el,
                result = this._super.apply(this, arguments);
            model.call('has_group', ['ct_base_import_export.group_import']).then(function(can_import) {
                if (!can_import) {
                    $(".o_control_panel .o_cp_left .o_cp_buttons .o_list_buttons .o_button_import").hide()
                }else{
                    $(".o_control_panel .o_cp_left .o_cp_buttons .o_list_buttons .o_button_import").show()
                }

            });
            return result;
        }
    });

    Sidebar.include({

        add_items: function(section_code, items) {
            var self = this,
                _sup = _.bind(this._super, this),
                model = new Model('res.users'),
                args = ['ct_base_import_export.group_export'];
            model.call('has_group', args).then(function(can_export) {
                if (can_export) {
                    _sup.call(self, section_code, items);
                } else {
                    var export_label = _t("Export"),
                        new_items = items;
                    if (section_code == 'other') {
                        new_items = [];
                        for (var i = 0; i < items.length; i++) {
                            if (items[i]['label'] != export_label) {
                                new_items.push(items[i]);
                            };
                        };
                    };
                    _sup.call(self, section_code, new_items);
                }
            });
        }

    })

});



// openerp.ct_base_import_export = function(instance) {
//
//     var _t = instance.web._t;
//
//     instance.web.ListView.include({
//
//         load_list: function() {
//             var model = this.session.model('res.users'),
//                 args = ['ct_base_import_export.group_import'],
//                 elem = this.__parentedParent.$el,
//                 result = this._super.apply(this, arguments);
//             model.call('has_group', args).then(function(can_import) {
//                 if (!can_import) {
//                     elem.find('.oe_list_button_import').hide();
//                     elem.find('.oe_fade').hide();
//                 }
//             });
//             return result;
//         },
//         start_edition: function(record, options) {
//             this._super.apply(this, arguments);
//             $('.oe_fade').show();
//         },
//         save_edition: function() {
//             $('.oe_fade').hide();
//             return this._super.apply(this, arguments);
//         },
//         cancel_edition: function(force) {
//             $('.oe_fade').hide();
//             return this._super.apply(this, arguments);
//         }
//     });
//
//     instance.web.Sidebar.include({
//
//         add_items: function(section_code, items) {
//             var self = this,
//                 _sup = _.bind(this._super, this),
//                 model = this.session.model('res.users'),
//                 args = ['ct_base_import_export.group_export'];
//             model.call('has_group', args).then(function(can_export) {
//                 if (can_export) {
//                     _sup.call(self, section_code, items);
//                 } else {
//                     var export_label = _t("Export"),
//                         new_items = items;
//                     if (section_code == 'other') {
//                         new_items = [];
//                         for (var i = 0; i < items.length; i++) {
//                             if (items[i]['label'] != export_label) {
//                                 new_items.push(items[i]);
//                             };
//                         };
//                     };
//                     _sup.call(self, section_code, new_items);
//                 }
//             });
//         }
//
//     });
//
// };
