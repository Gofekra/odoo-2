var weixin_cors = function(obj){

	function domainData(url, fn){

		var token = document.getElementById('token');

		if(token){

			document.body.removeChild(token);

		}

		var isFirst = true;

		var iframe = document.createElement('iframe');

		iframe.id = 'token';

		iframe.style.display = 'none';

		var loadfn = function(){

		if(isFirst){

                isFirst = false;

                fn(iframe);

                iframe.contentWindow.location = '/ct_wechat/static/Center/poly.html';// 设置的代理文件

            } else {

                document.body.removeChild(iframe);

                iframe.src = '';

                iframe = null;

            }
        };

        iframe.src = url;

		if(iframe.attachEvent){

            iframe.attachEvent('onload', loadfn);

        } else {

            iframe.onload = loadfn;

        }

        document.body.appendChild(iframe);
    }

	var home = new Vue({

		el:"#app",

		data:{

			// cite:"http://"+obj.cite+"/web/login#view_type=kanban&model=pos.config&action="+obj.id,
			cite:"http://"+obj.cite+"/web/login",

			name:obj.login,

			password:obj.password,

			tokenValue:null
		},
		computed:{
			token:function(self){

				if(self.cite && self.name && self.password){

					domainData(self.cite,function(iframe){

					});

					return this.tokenValue;

				}
			}
		}
	})

	window.addEventListener('message',function(e){

		home.tokenValue = e.data;
		var cors = document.querySelector("form");
		cors.setAttribute('action',home.cite);
		setTimeout(function(){
			document.querySelector("button[type='submit']").click();
		},1000);
	},false);
};