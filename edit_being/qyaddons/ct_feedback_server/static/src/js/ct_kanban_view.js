odoo.define('ct_feedback.KanbanView', function (require) {
"use strict";

var core = require('web.core');
var data = require('web.data');
var data_manager = require('web.data_manager');
var Model = require('web.DataModel');
var Dialog = require('web.Dialog');
var form_common = require('web.form_common');
var Pager = require('web.Pager');
var pyeval = require('web.pyeval');
var QWeb = require('web.QWeb');
var session = require('web.session');
var utils = require('web.utils');
var View = require('web.View');

var odooKanbanView = require('web_kanban.KanbanView');

var ctKanbanView = odooKanbanView.include({
    add_record_to_column: function (event) {
        var self = this;
        var column = event.target;
        var record = event.data.record;
        var data = {};
        data[this.group_by_field] = event.target.id;
        this.dataset.write(record.id, data, {'context':{'from_kanban':true}}).done(function () {
            if (!self.isDestroyed()) {
                self.reload_record(record);
                self.resequence_column(column);
            }
        }).fail(this.do_reload);
    }
});

return ctKanbanView;

})