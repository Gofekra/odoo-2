$(function(){

	$(".o_database_list").addClass('reg_reset');

	var checkbox = $("#auth_signup button[type='submit']");

	$("#blankCheckbox").click(function(){

		if(this.checked){

			checkbox.removeAttr("disabled");

		}else{

			checkbox.attr("disabled","disabled");
		}
	});

    if(document.getElementById("reset_password")){

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

		send_submit = STATES.newborn,

		PassRegExp = new RegExp("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,21}$"),//密码长度限制

		auth = $("#auth"),//手机验证码

		login = $("#login"),//用户名

		tel = $("#tel"),//号码

		password = $("#password"),//密码

		passconfirm = $("#passconfirm"),//确认密码

		submit = $("#submit");//提交按钮

		var countdown = function(){//倒计时

		var	second = conds;

			auth.attr("placeholder","倒计时"+second+"秒");

			submit.attr("disabled","disabled");

			conds_state = STATES.timing;

		var	cord = setInterval(function(){

				second--;

				auth.attr("placeholder","倒计时"+(second<0?0:second)+"秒");

				if(second<=0){

					clearInterval(cord);

					send_code.removeAttr("disabled");

					conds_state = STATES.overdue;

					auth_second.hide();

				}

			},1000);

			send_code.attr("disabled","disabled");

		},
		isdisable = function(result){//验证 验证码密码

			auth.add(password).add(passconfirm).parents(".form-group").removeClass('has-error');

			if(auth.val()==result && PassRegExp.test(password.val()) && password.val() == passconfirm.val()){

				submit.removeAttr("disabled");

				send_submit = STATES.overdue;

			}else{

				if(auth.val()!=result){

					auth.parents(".form-group").focus().addClass('has-error');

				}else{

					(!PassRegExp.test(password.val())?password:password.val() != passconfirm.val()?passconfirm:$('')).parents(".form-group").addClass('has-error');
				}

				send_submit = STATES.runing;
				
				submit.attr("disabled","disabled");

			}
		},
		getCode = function(data){//得的验证码

				odoo.define("cotong_clause",function(require){

					var ajax = require('web.ajax');

					var Dialog = require('web.Dialog');

					ajax.jsonRpc("/web/commit_send_message", 'call',data).then(function(result){

						if(!result){

							tel.add(login).parents(".form-group").addClass('has-error');

							alert("该用户不存在或者该手机号未绑定该账户!!!");

						    return false;
						}

						conds_state = STATES.runing;

						countdown();

						password.add(passconfirm).add(auth).off("input").on("input",isdisable.bind(this,result));
					
					})
				})
			
		}

		$("#reset_password").on("submit",function(e){

			if(send_submit!=STATES.overdue){

				e.preventDefault();

				return false;
			}
			
		})

		send_code.on("click",function(){//获取验证码动作

			if(conds_state==STATES.newborn || conds_state==STATES.overdue){

				login.add(tel).parents(".form-group").removeClass('has-error');

				if(!login.val() || !tel.val()){

					(login.val()?tel:login).focus().parents(".form-group").addClass('has-error');

					return false;

				}

				getCode({

					login:login.val(),
					
					tel:tel.val(),

					type:'reset'
				});

			}

		})

	}

})