odoo.define('cotong.hr', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var Model = require('web.Model');
var session = require('web.session');
var Dialog = require('web.Dialog');
var echart_ct = require("ct_dashboard.EchartView");
var QWeb = core.qweb;

var CTHR = Widget.extend({
    template: 'HRIndex',
    willStart: function() {
        return ajax.loadJS('/ct_dashboard/static/src/js/lib/echarts.min.js');
    },
    start:function(){

        this._super();

        this.DragSort('#content','.droptarget','.ibox-title')

        var ChartDate=this.loadChart();

        this.loadClick('.chartLoad',ChartDate);

        this.zoomClick('.fa-expand',ChartDate);

        //this.AjaxLis('#salaryWelfTable','table');
         //试用期/总人数
        ajax.jsonRpc('/hr/staff_three_ratio', 'call',{}).done(function(result){
            var ArrayJSon=(function(){
                var array=[];
                $.each(result,function(name,val){
                    array.push({value:val, name:name});
                })
                return array;
            })();

            $(".messages_col span.title").html();

            var testMember = ArrayJSon[1].value;
            var cadet = ArrayJSon[2].value;
            var allMember = ArrayJSon[0].value;

            $("#testMember").html(testMember);
            $("#cadet").html(cadet);
            $("#allMember").html(allMember);
        }.bind(this));

        //新人人数/总人数
        ajax.jsonRpc('/hr/staff_status', 'call',{}).done(function(result){
            var ArrayJSon=(function(){
                var array=[];
                $.each(result,function(name,val){
                    array.push({value:val, name:name});
                })
                return array;
            })();

            $(".messages_col span.title").html();

            var newMember = ArrayJSon[1].value;
            var atStatusMember = ArrayJSon[2].value;
            var notStatusMember = ArrayJSon[0].value;

            $("#newMember").html(newMember);
            $("#atStatusMember").html(atStatusMember);
            $("#notStatusMember").html(notStatusMember);

        }.bind(this));

        //合同签订等
        ajax.jsonRpc('/hr/staff_contract_status', 'call',{}).done(function(result){
            //console.log(result);
            var ArrayJSon=(function(){
                var array=[];
                $.each(result,function(name,val){
                    array.push({value:val, name:name});
                })
                return array;
            })();

            $(".messages_col span.title").html();
            
            var notPact = ArrayJSon[0].value;
            var timeoutPact = ArrayJSon[1].value;
            var alreayPact = ArrayJSon[2].value;

            $("#notPact").html(notPact);
            $("#alreayPact").html(alreayPact);
            $("#timeoutPact").html(timeoutPact);

        }.bind(this));

        
    },
    Digital:function(number){

        return Number(number)>parseInt(number)?Number(number).toFixed(2):number;

      },
      DragSort:function(fill,dragBox,drag){

            var fi = this.$el.find(fill),Storage = this.template,

            startDom = $(this.$el.find(dragBox)),

            setStorage = function(name,data){

                 localStorage.setItem(name,JSON.stringify(data)); 
            },
            getStorage = function(name){

                return JSON.parse(localStorage.getItem(name));
            },
            clearStorage = function(name){

                localStorage.removeItem(name);
            },
            listArray = function(DOM){

                var arr = new Array();

                DOM.each(function(){

                    arr.push($(this).attr('data-pos'));

                });

                return arr;
            },
            reseSort = function(){

                var startArray;

                if(!getStorage(Storage) || getStorage(Storage).length!=startDom.length){

                        startArray = [];

                        startDom.each(function(i){

                            startArray.push(i);

                        });

                        setStorage(Storage,startArray);
                }

                startSort();
            },
            startSort = function(){

                var arr = new Array(); 

                $.each(getStorage(Storage),function(i,val){//索引 值

                    startDom.eq(i).attr('data-pos',i)

                    arr[i] = startDom.get(val);

                });

                $(fi).html(arr);
                
            }
            reseSort();
            this.$el.find(dragBox).find(drag).on({
                'mousedown':function(){
                    $(this).parents(dragBox).prop('draggable',true);

                },
                'mouseup':function(){

                    $(this).parents(dragBox).prop('draggable',false);

                }
            })

            if(navigator.userAgent.indexOf("Firefox")>-1){

               /* 拖动开始*/
            document.addEventListener("dragstart", function(event) {

                if ( event.target.className === "droptarget" ) { 

                    event.dataTransfer.setData("sortDrag", event.target.id);

                 }

            });

            // 拖动完成
            document.addEventListener("dragend", function(event) {

                event.preventDefault();

                setStorage(Storage,listArray($(dragBox)));

            });

            //在放置目标
            document.addEventListener("dragover", function(event) {

                event.preventDefault();

            });

            //放置目标
            document.addEventListener("drop", function(event) {

                 event.preventDefault();

                 if ( event.target.className === dragBox.substr(1)) { 

                 var data = event.dataTransfer.getData("sortDrag");

                 if(document.getElementById(event.target.id).compareDocumentPosition(document.getElementById(data))==4){

                     $('#'+event.target.id).before($('#'+data));

                 }else{

                     $('#'+event.target.id).after($('#'+data));

                 }
                    $('#'+data).prop('draggable',false);

                 }
               
            });

            }else{

            this.$el.find(dragBox).on({'dragstart':function(){

                event.dataTransfer.setData("sortDrag",this.id);

            },'dragend':function(event){

                event.preventDefault();

                setStorage(Storage,listArray($(dragBox)));

            },'dragover':function(event){

                event.preventDefault();

            },'drop':function(){

                 event.preventDefault();

                 var data = event.dataTransfer.getData("sortDrag");

                 if(document.getElementById(this.id).compareDocumentPosition(document.getElementById(data))==4){

                     $(this).before($('#'+data));

                 }else{

                     $(this).after($('#'+data));

                 }

                 $('#'+data).prop('draggable',false);

            }});

            }
      },
    loadChart:function(){
        // 指定图表的配置项和数据
        var _self = this;

        var ChartDate={

            '.echart_hr0':{  //部门统计

                url:'/hr/staff_department_num',

                loadAjax:function(callback){

                   _self.getAjax(this.url,function(result){

                    if(!Object.keys(result).length){

                        return false;
                    }

                    if(callback){

                        callback(result);

                    }

                    _self.pie_circle('.echart_hr0',result);

                  });

                }
             },
            '.echart_hr1':{  //在职统计

                url:'/hr/staff_ratio',

                loadAjax:function(callback){

                   _self.getAjax(this.url,function(data){

                    if(!Object.keys(data).length){

                        return false;
                    }

                    if(callback){

                        callback(data);
                    }

                    data=_self.EChartilze(data);

                    _self.pie_circle('.echart_hr1',data.obj);

                  });

                }
              },
            '.echart_hr3':{  //年龄统计

                url:'/hr/staff_birthday',

                loadAjax:function(callback){

                   _self.getAjax(this.url,function(data){

                    if(callback){

                        callback(data);
                    }

                    data=_self.getAge(data);

                    _self.columnar('.echart_hr3',{

                    text:"（单位：人）",

                    xAxisDate:["20以下","20-30","30-40","40-50","50-60","60+"],

                    series:{

                        name:'（单位：人）',

                        type:'bar',

                        data: data

                    },

                    d:"",

                    aximat:"",

                    max:Math.max(10,Math.max.apply(null,data)+10),

                    min:0,

                    }  
                    );

                  });

                }
              },
            '.echart_hr2':{  //性别统计

                url:'/hr/staff_gender',

                loadAjax:function(callback){

                   _self.getAjax(this.url,function(data){

                    if(!Object.keys(data).length){

                        return false;
                    }

                    if(callback){

                        callback(data);
                    }

                    data=_self.EChartilze(data);

                    _self.pie_circle('.echart_hr2',data.obj);

                  });

                }
              },
            '.echart_hr4':{  //学历统计

                url:'/hr/staff_education',

                loadAjax:function(callback){

                   _self.getAjax(this.url,function(result){

                    if(!Object.keys(result).length){

                        return false;
                    }

                    if(callback){

                        callback(result);

                    }

                    var data=_self.EChartilze(result);

                     _self.columnar('.echart_hr4',{

                    text:"（单位：人）",

                    xAxisDate:["初中", "高中", "大专","本科","硕士", "博士","其他"],

                    series:{

                    name:'（单位：人）',

                    type:'bar',

                    data:[{name:'初中',value:result['初中']},
                        {name:'博士',value:result['博士']},
                        {name:'大专',value:result['大学专科']},
                        {name:'本科',value:result['大学本科']},
                        {name:'硕士',value:result['硕士']},
                        {name:'高中',value:result['高中/职高/中专']},
                        {name:'其他',value:result['其他']}]

                    },

                    d:"",

                    aximat:"",

                    max:Math.max(10,Math.max.apply(null,data.val)+10),

                    min:0,

                    });

                  });

                }
             },

        };
        $.each(ChartDate,function(name,val){

            window.requestAnimationFrame(function(){

                val.loadAjax();

            });

        })
        
        return ChartDate;
    },
    columnar:function(element,obj){
         
      var myChart = echarts.init(this.$el.find(element).get(0));

      var ct_echart = new echart_ct();     

      var option=ct_echart.optionBar(obj||{});

      myChart.setOption(option);

      myChart.resize()

      $(window).resize(function(){

         myChart.resize(); 

      });

      return myChart;

    },
    pie_circle:function(element,obj){
         
      var myChart = echarts.init(this.$el.find(element).get(0));

      var ct_echart = new echart_ct();     

      var option=ct_echart.optionPie_cir(obj||{},"人数比例","pie");

      myChart.setOption(option);

      myChart.resize()

      $(window).resize(function(){

         myChart.resize(); 

      });

      return myChart;

    },
    getAjax:function(url,callback){

         ajax.jsonRpc(url, 'call', {}).done(function(result){

            if(callback){

                callback(result);
            }

        });

    },
    EChartilze:function(data,sort){

         var obrArray = {name:[],obj:[],val:[]},

            _self = this;

         if(typeof(data) === 'object' && Object.prototype.toString.call(data) === '[object Object]' && !data.length){

            $.each(data,function(name,val){

                obrArray.obj.push({'name':name,'value':_self.Digital(val)});

                obrArray.name.push(name.substr(0,8));

                obrArray.val.push(val);

            });

         }else if(typeof(data) === 'object' && Object.prototype.toString.call(data) === '[object Array]'){

            $.each(data,function(name,val){

                obrArray.obj.push(val);

                obrArray.name.push(val.name.substr(0,8));

                obrArray.val.push(_self.Digital(val.value));

            });

         }

         if(sort){

            for(var i=0;i<obrArray.val.length;i++){

            for(var j=i;j<obrArray.val.length;j++){

                if(obrArray.val[i]<obrArray.val[j]){

                var temp=[obrArray.name[i],obrArray.obj[i],obrArray.val[i]];

                obrArray.name[i] = [obrArray.name[j],obrArray.obj[i]=obrArray.obj[j],obrArray.val[i]=obrArray.val[j]][0];

                obrArray.name[j]=temp[0];

                obrArray.obj[j]=temp[1];

                obrArray.val[j]=temp[2];
                
                 }
              }
          }

        }

        return obrArray;

    },
    loadAnimation:function(){

        $('.chartUpdate').remove().empty();

        var updateChart,hideEvent;

        updateChart =$('<div class="chartUpdate"><div class="spinner"><div class="rect1"></div><div class="rect2"></div><div class="rect3"></div><div class="rect4"></div><div class="rect5"></div></div></div>').appendTo('.o_content');

        hideEvent = {

            hide:function(){

            $(updateChart).animate({'opacity':0},1000,function(){

                    $(this).off().remove().empty();

            });
        }};

        updateChart.on('click',function(){

            hideEvent.hide();

        })

        return hideEvent;

    },
    loadClick:function(element,ChartDate){

           var _self=this;

           _self.$el.find(element).on('click',function(){

              try{
                    var ThisBinDate = $(this).attr('dataDom'),

                    updateChart;

                    if(ThisBinDate){

                        updateChart = _self.loadAnimation();

                         ChartDate[ThisBinDate].loadAjax(function(data){

                            updateChart.hide();

                        });

                    }

                }catch(e){

                    console.log(e);
                }

        });
    },
  zoomClick:function(element,ChartDate){

        var EcharDom,

        _self=this,

        ThisBinDate;

        this.$el.find(element).on('click',function(){

            if(EcharDom=$(this).attr('dataDom')){

                if(!($(EcharDom).hasClass('zooMax'))){

                    $(EcharDom).addClass('zooMax').find('.fa.fa-expand').addClass("fa-compress");
                    $(".animated").removeClass('active');

                }else{
                    $(EcharDom).removeClass('zooMax').find('.fa.fa-expand').removeClass("fa-compress");
                    $(".animated").addClass('active');
                }

                try{

                     ThisBinDate = $(this).attr('dataResize');

                     if(ThisBinDate){

                        ChartDate[ThisBinDate].loadAjax();

                     }

                }catch(e){

                    console.log(e);
                }
            }
        });
    },
    JsonSort:function(d,s){

        var sortData={};

            sortData = d.map(function(value){

                var data={};

                s.forEach(function(val,index){

                    data[val] = value[val];

                });

                return data;

            });

            return sortData;
    },
    getAge:function(birthday){

        var ageArray = new Array(),rangData;

        if(birthday===false) {

            return false;

        }else {

            birthday = birthday.filter(function(val){
                return val!==false;
            })

            rangData = birthday.map(function(val){
                return (new Date()-new Date(val))/1000/3600/24/365;
            });

            ageArray=[
            rangData.filter(function(val){
                return val<20;
            }).length,
            rangData.filter(function(val){
                return val>=20 && val<30;
            }).length,
            rangData.filter(function(val){
                return val>=30 && val<40;
            }).length,
            rangData.filter(function(val){
                return val>=40 && val<50;
            }).length,
            rangData.filter(function(val){
                return val>=60;
            }).length,
            rangData.filter(function(val){
                return isNaN(val);  
            }).length,
            
            ]

        }

        return  ageArray;
    }
});

core.action_registry.add('hr.index', CTHR);

return CTHR;
});

