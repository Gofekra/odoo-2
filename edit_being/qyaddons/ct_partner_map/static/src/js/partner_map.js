odoo.define('ct_partner_map', function (require) {

var ajax = require('web.ajax');
var core = require('web.core');
var form_common = require('web.form_common');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var Model = require('web.Model');
var session = require('web.session');
var Dialog = require('web.Dialog');
var QWeb = core.qweb;

    var FieldBaiduMap = form_common.AbstractField.extend({
        template: 'BaiduMap',
        start:function(){

            this._super.apply(this,arguments);

            this.load_map();

        },
        load_map:function(){

            var self = this;

             this.alive(new Model("res.partner").call("search_key").then(function(result){

                 if(!result){

                        alert("请配置你的密钥");

                        return;
                 }

                ajax.loadJS('http://api.map.baidu.com/getscript?v=2.0&ak='+(result)).then(function(){

                    self.render_map();

                })

            }));
        },
        render_map: function() {
            var self = this;
            var flag = true;
            var address="";

            var hash = function(search){

                var dict = ( window.location.hash).split("#")[1].split("&");

                var The = dict.filter(function(i){

                    return i.indexOf(search+"=")==0;

                });

                return The.length?The[0].split("=")[1]:"";
            };

            var loadData = function(){

                return new Promise(function(resolve){

                     new Model("res.partner").call("search_addres",[],{id:hash("id")}).then(function(result){

                        address = result;

                        resolve(result);
                    });

                })

               
            }


            function mapDispaly () {
                flag = false;   
                console.log(address);
                
                var map = new BMap.Map("baidumap");
                var localSearch = new BMap.LocalSearch(map);
                localSearch.setSearchCompleteCallback(function(searchResult) {
                    if (searchResult.getPoi(0) === undefined) {
                        $('#baidumap').html('请按格式正确填写地址！');
                        alert("请正确填写地址！\n不然地图无法显示！");
                    } else {
                        map.enableScrollWheelZoom(); //启用滚轮放大缩小，默认禁用
                        map.enableContinuousZoom(); //启用地图惯性拖拽，默认禁用
                        map.addControl(new BMap.NavigationControl()); //添加默认缩放平移控件
                        map.addControl(new BMap.OverviewMapControl()); //添加默认缩略地图控件
                        var poi = searchResult.getPoi(0);
                        var marker = new BMap.Marker(new BMap.Point(poi.point.lng, poi.point.lat)); // 创建标注，为要查询的地方对应的经纬度
                        map.addOverlay(marker);
                        var phone = address.mobile;
                        var phone_str = "<a href='tel:" + phone + "'>" + phone + "</a>";
                        var content = '<div>' + address.name + '<br/>' + '地址：' + address.cite + '<br/>' + '电话：' + phone_str + '</div>';
                        var infoWindow = new BMap.InfoWindow(content);
                        marker.openInfoWindow(infoWindow);
                        marker.addEventListener("click", function() {
                            this.openInfoWindow(infoWindow);
                        });
                    }
                });
                map.centerAndZoom(address.cite,15);
                localSearch.search(address.cite);
            };

            function foo(){

                var str = $(this).find("a").text().trim();

                if(str === '百度地图'){

                    window.requestAnimationFrame(function(){

                        loadData().then(function(result){

                            mapDispaly();
                        })

                    });

                }

            }

            function back(){

                 setTimeout(function () {

                    loadData().then(function(result){

                        mapDispaly();
                    })

                 },1000);

            }

            $(".o_content").undelegate('.o_notebook>.nav-tabs li','click').delegate('.o_notebook>.nav-tabs li', 'click',foo);
            $(".o_control_panel").undelegate('.o_cp_right .o_cp_pager .btn-group button','click').delegate('.o_cp_right .o_cp_pager .btn-group button','click',back);

        }
    });

    core.form_widget_registry.add('baidumap', FieldBaiduMap);

    var supplierMap = Widget.extend({
        template: "supplier_map",
        start: function() {
            this.load_map()
        },
        load_map:function(){

            var self = this;

             this.alive(new Model("res.partner").call("search_key").then(function(result){

                 if(!result){

                        alert("请配置你的密钥");

                        return;

                 }

                ajax.loadJS('http://api.map.baidu.com/getscript?v=2.0&ak='+result).then(function(){

                    self.render_map();

                })

            }));
        },
        render_map:function(){
            this.$el.height($(".o_content").height());
            var self = this;
            new Model('res.partner')
                .query(['name', 'state_id', 'city', 'street2', 'street', 'phone', 'mobile'])
                .filter([
                    ['supplier', '=', true],
                    ['active', '=', 1],
                    ['is_company', '=', 1]
                ])
                .limit(20)
                .all()
                .then(function(results) {
                    if (results.length > 0) {
                        var marker_arr = [];
                        for (var i = results.length - 1; i >= 0; i--) {
                            var address = '';
                            if (results[i].state_id[1]) {
                                address += results[i].state_id[1];
                            }
                            if (results[i].city) {
                                address += results[i].city;
                            }
                            if (results[i].street2) {
                                address += results[i].street2;
                            }
                            if (results[i].street) {
                                address += results[i].street;
                            }
                            var tel = results[i].phone || results[i].mobile || '空';
                            var name = results[i].name;
                            marker_arr.push({
                                address: address,
                                tel: tel,
                                name: name
                            });
                        }
                        if (marker_arr.length > 0) {

                            ajax.jsonRpc('/suppliersmap', 'call', {
                                    'marker_arr': marker_arr
                                })
                                .then(function(points) {
                                    if (points.length > 0) {
                                        var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
                                        map.enableScrollWheelZoom(true); //启用滚轮放大缩小
                                        //向地图中添加缩放控件
                                        var ctrlNav = new window.BMap.NavigationControl({
                                            anchor: BMAP_ANCHOR_TOP_LEFT,
                                            type: BMAP_NAVIGATION_CONTROL_LARGE
                                        });
                                        map.addControl(ctrlNav);

                                        //向地图中添加缩略图控件
                                        var ctrlOve = new window.BMap.OverviewMapControl({
                                            anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
                                            isOpen: 1
                                        });
                                        map.addControl(ctrlOve);

                                        //向地图中添加比例尺控件
                                        var ctrlSca = new window.BMap.ScaleControl({
                                            anchor: BMAP_ANCHOR_BOTTOM_LEFT
                                        });
                                        map.addControl(ctrlSca);
                                        var localSearch = new BMap.LocalSearch(map);
                                        localSearch.enableAutoViewport(); //允许自动调节窗体大小
                                        var point_all = [];
                                        for (var i = points.length - 1; i >= 0; i--) {
                                            point_all.push(new BMap.Point(points[i].point.lng, points[i].point.lat));
                                        }
                                        for (var i = points.length - 1; i >= 0; i--) {
                                            var marker = new BMap.Marker(new BMap.Point(points[i].point.lng, points[i].point.lat));
                                            map.addOverlay(marker);
                                            marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
                                            // 给标注点添加点击事件，并立即执行函数和闭包
                                            (function() {
                                                var phone_str = "<a href='tel:" + points[i].tel + "'>" + points[i].tel + "</a>";
                                                var content = '<div>' + points[i].name + '<br/>' + '地址：' + points[i].address + '<br/>' + '电话：' + phone_str + '</div>';
                                                var infoWindow = new BMap.InfoWindow(content);
                                                marker.addEventListener("click", function() {
                                                    this.openInfoWindow(infoWindow);
                                                });
                                            })();
                                        }
                                        // 根据标注点数组自动缩放级别
                                        if (point_all.length == 1) {
                                            map.centerAndZoom(new BMap.Point(points[0].point.lng, points[0].point.lat), 15);
                                        } else {
                                            var view = map.getViewport(point_all);
                                            var mapZoom = view.zoom;
                                            var centerPoint = view.center;
                                            map.centerAndZoom(centerPoint, mapZoom - 1);
                                        }

                                    } else {
                                        var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
                                        //没有坐标，显示全中国
                                        map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
                                    }
                                });
                        } else {
                            var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
                            //没有坐标，显示全中国
                            map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
                        }
                    } else {
                        // 创建Map实例
                        var map = new BMap.Map("oe_supplier_map");
                        //没有坐标，显示全中国
                        map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
                    }

                });
        }
        })

    core.action_registry.add('supplierMap', supplierMap);

})


