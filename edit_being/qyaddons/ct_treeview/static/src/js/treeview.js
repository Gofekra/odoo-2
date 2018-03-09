odoo.define('treeview.HomeView', function (require) {
"use strict";
var ajax = require('web.ajax');
var config = require('web.config');
var core = require('web.core');
var Model = require('web.Model');
var Widget = require('web.Widget');
var QWeb = core.qweb;
var ListView = require('web.ListView');

    var conArray = function(result){
        switch(typeof result){
            case 'string':
                return $.parseJSON(result);
                break;
            default:
                return result;
                break;
        }
    };

    ListView.include({
        load_list:function(){
            this._super();
            //drag
            this.drag();
            return $.when();
        },
        drag:function(){
            var parent = this;
            +(function(Sortdefind){
              try{
                var sort = Sortdefind('sortTable');
                sort.init({
                  el:'.table-responsive :not(.o_list_view_grouped)',
                  drag:'thead tr th:not(.o_list_record_selector)',
                  dragsync:{
                    el:'tbody tr,tfoot tr',
                    find:'td:not(.o_list_record_selector,:first-child)'
                  },
                  dragact:'TDrag'
                });
              }catch(e){
                console.log(e)
              }
            })(function(amd){
              var Sortdefind = (function(mod){
                mod.sortTable = (function(){
                  function sortTable(){
                    this.option = {
                    };
                  }
                  sortTable.prototype = {
                    data:[],
                    init:function(config){
                      var el = $.extend(this.option,config)
                      self = this;
                      this.el = parent.$(el.el);
                      this.drag = this.el.find(el.drag);
                      this.sel = this.el.find(el.dragsync.el);
                      this.initSort().done(function(){
                        self[el.way]?self[el.way]():self.column();
                      });
                    },
                    initSort:function(){
                        var self = this,
                            dtd = $.Deferred();
                        this.local.get().then(function(result){
                            result = conArray(result);
                            self.data = result.length?result:self.initData(self.drag);
                            self.thead();
                            self.tbody();
                            dtd.resolve();
                        });
                        return dtd.promise();
                    },
                    thead:function(){
                        var thead = new Array(),
                            self = this;
                            $.each(this.data,function(index,val){
                                thead.push(self.drag.get(val));
                            });
                            $.each(thead,function(index,val){
                                self.drag.parent().append(thead[index]);
                            })
                    },
                    tbody:function(){
                        var tbody = new Array();
                            self = this;
                            this.sel.each(function(index,val){
                               tbody = [];
                                var tr = $(this),
                                    td = tr.find(self.option.dragsync.find);
                               $.each(self.data,function(i,v){
                                    tbody.push(td.eq(v));
                               });
                               td.each(function(i,v){
                                    tr.append(tbody[i]);
                               });
                            })

                    },
                    initData:function(sort){
                      var self = this;
                      $(sort).each(function(index){
                        self.data.push(index);
                      });
                      return this.data;
                    },
                    column:function(){
                      var x = 0,
                          index = 0,
                          self = this,
                          drag = false;
                      this.drag.on('mousedown',function(e){
                        var _self = $(this),down,up;
                        x = e.clientX;
                        drag = true;
                        index = $(this).index()-1;
                        self.ClassSilde(index);
                        $(this).addClass(self.option.dragact).siblings().removeClass(self.option.dragact);
                        $(document).on({
                          mousemove:down=function(e){
                              if(drag){
                                  _self.css({left:(e.clientX-x)+'px'});
                                  self.sel.find('.'+self.option.dragact).css({left:(e.clientX-x)+'px'});
                                }
                              return false;
                          },
                          mouseup:up=function(e){
                            var x = e.clientX;
                            drag = false;
                            self.drag.not('.'+self.option.dragact).each(function(){
                              var left = $(this).offset().left,
                                  width = $(this).outerWidth(),
                                  TheIndex = $(this).index()-1;
                              if(x>=left && x<left + width){
                                if(TheIndex>index){
                                  $(this).after(_self);
                                  self.insert(TheIndex,1);
                                }else{
                                  $(this).before(_self);
                                  self.insert(TheIndex,0);
                                }
                                self.data.splice(TheIndex,0,Number(self.data.splice(index,1).join()));
                              }
                            });
                            self.drag.removeClass(self.option.dragact).removeAttr('style');
                            self.sel.find('.'+self.option.dragact).removeAttr('style').removeClass(self.option.dragact);
                            $(document).off('mousemove',down).off('mouseup',up);
                            self.http(self.data);
                          }
                        });
                      });
                    },
                    ClassSilde:function(index){
                      this.sel.find(this.option.dragsync.find+':eq('+index+')').addClass(this.option.dragact).siblings().removeClass(this.option.dragact)
                    },
                    insert:function(index,place){
                      var self = this;
                      this.sel.each(function(){
                        if(place){
                          $(this).find(self.option.dragsync.find).eq(index).after($(this).find('.'+self.option.dragact));
                        }else{
                          $(this).find(self.option.dragsync.find).eq(index).before($(this).find('.'+self.option.dragact));
                        }
                      });
                    },
                    http:function(sort){
                        this.local.set(sort);
                    },
                    local:(function(){
                        var Ajax = function(data){
                            return ajax.jsonRpc('/treeview/order_test', 'call', data);
                        }
                        return {
                            set:function(data){
                                Ajax({
                                    key:'T'+parent.name,
                                    val:JSON.stringify(data)
                                })
                            },
                            get:function(){
                                return Ajax({
                                    key:'T'+parent.name
                                })
                            }
                        };
                    })()
                  };
                  return sortTable;
                })();
                return mod;
              })(Sortdefind || {});
              return Sortdefind[amd]?new Sortdefind[amd]():{};
            });
        }
    })

});