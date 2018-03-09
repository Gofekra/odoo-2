odoo.define("oepetstore",function(require){
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
     var data = require('web.data');
    var QWeb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;

    // var HomePage = Widget.extend({
    //     start: function() {
    //       var self = this;
    //         var model = new Model("oepetstore.message_of_the_day");
    //
    //         /***  调用后端的方法 start   ***/
    //         //{context: new data.CompoundContext()} 可以不用写
    //         //     model.call("my_method",['yes'], {context: new data.CompoundContext()}).then(function(result) {
    //         //      console.log(result)
    //         //     // self.$el.append("<div>Hello " + result["hello"] + "</div>");
    //         //        self.$el.append(result["hello"]);
    //         // });
    //         /***  调用后端的方法 end   ***/
    //
    //         },
    //     });






        var HomePage = Widget.extend({
            template: "HomePage",
            start: function() {
                var self = this;
                return new Model("oepetstore.message_of_the_day")
                    .query(["message"])
                    .order_by('-create_date', '-id')
                    .all()
                    .then(function(result) {
                        (new MessagePage(this,result)).appendTo(self.$el);
                    });
            }

        });

        var MessagePage = Widget.extend({
            template: "MessagePage",
            init:function(parent,result){
                console.log(result)

                this._super.apply(this,arguments);
                this.message = result;
            },
            start: function() {

            },
        });







        core.action_registry.add('petstore.homepage', HomePage);
    });