// openerp.ct_partner_map = function(instance) {

//     instance.ct_partner_map.FieldBaiduMap = instance.web.form.AbstractField.extend({
//         template: 'BaiduMap',
//         render_value: function() {
//             var self = this;
//             var address = self.get('value');
//             if (!address) {
//                 address = "上海市浦东新区浦东南路滨江2250号,上海企通软件有限公司,400-820-8720";
//             }
//             function mapDispaly () {
//                 var map = new BMap.Map("baidumap");
//                 var localSearch = new BMap.LocalSearch(map);
//                 localSearch.setSearchCompleteCallback(function(searchResult) {
//                     if (searchResult.getPoi(0) === undefined) {
//                         $('#baidumap').html('请按格式正确填写地址！');
//                         alert("请正确填写地址！\n不然地图无法显示！");
//                     } else {
//                         map.enableScrollWheelZoom(); //启用滚轮放大缩小，默认禁用
//                         map.enableContinuousZoom(); //启用地图惯性拖拽，默认禁用
//                         map.addControl(new BMap.NavigationControl()); //添加默认缩放平移控件
//                         map.addControl(new BMap.OverviewMapControl()); //添加默认缩略地图控件
//                         var poi = searchResult.getPoi(0);
//                         var marker = new BMap.Marker(new BMap.Point(poi.point.lng, poi.point.lat)); // 创建标注，为要查询的地方对应的经纬度
//                         map.addOverlay(marker);
//                         var phone = address.split(",")[2];
//                         var phone_str = "<a href='tel:" + phone + "'>" + phone + "</a>";
//                         var content = '<div>' + address.split(",")[1] + '<br/>' + '地址：' + address.split(",")[0] + '<br/>' + '电话：' + phone_str + '</div>';
//                         var infoWindow = new BMap.InfoWindow(content);
//                         marker.openInfoWindow(infoWindow);
//                         marker.addEventListener("click", function() {
//                             this.openInfoWindow(infoWindow);
//                         });
//                     }
//                 });
//                 map.centerAndZoom(address.split(",")[0], 15);
//                 localSearch.search(address.split(",")[0]);
//             };
//             $('.ui-tabs-anchor').click(function (argument){
//                 var str = $(this)[0].childNodes[0].data.replace(/\s/g, "")
//                 if(str === '百度地图'){
//                     mapDispaly();
//                 }
//             });
//             mapDispaly();
//         },


