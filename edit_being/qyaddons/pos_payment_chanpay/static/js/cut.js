odoo.define('point_of_sale.chjie', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var Model = require('web.Model');
    var utils = require('web.utils');
    var formats = require('web.formats');
    var pos_of_sale = require('point_of_sale.screens');
    var ajax = require('web.ajax');
    var ScreenWidget = pos_of_sale.ScreenWidget;
    var PaymentScreenWidget = pos_of_sale.PaymentScreenWidget;
    var Event;

    var QWeb = core.qweb;
    var _t = core._t;

    var round_pr = utils.round_precision;

    PaymentScreenWidget.include({
        init: function(parent, options) {
        var self = this;
        this._super(parent, options);

        this.pos.bind('change:selectedOrder',function(){
                this.renderElement();
                this.watch_order_changes();
            },this);
        this.watch_order_changes();

        this.inputbuffer = "";
        this.firstinput  = true;
        this.decimal_point = _t.database.parameters.decimal_point;

        this.keyboard_keydown_handler = function(event){
            if (event.keyCode === 8 || event.keyCode === 46) { // Backspace and Delete
                event.preventDefault();

                // These do not generate keypress events in
                // Chrom{e,ium}. Even if they did, we just called
                // preventDefault which will cancel any keypress that
                // would normally follow. So we call keyboard_handler
                // explicitly with this keydown event.
                self.keyboard_handler(event);
            }
        };

        this.keyboard_handler = function(event){
            var key = '';

            if (event.type === "keypress") {
                if (event.keyCode === 13) { // Enter
                    self.$('.next').trigger("click");
                } else if ( event.keyCode === 190 || // Dot
                            event.keyCode === 110 ||  // Decimal point (numpad)
                            event.keyCode === 188 ||  // Comma
                            event.keyCode === 46 ) {  // Numpad dot
                    key = self.decimal_point;
                } else if (event.keyCode >= 48 && event.keyCode <= 57) { // Numbers
                    key = '' + (event.keyCode - 48);
                } else if (event.keyCode === 45) { // Minus
                    key = '-';
                } else if (event.keyCode === 43) { // Plus
                    key = '+';
                }
            } else { // keyup/keydown
                if (event.keyCode === 46) { // Delete
                    key = 'CLEAR';
                } else if (event.keyCode === 8) { // Backspace
                    key = 'BACKSPACE';
                }
            }

            self.payment_input(key);
            event.preventDefault();
        };

        this.pos.bind('change:selectedClient', function() {
            self.customer_changed();
        }, this);
    },
        renderElement: function() {
        var self  = this;
        this._super.apply(this,arguments);
        this.$('.next').click(function(){
            if(!$(this).hasClass("highlight")){
                return false;
            }
            self.gui.show_screen('chjie');

        });
    }
    });
    var chjie = ScreenWidget.extend({
        template:"chjie_pay",
        init: function(){
            this._super.apply(this,arguments);
        },
        show:function(){
            var self = this;
            this.res_Reg();
            self.$el.find(".report").html("条形码读取中");
            setTimeout(function(){
                self.report();
            },1000);
        },
        sse:function(){

            var self = this;

                if(Event){

                    clearInterval(Event);

                }

                Event = setInterval(function(){

                ajax.jsonRpc("/payment/chgjiepos/EventSource", 'call', {}).done(function(result){

                   if(result){

                       ajax.jsonRpc("/payment/chgjiepos/NewSource", 'call', {});

                       self.$(".end").trigger("click");

                        return false;

                   }

                });

            },100);
        },
        report:function(){
            var self = this;
            new Model('pos.order').call('action_search_num',{name:this.pos.get_order().name}).then(function(result){
                if(!result){ return false };
                var src = "/report/barcode/Code128/"+result+"?width=500&height=100";
                self.$el.find(".report").html("<a href='"+src+"' target='_blank'>"+result+"</a>");
                $.ajax({
                  type: "GET",
                  url: src,
                  success: function(result){
                      var img = new Image();
                      img.src=src;
                      self.$el.find(".report").prepend(img);

                   }

                });
                self.sse();
             });

        },
        res_Reg:function(){
            var self = this;
            this.$el.toggleClass('oe_hidden');
            this.$(".cancel").unbind().click(function(){
                self.unlink();
            });
            this.$(".end").unbind().click(function(){
                self.validate_order();
            })
        },
        unlink:function(){
            var self = this;
            if(Event){
                clearInterval(Event);
            }
            new Model('pos.order').call('action_unlink',{name:this.pos.get_order().name}).then(function(result){
                 self.gui.show_screen('payment');
             })
        },
        order_is_valid: function(force_validation) {
        var self = this;
        var order = this.pos.get_order();
        if (order.get_orderlines().length === 0) {
            this.gui.show_popup('error',{
                'title': _t('Empty Order'),
                'body':  _t('There must be at least one product in your order before it can be validated'),
            });
            return false;
        }

        var plines = order.get_paymentlines();
        for (var i = 0; i < plines.length; i++) {
            if (plines[i].get_type() === 'bank' && plines[i].get_amount() < 0) {
                this.gui.show_popup('error',{
                    'message': _t('Negative Bank Payment'),
                    'comment': _t('You cannot have a negative amount in a Bank payment. Use a cash payment method to return money to the customer.'),
                });
                return false;
            }
        }

        if (!order.is_paid() || this.invoicing) {
            return false;
        }

        // The exact amount must be paid if there is no cash payment method defined.
        if (Math.abs(order.get_total_with_tax() - order.get_total_paid()) > 0.00001) {
            var cash = false;
            for (var i = 0; i < this.pos.cashregisters.length; i++) {
                cash = cash || (this.pos.cashregisters[i].journal.type === 'cash');
            }
            if (!cash) {
                this.gui.show_popup('error',{
                    title: _t('Cannot return change without a cash payment method'),
                    body:  _t('There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'),
                });
                return false;
            }
        }

        // if the change is too large, it's probably an input error, make the user confirm.
        if (!force_validation && order.get_total_with_tax() > 0 && (order.get_total_with_tax() * 1000 < order.get_total_paid())) {
            this.gui.show_popup('confirm',{
                title: _t('Please Confirm Large Amount'),
                body:  _t('Are you sure that the customer wants to  pay') +
                       ' ' +
                       this.format_currency(order.get_total_paid()) +
                       ' ' +
                       _t('for an order of') +
                       ' ' +
                       this.format_currency(order.get_total_with_tax()) +
                       ' ' +
                       _t('? Clicking "Confirm" will validate the payment.'),
                confirm: function() {
                    self.validate_order('confirm');
                },
            });
            return false;
        }

        return true;
    },
        finalize_validation: function() {
        var self = this;
        var order = this.pos.get_order();
        var def = $.Deferred()
        if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) {
                this.pos.proxy.open_cashbox();
        }

        // order.initialize_validation_date();
        if (order.is_to_invoice()) {
            var invoiced = this.pos.push_and_invoice_order(order);
            this.invoicing = true;
            invoiced.fail(function(error){
                self.invoicing = false;
                if (error.message === 'Missing Customer') {
                    self.gui.show_popup('confirm',{
                        'title': _t('Please select the Customer'),
                        'body': _t('You need to select the customer before you can invoice an order.'),
                        confirm: function(){
                            self.gui.show_screen('clientlist');
                        },
                    });
                } else if (error.code < 0) {        // XmlHttpRequest Errors
                    self.gui.show_popup('error',{
                        'title': _t('The order could not be sent'),
                        'body': _t('Check your internet connection and try again.'),
                    });
                } else if (error.code === 200) {    // OpenERP Server Errors
                    self.gui.show_popup('error-traceback',{
                        'title': error.data.message || _t("Server Error"),
                        'body': error.data.debug || _t('The server encountered an error while receiving your order.'),
                    });
                } else {                            // ???
                    self.gui.show_popup('error',{
                        'title': _t("Unknown Error"),
                        'body':  _t("The order could not be sent to the server due to an unknown error"),
                    });
                }
            });
            invoiced.done(function(){
                self.invoicing = false;
                self.gui.show_screen('receipt');
            });
        } else {
            this.pos.push_order(order);
            this.gui.show_screen('receipt');
            def.resolve(true);
        }

        return def;
    },
        validate_order: function(force_validation) {
        if (this.order_is_valid(force_validation)) {
            var self = this;

            this.finalize_validation().then(function(){

                 new Model('pos.order').call('action_pos_order_paid_reset',{name:self.pos.get_order().name}).then(function(result){
                        if(Event){
                            clearInterval(Event);
                        }
                 })

            });

        }else{
            alert("你的钱不够");
            this.gui.show_screen('payment');

        }
    }
    });

    gui.define_screen({name:'chjie', widget: chjie});

    return chjie;
});