odoo.define('ct_dashboard.EchartView', function (require) {
"use strict";
var ajax = require('web.ajax');
var Widget = require('web.Widget');

var cotong_dashboard = Widget.extend({
    willStart: function() {
        return ajax.loadJS('/ct_dashboard/static/src/js/lib/echarts.min.js');
    },
    optionPie_cir: function (data,titleName,chart_tpye) {
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}:{c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                data:data,
                x:'left'
            },
            textStyle:{
                fontFamily:"Microsoft YaHei",
                fontSize: 12
            },
            series: [
                {
                    name: titleName,
                    type: chart_tpye,
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:data,
                    center:['60%','50%'] //图的显示位置
                }
            ],
            backgroundColor: '#fff'
        };
        return option;
    },
    optionBar_Gradient:{
        from:"#a40000",
        to:"#380000"
    },
    optionBar: function(char_obj) {
            //初始化
            var fom = this.optionBar_Gradient.from,
                to = this.optionBar_Gradient.to;
            var _extend=$.extend({},{
                text:'标题',
                backgroundColor:"#CCC",
                d:'%',
                xAxisDate:["延时","准时","合格"],
                aximat:'%',
                max:200,
                min:0,
                series:{
                    name:'销量',
                    type:'bar',
                    data: [
                    {value:20,name:"20%"},
                    {value:30,name:"30%"},
                    {value:40,name:"40%"}
                ]
                }
            },char_obj);

            _extend.max = Math.ceil(_extend.max/5)*5;

            var option = {
            title: {
                text: _extend.text,
                textStyle: {
                    fontSize: 12,
                    fontWeight: 'bolder',
                    fontFamily:"Microsoft YaHei",
                    color: '#333'       // 主标题文字颜色
                },
            },
            backgroundColor: "#fff",
            itemStyle: {
                normal:{
                    color:new echarts.graphic.LinearGradient(0,0,0,1,[{
                        offset:1,
                        color:"#ddd"
                    },{
                        offset:0,
                        color:"#a0a0a0"
                    }])
                }
            },
            textStyle:{
                fontFamily:"Microsoft YaHei",
                fontSize: 12,
                color:"#666"
            },
            grid:{'x':Math.max(30,_extend.max.toString().length*12),y:40,x2:0,y2:40},
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} "+_extend.d,
                textStyle:{
                    fontFamily:"微软雅黑",
                    fontSize: 12,
                    color:"#FFF"
                }
            },
            xAxis:[
                {
                    data:_extend.xAxisDate,
                    axisLine:{
                        lineStyle:{
                            "color": new echarts.graphic.LinearGradient(0,0,1,0,[{
                                offset:0,
                                color:fom
                            },{
                                offset:1,
                                color:to
                            }]),
                        }
                    },
                    axisTick:{
                        show:false
                    }
                }
            ],
            yAxis:[
                {
                    axisLine:{
                        lineStyle:{
                            "color": new echarts.graphic.LinearGradient(0,0,0,1,[{
                                offset:1,
                                color:fom
                            },{
                                offset:0,
                                color:to
                            }]),
                        }
                    },
                    type : 'value',
                    axisLabel : {
                        formatter: '{value} '+_extend.d,
                        textStyle:{
                           color:fom
                        }
                    },
                    splitLine:{
                        lineStyle:{
                            "type": "dashed",
                            "color":"#dcdcdc"
                        }
                    },
                    min:0,
                    max:_extend.max
                }
            ],
            series: [{
                name: _extend.series.name,
                type: _extend.series.type,
                data:_extend.series.data,
                barWidth:35,

            }]
        };

        if(_extend.line){

            option.series.unshift(_extend.line);
        }

        return option;
    },
    tips: function () {
    	console.log("模块引用成功");
    }

});
return cotong_dashboard;
});