//     });

//     instance.web.form.widgets.add('baidumap', 'instance.ct_partner_map.FieldBaiduMap');

//     instance.supplierMap = instance.Widget.extend({
//         template: "supplier_map",
//         start: function() {
//             var self = this;
//             new instance.web.Model('res.partner')
//                 .query(['name', 'state_id', 'city', 'street2', 'street', 'phone', 'mobile'])
//                 .filter([
//                     ['supplier', '=', true],
//                     ['active', '=', 1],
//                     ['is_company', '=', 1]
//                 ])
//                 .limit(20)
//                 .all()
//                 .then(function(results) {
//                     if (results.length > 0) {
//                         var marker_arr = [];
//                         for (var i = results.length - 1; i >= 0; i--) {
//                             var address = '';
//                             if (results[i].state_id[1]) {
//                                 address += results[i].state_id[1];
//                             }
//                             if (results[i].city) {
//                                 address += results[i].city;
//                             }
//                             if (results[i].street2) {
//                                 address += results[i].street2;
//                             }
//                             if (results[i].street) {
//                                 address += results[i].street;
//                             }
//                             var tel = results[i].phone || results[i].mobile || '空';
//                             var name = results[i].name;
//                             marker_arr.push({
//                                 address: address,
//                                 tel: tel,
//                                 name: name
//                             });
//                         }
//                         if (marker_arr.length > 0) {

