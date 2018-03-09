odoo.define("wechat_com",function(require){
'use strict';
  console.log(11);
	var ajax = require('web.ajax');
	var Dialog = require('web.Dialog');

// 状态的映射
	var STATES = {

	    newborn: 'newborn',  // 刚创建

	    timing: 'timing',    // 正在倒计时过期处理

	    runing: 'runing',    // 正在运行中的数据

	    overdue: 'overdue'   // 已经过期了
	};

	var send_code = $("#send_code"),//发送验证码

		conds = 120,//倒计时

		conds_state = STATES.newborn,//倒计时状态

		next_state = STATES.newborn,//下一步状态

        bookname=$("#bookname"),//域名

        login = $("#firstname"),//用户名

		auth = $("#code"),//手机验证码

		tel = $("#phone"),//手机号码

		password = $("#password"),//密码

		nextinfo = $("#next_step"),//下一步

		submit = $("#btn_submit");//提交按钮

	var countdown = function(){//倒计时

		var	second = conds;

			auth.attr("placeholder","倒计时"+second+"秒");


			conds_state = STATES.timing;

		var	cord = setInterval(function(){

			second--;

			auth.attr("placeholder","倒计时"+(second<0?0:second)+"秒");

			if(second<=0){

				clearInterval(cord);

				send_code.removeAttr("disabled");

				conds_state = STATES.overdue;

				auth.removeAttr('placeholder');

			}

		},1000);

		send_code.attr("disabled","disabled");

	},
	isdisable = function(result){//验证 验证码密码

		next_state = STATES.timing;

		auth.parents(".form-group").removeClass('has-error');

		if(auth.val()==result){

			next_state = STATES.overdue;

			nextinfo.removeAttr("disabled");

		}else{

			next_state = STATES.runing;

			auth.parents(".form-group").focus().addClass('has-error');

			nextinfo.attr("disabled","disabled");

		}
	},
	getCode = function(data){//得到验证码
      console.log(data)
		ajax.jsonRpc("/web/commit_send_message", 'call',data).then(function(result){

			console.log(result);

			conds_state = STATES.runing;

			countdown();

			auth.off("input").on("input",isdisable.bind(this,result));

		})

	}

	send_code.on("click",function(){//获取验证码动作

		if(conds_state==STATES.newborn || conds_state==STATES.overdue){

			login.add(tel).parents(".form-group").removeClass('has-error');

			if(!tel.val()){

				tel.focus().parents(".form-group").addClass('has-error');

				return false;

			}
           console.log(tel.val())
			getCode({

				tel:tel.val(),
				type:'register'
			});

		}

	})

	nextinfo.on("click",function(){

		if(next_state==STATES.newborn || next_state==STATES.overdue){

			$("#next_confirm").hide();

			$("#form_group").removeClass('hidden').show();

		}

	})


})


