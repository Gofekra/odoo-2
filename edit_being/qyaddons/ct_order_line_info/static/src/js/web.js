odoo.define('web.ProductPopOver', function (require) {
'use strict';

var core = require('web.core');
var formats = require('web.formats');
var ListView = require('web.ListView'); 
var Model = require('web.Model');

var QWeb = core.qweb;

var switch_money = function(num,fixed){

    if(typeof num === 'number'){

        var num = num.toFixed(fixed).toString().split('.');

        num[0] = num[0].split('').reverse().join('').replace(/\d{3}/g,function($1){

            return $1+',';

        }).replace(/\,$/,'').split('').reverse().join('');

        return num.join('.');
    }

    return num;

}


ListView.List.include({

    render:function(){

        this._super.apply(this,arguments);

        if(this.view.model=='sale.order.line' || this.view.model=='purchase.order.line'){

            setTimeout(function(){

                this.sale();

            }.bind(this),1000);
        }
    },
    sale:function(){

       var self = this,

           viewId = this.dataset.parent_view.datarecord.id,

           Users = new Model(this.view.model);

       _.each(this.$current.find('tr'),function(k){
           if($(k).data('id')){
                Users.call('search_stock',[],{id:$(k).data('id')}).then(function(result){
                    var result_array = {};
                    if(_.isArray(result)){
                        _.each(result,function(v){
                            result_array[v.name] = v.val;
                        });
                        result = result_array;
                    }

                    $(k).popover({
                        'content': QWeb.render("ProductPopOver",{
                            info:result
                        }),
                        'html': true,
                        'placement': 'auto',
                        'title': self.dataset.parent_view.datarecord.name,
                        'trigger': 'hover',
                        'delay': { 'show': 0, 'hide': 100 },
                    });
                })
           }


            // Users.query(['product_id','name','product_uom_qty','product_qty','price_subtotal','price_unit','customer_lead','date_planned']).filter([['id', '=', $(k).data('id')],['order_id','=',viewId]]).limit(1).first().then(function(result){
            
            //     if(result.date_planned){
                    
            //         result.date_planned  = result.date_planned.split(/\s+/)[0].replace(/(\d{4})-(\d{2})-(\d{2})/,'$1年$2月$3日');                    
            //     }

            //     $(k).popover({
            //         'content': QWeb.render("ProductPopOver",{
            //             info:{
            //                 '产品':result.product_id[1],
            //                 '说明':result.name,
            //                 '数量':switch_money(result.product_uom_qty || result.product_qty,3),
            //                 '单价':'$'+switch_money(result.price_unit,2),
            //                 '小计':'$'+switch_money(result.price_subtotal,2),
            //                 '交货时间':result.date_planned || switch_money(result.customer_lead,2)+'天',
            //             }
            //         }),
            //         'html': true,
            //         'placement': 'auto',
            //         'title': self.dataset.parent_view.datarecord.name,
            //         'trigger': 'hover',
            //         'delay': { 'show': 0, 'hide': 100 },
            //     });

            // })

       });

    }
})

});
