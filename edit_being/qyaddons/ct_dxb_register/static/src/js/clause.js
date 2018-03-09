$(function(){

	var checkbox = $("#auth_signup button[type='submit']");

	$("#blankCheckbox").click(function(){

		if(this.checked){

			checkbox.removeAttr("disabled");

		}else{

			checkbox.attr("disabled","disabled");
		}
	});

    if(document.getElementById("reset_password")){

	var send_code = $("#send_code"),//发送验证码

		auth_second = $("#auth_second"),//重新获取验证码计时

		conds = 120,//倒计时

		PassRegExp = new RegExp("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,21}$");//密码长度限制

		auth = $("#auth"),//手机验证码

		login = $("#login"),//用户名

		tel = $("#tel"),//号码

		password = $("#password"),//密码

		passconfirm = $("#passconfirm"),//确认密码

		submit = $("#submit");//提交按钮

		var countdown = function(){//倒计时

		var	second = conds;

			auth_second.show().find("span").text(second);

			submit.attr("disabled","disabled");

		var	cord = setInterval(function(){

				second--;

				auth_second.find("span").text(second<0?0:second);

				if(second<=0){

					clearInterval(cord);

					send_code.removeAttr("disabled");

					auth_second.hide();

				}

			},1000);

			send_code.attr("disabled","disabled");

		},
		isdisable = function(result){//验证 验证码密码

			auth.add(password).add(passconfirm).parents(".form-group").removeClass('has-error');

			if(auth.val()==result && PassRegExp.test(password.val()) && password.val() == passconfirm.val()){

				submit.removeAttr("disabled");

			}else{

				if(auth.val()!=result){

					auth.parents(".form-group").focus().addClass('has-error');

				}else{

					(!PassRegExp.test(password.val())?password:password.val() != passconfirm.val()?passconfirm:$('')).parents(".form-group").addClass('has-error');
				}
				
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

							new Dialog(null, {

						        size: 'medium',

						        title: "手机号验证错误！",

						        $content: $('<div>').html("该用户不存在或者该手机号未绑定该账户")
						    
						    }).open();

						    return false;
						}

						countdown();

						password.add(passconfirm).add(auth).off("input").on("input",isdisable.bind(this,result));
					
					})
				})
			
		}

		send_code.on("click",function(){//获取验证码动作

			login.add(tel).parents(".form-group").removeClass('has-error');

			if(!login.val() || !tel.val()){

				(login.val()?tel:login).focus().parents(".form-group").addClass('has-error');

				return false;

			}

			getCode({

				login:login.val(),
				
				tel:tel.val()
			});

		})

	}

})