//                             openerp.jsonRpc('/suppliersmap', 'call', {
//                                     'marker_arr': marker_arr
//                                 })
//                                 .then(function(points) {
//                                     if (points.length > 0) {
//                                         var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
//                                         map.enableScrollWheelZoom(true); //启用滚轮放大缩小
//                                         //向地图中添加缩放控件
//                                         var ctrlNav = new window.BMap.NavigationControl({
//                                             anchor: BMAP_ANCHOR_TOP_LEFT,
//                                             type: BMAP_NAVIGATION_CONTROL_LARGE
//                                         });
//                                         map.addControl(ctrlNav);

//                                         //向地图中添加缩略图控件
//                                         var ctrlOve = new window.BMap.OverviewMapControl({
//                                             anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
//                                             isOpen: 1
//                                         });
//                                         map.addControl(ctrlOve);

//                                         //向地图中添加比例尺控件
//                                         var ctrlSca = new window.BMap.ScaleControl({
//                                             anchor: BMAP_ANCHOR_BOTTOM_LEFT
//                                         });
//                                         map.addControl(ctrlSca);
//                                         var localSearch = new BMap.LocalSearch(map);
//                                         localSearch.enableAutoViewport(); //允许自动调节窗体大小
//                                         var point_all = [];
//                                         for (var i = points.length - 1; i >= 0; i--) {
//                                             point_all.push(new BMap.Point(points[i].point.lng, points[i].point.lat));
//                                         }
//                                         for (var i = points.length - 1; i >= 0; i--) {
//                                             var marker = new BMap.Marker(new BMap.Point(points[i].point.lng, points[i].point.lat));
//                                             map.addOverlay(marker);
//                                             marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
//                                             // 给标注点添加点击事件，并立即执行函数和闭包
//                                             (function() {
//                                                 var phone_str = "<a href='tel:" + points[i].tel + "'>" + points[i].tel + "</a>";
//                                                 var content = '<div>' + points[i].name + '<br/>' + '地址：' + points[i].address + '<br/>' + '电话：' + phone_str + '</div>';
//                                                 var infoWindow = new BMap.InfoWindow(content);
//                                                 marker.addEventListener("click", function() {
//                                                     this.openInfoWindow(infoWindow);
//                                                 });
//                                             })();
//                                         }
//                                         // 根据标注点数组自动缩放级别
//                                         if (point_all.length == 1) {
//                                             map.centerAndZoom(new BMap.Point(points[0].point.lng, points[0].point.lat), 15);
//                                         } else {
//                                             var view = map.getViewport(point_all);
//                                             var mapZoom = view.zoom;
//                                             var centerPoint = view.center;
//                                             map.centerAndZoom(centerPoint, mapZoom - 1);
//                                         }

//                                     } else {
//                                         var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
//                                         //没有坐标，显示全中国
//                                         map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
//                                     }
//                                 });
//                         } else {
//                             var map = new BMap.Map("oe_supplier_map"); // 创建Map实例
//                             //没有坐标，显示全中国
//                             map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
//                         }
//                     } else {
//                         // 创建Map实例
//                         var map = new BMap.Map("oe_supplier_map");
//                         //没有坐标，显示全中国
//                         map.centerAndZoom(new BMap.Point(103.388611, 35.563611), 5);
//                     }

//                 });
//         },

//     });


//     instance.web.client_actions.add('supplierMap', 'instance.supplierMap');
// }
