odoo.define('ct_dashboard.home', function (require) {
	"use strict";
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.Model');
var session = require('web.session');
var Dialog = require('web.Dialog');
var echart_ct = require("ct_dashboard.EchartView");
var QWeb = core.qweb;

return Widget.extend({
	willStart:function(){

        return ajax.loadJS('/ct_dashboard/static/src/js/lib/echarts.min.js');
        
    },
    Digital:function(number){

        return Number(number)>parseInt(number)?Number(number).toFixed(2):number;

    },
  	EchartCut:function(element,ChartDate){

        this.$(element).on('click',function(){

            ChartDate[$(this).addClass('active').siblings().removeClass('active').attr('dataDom')||'.echart2'].loadAjax()

        })

    },
    IsNull:function(data){

        if(typeof(data) === 'object' && Object.prototype.toString.call(data) === '[object Object]' && !data.length){
           
            return Object.keys(data);

        }else{

            return data;
        }

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
  	columnar:function(element,obj,pie){
         
      var myChart = echarts.init(this.$el.find(element).get(0));

      var ct_echart = new echart_ct();   

      obj = obj || {};  

      var option=pie?ct_echart.optionPie_cir(obj.data,obj.titleName,'pie'):ct_echart.optionBar(obj);

      myChart.setOption(option);

      myChart.resize()

      $(window).resize(function(){

         myChart.resize(); 

      });

      return myChart;

    },
    getAjax:function(url,callback){

        return ajax.jsonRpc(url, 'call', {}).done(function(result){

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

                    obrArray.name.push(name.toString().substr(0,8));

                    obrArray.val.push(val);

            });

         }else if(typeof(data) === 'object' && Object.prototype.toString.call(data) === '[object Array]'){

            $.each(data,function(name,val){

                    obrArray.obj.push(val);

                    obrArray.name.push(val.name.toString().substr(0,8));

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
    selected_item: function (event,modelName) {
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: modelName,
            res_id: $(event.currentTarget).data('id'),
            views: [[false, 'form']],
            target: 'current',
            context: {},
        });
    },
    AjaxLis:function(element,url,obj){

        var _self = this;

        var loadClick = function(obj){

            var refresh = $(_self.$el.find(element).get(0)).attr('dataDom');

            if(refresh){

                _self.$el.find(refresh).on('click',function(){

                    var loadAnima = _self.loadAnimation();

                    cutTable[obj.cut](obj.Sort,function(){

                        loadAnima.hide();

                    });

                })

            }

        };

        var getMode = function(Model){

            _self.$(element).find('tr').on('click',function(event){

                _self.selected_item(event,Model);
                
            })

            return true;

        }

        var cutTable = {

            list:function(s,callback){

                _self.getAjax(url,function(data){

                    if(!data.length){

                        return false;
                        
                    }

                    if(callback){

                        callback(data);

                    }

                    var html = new String(),mnsj;

                    mnsj = data.slice(0,6);

                    mnsj = !!s?_self.JsonSort(mnsj,s):mnsj;
                    
                    mnsj = mnsj.map(function(val){

                    $.each(val,function(name,value){

                        html += '<li>\
                                    <a href="">\
                                        <i class="fa fa-circle-o"></i>\
                                        <span class="m-l-xs">'+name+':'+value+'</span>\
                                    </a>\
                                </li>';

                    });

                    return html;

                }).join(' ');

                $(_self.$el.find(element).get(0)).html(mnsj);
                
                });

            },
            table:function(s,callback){

                _self.getAjax(url,function(data){

                    if(callback){

                        callback(data);

                    }
                   
                    var html = new String(),mnsj,empty=5,trHtml = $(_self.$el.find(element).get(0));
                    
                    if (data.length){

                        mnsj = data.slice(0,empty);

                        mnsj = !!s?_self.JsonSort(mnsj,s):mnsj;

                        $.each(mnsj,function(name,val){

                            html+= '<tr role="row" class="odd getId" data-id='+(data[name].id || 0)+'>';

                        $.each(val,function(a,b){

                            html+= '<td title="'+b+'">'+b+'</td>';

                        });

                        html+= '</tr>';

                        });

                    trHtml.html(html);

                    data[0]['model_name'] && getMode(data[0]['model_name']);

                    }

                    var trlen = _self.$el.find(element).find('tr').length;

                    var trHeLength = _self.$(element).parent('table').find('thead tr th').length;

                    var trRepeat = '<tr height="35" class="odd getId">';

                    for(var i=1;i<=trHeLength;i++){

                        trRepeat+='<td/>';

                    }

                    for(var i=1;i<=empty-trlen;i++){

                        trHtml.append(trRepeat);
                    
                    }

                    trHtml.find('tr:even').removeClass('odd').addClass('even');


                });
            }
        }

        try{

            loadClick(obj);    

            return cutTable[obj.cut](obj.Sort);

        }catch(e){

            console.log(e)

        }
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
});


    


});