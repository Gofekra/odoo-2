odoo.define('import_data_by_fields.import', function (require) {
    'use strict';

    var DataImport = require('base_import.import').DataImport;

    DataImport.include({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // #员工出勤根据主键更新记录
                self.$el.on('click', 'input.oe_import_by_number', function () {
                    self.oe_import_by_number = !self.oe_import_by_number;
                })
            })
        },
        import_options: function () {
            var option = this._super();
            option.oe_import_by_number = this.oe_import_by_number;
            return option;
        },
    });

});