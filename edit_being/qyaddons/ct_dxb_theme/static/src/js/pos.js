odoo.define('cotong.pos.home', function (orequire) {
"use strict";

var ajax = orequire('web.ajax');
var core = orequire('web.core');
var SystrayMenu = orequire('web.SystrayMenu');
var Widget = orequire('web.Widget');
var Model = orequire('web.Model');
var session = orequire('web.session');
var Dialog = orequire('web.Dialog');
var datepicker = orequire('web.datepicker');
var home = orequire('ct_dashboard.home');
var echart_ct = orequire("ct_dashboard.EchartView");
var QWeb = core.qweb;
var echarts;

var ct_pos_home = Widget.extend(home.prototype,{
    active:1,
    events: {
        "click .pos_header .ibox": 'Action_sale',
        "click .content #Income .ibox-title":'Income_charts',
        "click .content #SalesCharts .ibox-title":'SalesCharts_charts'
  	},
  	get_date:function(AddDayCount){
		var dd = new Date();
	    dd.setDate(dd.getDate()+AddDayCount);
	    var y = dd.getFullYear();
	    var m = dd.getMonth()+1;
	    var d = dd.getDate();
	    return y+"年"+m+"月"+d+"日";
	},
    willStart: function() {

    	var dtd = $.Deferred();

    	ajax.loadJS('/ct_dxb_theme/static/src/js/lib/DatePicker/bootstrap-datepicker.min.js').then(function(){

    		return $.when(ajax.loadJS('/ct_dxb_theme/static/src/js/lib/DatePicker/bootstrap-datepicker.zh-CN.min.js'),ajax.loadJS('http://echarts.baidu.com/build/dist/echarts.js').then(function(){

	    		require.config({
				    paths: {
				        echarts: 'http://echarts.baidu.com/build/dist'
				    }
				});

				require(['echarts','echarts/chart/pie','echarts/chart/funnel','echarts/chart/bar'],function(ec){

					echarts = ec;

					dtd.resolve();

				})

	    	}))

    	})

    	return dtd;
    },
    selected_item: function (model,modelName,domai,option) {
        this.do_action(_.extend({
        	name:modelName,
            type: 'ir.actions.act_window',
            res_model: model,
            domain:domai,
            views: [[false, 'list']],
        },option || {}));
    },
    Action_sale:function(event){
    	this.do_action({
        	name: $(event.currentTarget).find(".title").text().trim(),
            type: 'ir.actions.act_window',
            res_model: 'pos.order',
            domain:this.result.domain[$(event.currentTarget).data('id')],
            views: [[false, 'list']],
            context: {},
        });
    },
    Income_charts:function(event){

    	var that = this;

    	new Model("pos.order").call("search_milimit",[],that.action_date({name:0})).then(function(result){

			that.selected_item('pos.receivables.report',$(event.currentTarget).text().trim(),result);

		})
    },
    SalesCharts_charts:function(event){

    	var that = this;

    	new Model("pos.order").call("search_top",[],that.action_date()).then(function(result){

			that.selected_item('pos.produce.rank',$(event.currentTarget).text().trim(),result,{limit:5,context:{'group_by':'product_id'}});

		})
    },
    start:function(){

        this._super();

        window.requestAnimationFrame(function(){

    		this.date_search();

    	}.bind(this))

        this.render();

    },
    date_search:function(){

    	var dateRange,start_date,end_date,submit_date,that = this;

    	$("#oe_main_menu_navbar .collapse .navbar-left.show").ready(function(){

    		if(!$("#oe_main_menu_navbar .collapse #dateRange").length){

    		var start = that.get_date(that.date_start),

			end = that.get_date(that.date_end),

			patt = /(\d{4})年(\d+)月(\d+)日/g;

    		$("#oe_main_menu_navbar .collapse .navbar-left").after(QWeb.render("dateRange"));

    		dateRange = $("#oe_main_menu_navbar .collapse #dateRange");

    		submit_date = dateRange.find("button");

    		start_date = dateRange.find(".o_datepicker_input[name='start_date']").val(start);

    		end_date = dateRange.find(".o_datepicker_input[name='end_date']").val(end);

			that.start_date = start.replace(patt,'$1-$2-$3')+" 00:00:00"

			that.end_date = end.replace(patt,'$1-$2-$3')+" 23:59:59"

    		submit_date.click(that.render.bind(that));

    		start_date.datepicker({
				language: 'zh-CN',	
			}).on('changeDate',function(ev){

				that.start_date = $(this).val().replace(patt,'$1-$2-$3')+" 00:00:00"

				start = new Date(ev.date.valueOf());

				end = new Date(that.end_date);

				if(start>end){

					end_date.val($(this).val()).datepicker('update');

					that.end_date = $(this).val().replace(patt,'$1-$2-$3')+" 23:59:59"

				}

			});

			end_date.datepicker({
				language: 'zh-CN',
				maxDate: 0
			}).on('changeDate',function(ev){

				that.end_date = $(this).val().replace(patt,'$1-$2-$3')+" 23:59:59"

				end = new Date(ev.date.valueOf())

				start = new Date(that.start_date)

				if(start>end){

					start_date.val($(this).val()).datepicker('update');

					that.start_date = $(this).val().replace(patt,'$1-$2-$3')+" 00:00:00"
				}

			})
		}

    	})
    },
    action_date:function(object){

		return _.extend({start_time:this.start_date || this.active,end_time:this.end_date || this.active},object||{})
    },
    render:function(){

    	var that = this;

    	new Model("pos.order").call("search_pos_result",[],this.action_date()).then(function(result){

    		that.$el.html(QWeb.render("PosHom",{data:result}))

    		that.result = result;

    		that.ready();

    	})
    },
    ready:function(){

    	window.requestAnimationFrame(function(){

    		this.loadChart();

    	}.bind(this))

    },
    optionBar:function(el){

    	var myChart = echarts.init(el);

        var that = this;

        var Serialize = that.EChartilze(that.result.qty_limit);

	    var option = {

	    legend: {
	        data:['数量','金额'],
	        'selected':{
	            '数量':true,
	            '金额':false,
	        }
	    },
	    grid:{'x':50,y:40,x2:20,y2:30},
	    calculable : true,
	    xAxis : [
	        {
	            type : 'category',
	            data : Serialize.name,
	            axisLine: {
	                lineStyle: {
	                    color: '#ccc'
	                },
            	},
            	axisTick:{
            		show:false
            	}
	        }
	    ],
	    yAxis : [
	        {
	            type : 'value',
	            axisLine: {
	                lineStyle: {
	                    color: '#ccc'
	                }
            	}
	        }
	    ],
	    series : [
	        {
	        	itemStyle: {
	                normal: {
	                    label: {
	                        show: true,
	                        position: 'top',
	                        formatter: '{c}'
	                    },
	                    color:'#9BCA63'
	                }
	            },
	            name:'数量',
	            type:'bar',
	            barWidth:35,
	            data:that.result.qty_limit,
	        },
	        {
	        	itemStyle: {
	                normal: {
	                    label: {
	                        show: true,
	                        position: 'top',
	                        formatter: '￥{c}'
	                    },
	                    color:'#C1232B'
	                }
	            },
	            name:'金额',
	            type:'bar',
	            data:that.result.amount_limit,
	            barWidth:35,
	        }
	    ]
	};
    	myChart.setOption(option);

    	myChart.hideLoading();

    	this.ChartAction(myChart,option,el);

    },
    optionPie:function(el){

    	var myChart = echarts.init(el);

        var that = this;

        var Serialize = that.EChartilze(that.result.pay);

	    var option = {
		    tooltip : {
		        trigger: 'item',
		        formatter: "{a} <br/>{b} :￥ {c} ({d}%)"
		    },
		    color:['#56ABE2', '#F08080','#83D93D'],
		    legend: {
		        orient : 'vertical',
		        x : 'right',
		        data:Serialize.name
		    },
		    calculable : true,
		    series : [
		        {
		        	itemStyle : {
                normal : {
                    label : {
                        formatter : "{b} :￥ {c}"
                    },
                    labelLine : {
                        show : true
                    }
                },
            },
		            name:'收入统计',
		            type:'pie',
		            radius : '70%',
		            center: ['45%', '50%'],
		            data:Serialize.obj
		        }
		    ]
		};
                    
    	myChart.setOption(option);

    	myChart.hideLoading();

    	this.ChartAction(myChart);

    },
    ChartAction:function(myChart,option,el){

	    //穿透

	    var that = this;

		function eConsole(param) {

			if(param.type=="legendSelected" && option && el){

				$.each(option.legend.selected,function(i){

					option.legend.selected[i]=i==param.target?true:false;
				})

				switch(param.target){

					case "数量":
						option.xAxis[0].data = that.EChartilze(that.result.qty_limit).name;
					break;
					case "金额":
						option.xAxis[0]["data"] = that.EChartilze(that.result.amount_limit).name;
					break;
				}


				myChart.clear();

				myChart.setOption(option,true);
			}

			if(param.type=="click"){

				switch(param.seriesName){

					case "收入统计":

						new Model("pos.order").call("search_milimit",[],that.action_date({name:param.name})).then(function(result){

							console.log(result)
							
							that.selected_item('pos.receivables.report',param.name,result);
						
						})

					break;
					case "数量":
					case "金额":
						that.selected_item('pos.produce.rank',param.name,['&','&',['date_order','>=',param.data.start_time],['date_order','<=',param.data.end_time],['product_id','=',param.data.product_id]],{context: {'group_by':'product_id'}});
					break;
				}
			}

		}

	    require(['echarts/config'],function(ecConfig){

			myChart.on(ecConfig.EVENT.CLICK, eConsole);
			myChart.on(ecConfig.EVENT.DBLCLICK, eConsole);
			myChart.on(ecConfig.EVENT.DATA_ZOOM, eConsole);
			myChart.on(ecConfig.EVENT.LEGEND_SELECTED, eConsole);
			myChart.on(ecConfig.EVENT.MAGIC_TYPE_CHANGED, eConsole);
			myChart.on(ecConfig.EVENT.DATA_VIEW_CHANGED, eConsole);

		})

    },
    loadChart:function(){
        // 指定图表的配置项和数据
        this.optionBar(this.$el.find("#SalesCharts .chart_show").get(0));
        this.optionPie(this.$el.find("#Income .chart_show").get(0))             
    },
});

var dd = new Date();

var today_home = Widget.extend(ct_pos_home.prototype,{
	active:1,
	date_start:0,
	date_end:0,
})

var Yesterday_home = Widget.extend(ct_pos_home.prototype,{
	active:2,
	date_start:-1,
	date_end:-1,
})

var This_week_home = Widget.extend(ct_pos_home.prototype,{
	active:3,
	date_start:(function(){
		return (dd.getDay() || 7)*-1+1
	})(),
	date_end:0,
})

var This_month_home = Widget.extend(ct_pos_home.prototype,{
	active:4,
	date_start:(function(){
		return dd.getDate()*-1+1
	})(),
	date_end:0,
})

core.action_registry.add('pos_today.index', today_home);
core.action_registry.add('pos_Yesterday.index', Yesterday_home);
core.action_registry.add('pos_This_week.index', This_week_home);
core.action_registry.add('pos_This_month.index', This_month_home);


});

