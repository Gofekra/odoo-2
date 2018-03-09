/*global Highcharts*/
odoo.define("web_lead_funnel_chart.web_lead_funnel_chart", function(require) {
    "use strict";

    var core = require("web.core");
    var dataset = require("web.data");
    var Widget = require("web.Widget");
    var ajax = require('web.ajax');
    var _t = core._t;

    var web_lead_funnel_chart = Widget.extend({
        willStart: function() {
            return ajax.loadJS('/web_lead_funnel_chart/static/src/js/echarts.min.js');
        },
        template: "FunnelChart",
        start: function() {
            var self = this;
            var emp_child = [];
            self.crm_lead_dataset = new dataset.DataSetSearch(self, "crm.lead", {}, []);
            self.crm_lead_dataset.call("get_lead_stage_data", [
                []
            ]).done(function(callbacks) {

              var currentValue=callbacks.slice().map(function(i){
                  return i.name;
              });

              var min = 0;
              var defaultValue = callbacks.slice().map(function(i){
                  var m = $.extend({},i);
                    m.value = min+=20;
                    return m;
              });
                var myChart = echarts.init($("#container").css({width:"100%",height:$(".o_content").height()+"px",margin:"0 auto"}).get(0));
                myChart.setOption( {
                color : [
                             'rgba(255, 69, 0, 0.5)',
                    'rgba(255, 150, 0, 0.5)',
                    'rgba(255, 200, 0, 0.5)',
                    'rgba(155, 200, 50, 0.5)',
                ],
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c}"
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                legend: {
                    top: '5%',
                    data :currentValue
                },
                calculable : true,
                series : [
                    {
                        name:'预期',
                        type:'funnel',
                        x: '10%',
                        width: '80%',
                        itemStyle: {
                            normal: {
                                label: {
                                    formatter: '{b}预期'
                                },
                                labelLine: {
                                    show : false
                                }
                            },
                            emphasis: {
                                label: {
                                    position:'inside',
                                    formatter: '{b}预期 : {c}'
                                }
                            }
                        },
                        data:defaultValue
                    },
                    {
                        name:'实际',
                        type:'funnel',
                        x: '10%',
                        width: '80%',
                        maxSize: '80%',
                        itemStyle: {
                            normal: {
                                borderColor: '#fff',
                                borderWidth: 2,
                                label: {
                                    position: 'inside',
                                    formatter: '{c}',
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            emphasis: {
                                label: {
                                    position:'inside',
                                    formatter: '{b}实际 : {c}'
                                }
                            }
                        },
                        data:callbacks
                    }
                ]
            });

                            });

                    },
                });

    core.action_registry.add("web_lead_funnel_chart.funnel", web_lead_funnel_chart);

});
