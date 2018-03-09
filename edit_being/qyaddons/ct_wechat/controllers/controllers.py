# -*- coding: utf-8 -*-
import logging,json,urlparse
from odoo import http
from odoo.http import  request

_logger = logging.getLogger(__name__)
import  urllib2,urllib

# wx_appid='wx6e8a286d0b9761bf'
# wx_AppSecret='6caf3b6838aa07ac22aacdbd5662e78e'

class WeiXinLogin(http.Controller):
    def __init__(self):
        param = request.env()['ir.config_parameter']
        self.wx_appid = param.get_param('wx_appid') or ''
        self.wx_AppSecret = param.get_param('wx_AppSecret') or ''

        from ..rpc import oa_client
        oa_client.init_oa_client(self.wx_appid, self.wx_AppSecret)

    def send_url(self,token_url, params):
        try:
            request = urllib2.Request(token_url, data=urllib.urlencode(params))
            get_data = urllib2.urlopen(request).read()
            sort_data = json.loads(get_data)
            return sort_data
        except Exception, e:
            _logger.info("获取参数错误：")

    def get_token(self,res_code):
        # 2.通过code换取网页授权access_token

        token_url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid':self.wx_appid,
            'secret': self.wx_AppSecret,
            'code': res_code['code'],
            'grant_type': 'authorization_code'
        }
        return self.send_url(token_url, params)



    @http.route('/wx/MP_verify_UWWzP166f4TEaVNu.txt',type='http', auth="none", methods=['GET', 'POST'], csrf=False)
    def wx_lweb(self, **kw):
        _logger.info("读取文件夹")
        return 'UWWzP166f4TEaVNu'


    #微信用户验证
    def check_code(self,redirect_uri):
        return  request.render('ct_wechat.weixin_daili', {
                "target": 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+self.wx_appid+'&'+redirect_uri+'&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
            })

    #运用Auth_sinup 获取Token进行外部登录
    def get_user_token_password(self,username,url):
        data = {
            'login':str(username)
        }
        url ='http://'+str(url)+'/web/commit_reset_token'
        print data,url
        request = urllib2.Request(url, urllib.urlencode(data))
        response = urllib2.urlopen(request).read()  # 打开实时请求request
        sort_data = json.loads(response)
        password_token= sort_data['oauth_access_token']
        if password_token:
            return password_token
        else:
            raise UserWarning('用户名身份验证失败，请重新输入')

    #查看关联用户进行绑定
    def get_user_bind(self):
        password_token=''
        return password_token



    def check_weixin_action(self,kwargs):
        res_users = self.get_token(kwargs)
       #  openid =  'obcxKwd5W-VtOyzvXYX6ldHCIkRA'
        openid = res_users['openid']
        if openid:
            # 查询是否已绑定微信

            #1、主账号
            weixin_id = request.env['res.partner.about.openid'].sudo().search([('openid', '=', openid)])
            if not weixin_id:
                _logger.info("进行微信绑定")
                return request.render('ct_wechat.check_username', {'openid': openid})
            else:
                res = request.env['saas_portal.client'].sudo().search([('partner_id', '=', weixin_id.partner_id.id)])
                # callbackurl = str(res.name) + '/web#view_type=kanban&model=pos.config&menu_id=287&action=399&'
                # user_password=self.get_user_token_password(weixin_id.username,res.name)
                return request.render('ct_wechat.weixin_daili', {
                    "cors": {
                        "cite": str(res.name),
                        "login": str(weixin_id.partner_id.username),
                        "password": str(weixin_id.partner_id.user_password),
                        "id": 339
                    }
                })
        else:
            raise UserWarning('身份验证失败，请退出重新尝试')

    # 微信公众号菜单调整接口---引导用户点击微信授权页面
    @http.route('/daili', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def web_daili(self, **kwargs):
        _logger.info("微信免登录代理 %s" % (kwargs))
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        callbackurl = urlparse.urljoin(base_url, '/wx/login')
        url = {'redirect_uri': callbackurl}
        redirect_uri=urllib.urlencode(url)
        return  self.check_code(redirect_uri)







    #网页授权完毕，进行获取用户信息验证，验证结束登陆到对应的网站
    @http.route('/wx/login', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def wx_login(self,**kwargs):
        return self.check_weixin_action(kwargs)


    #网页授权接口
    @http.route('/wx', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def wx_daili(self,**kwargs):
        # 网页授权完毕，进行获取用户信息验证，验证结束登陆到对应的网站
        if kwargs:
            return self.check_weixin_action(kwargs)
        else:
            base_url = request.env['ir.config_parameter'].get_param('web.base.url')
            callbackurl = urlparse.urljoin(base_url, '/wx/login')
            url = {'redirect_uri': callbackurl}
            redirect_uri = urllib.urlencode(url)
            return self.check_code(redirect_uri)


    def check_cluster_user(self,partner_id,database,username,user_password,openid,phone):
        res=request.env['res.partner.about.user'].sudo().search([('username','=',username),('partner_id','=',partner_id.id)])
        if res:
            if res.partner_id.user_password != user_password:
                return request.render('ct_wechat.check_username', {
                    'message': "你提交的密码有误,请重新输入，或者直接联系客服！",
                    'phone': phone
                })
            else:
                if res.partner_id.phone != phone:
                    return request.render('ct_wechat.check_username', {
                        'message': "你提交的手机号有误,请重新输入，或者直接联系客服！",
                        'phone': phone
                    })
                else:
                    res.open_id = openid
                    url = str(database) + '/web/login'
                    # user_password = self.get_user_token_password(username, database)
                    return request.render('ct_wechat.weixin_daili', {
                        "cors": {
                            "cite": url,
                            "login": str(username),
                            "password": str(user_password)
                        }
                    })
        else:
            return request.render('ct_wechat.check_username', {
                        'message': "你提交的账户有误,请重新输入，或者直接联系客服！",
                        'phone': phone
                    })



    def check_main_user(self,database,username,user_password,openid,phone):

        res = request.env['saas_portal.client'].sudo().search([('name', '=', database)])
        if res:
            #先判断该用户是否为主账户/从账户
            if res.partner_id.username != username:
                #当主帐户不存在时寻找关联用户
                return self.check_cluster_user(res.partner_id,database,username,user_password,openid,phone)
            else:
                if res.partner_id.user_password != user_password:
                    return request.render('ct_wechat.check_username', {
                        'message': "你提交的密码有误,请重新输入，或者直接联系客服！",
                        'phone': phone
                    })
                else:
                    if res.partner_id.phone != phone:
                        return request.render('ct_wechat.check_username', {
                            'message': "你提交的手机号有误,请重新输入，或者直接联系客服！",
                            'phone': phone
                        })
                    else:
                        # res.partner_id.about_openid_ids |= openid
                        request.env['res.partner.about.openid'].sudo().create({'openid':openid, 'partner_id': res.partner_id.id})
                        # url = str(database) + '/web#view_type=kanban&model=pos.config&menu_id=287&action=399&'
                        # user_password = self.get_user_token_password(username, database)
                        return request.render('ct_wechat.weixin_daili', {
                            "cors": {
                                "cite": str(database),
                                "login": str(username),
                                "password": str(user_password),
                                "id":339
                            }
                        })
        else:
            return request.render('ct_wechat.check_username', {
                'message': "你提交的账套名有误,请重新输入，或者直接联系客服！",
                'phone':phone
            })

    #根据用户输入的账套进行验证，记录用户的信息
    @http.route('/bind/openid', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def wx_bind(self, **kwargs):
        database=kwargs['bookname']
        username=kwargs['firstname']
        user_password=kwargs['inputPassword']
        openid=kwargs['openid']
        phone=kwargs['phone']
        return  self.check_main_user(database,username,user_password,openid,phone)



    @http.route('/wx/test', type="http", auth='none', methods=['GET', 'POST'], csrf=False)
    def wx_test(self, **kwargs):
        return request.render('ct_wechat.check_username')
#
# def check_token(res_token):
#     #3.检验授权凭证（access_token）是否有效
#     url='https://api.weixin.qq.com/sns/auth'
#     params = {
#         'openid': res_token['openid'],
#         'access_token':res_token['access_token']
#     }
#     check_res = send_url(url,params)
#     if check_res['errcode']==0:
#         return res_token
#     else:
#         # 如果access_token超时，那就刷新
#         url='https://api.weixin.qq.com/sns/oauth2/refresh_token?'
#         params = {
#             'appid': wx_appid,
#             'grant_type':'refresh_token',
#             'refresh_token':res_token['refresh_token']
#         }
#         return  send_url(url, params)
#
#
#
# def get_user(res_check):
#     url = u'https://api.weixin.qq.com/sns/userinfo'
#     params = {
#         'access_token': res_check["access_token"],
#         'openid': res_check["openid"],
#     }
#     # 4.拉取用户信息
#     return send_url(url, params)


