# coding: utf-8
"""
 * 支付宝接口公用函数 python版本
 * 详细：该类是请求、通知返回两个文件所调用的公用函数核心处理文件
 * 版本：1.0
 * 日期：2012-07-19（官方）本接口写于2017年新春
 * 说明：
"""

import json
import sys
import types

from base64 import b64encode,b64decode
from urllib import urlencode

def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):  
    if strings_only and isinstance(s, (types.NoneType, int)):  
        return s  
    if not isinstance(s, basestring):  
        try:  
            return str(s)  
        except UnicodeEncodeError:  
            if isinstance(s, Exception):  
                return ' '.join([smart_str(arg, encoding, strings_only,  
                        errors) for arg in s])  
            return unicode(s).encode(encoding, errors)  
    elif isinstance(s, unicode):  
        return s.encode(encoding, errors)  
    elif s and encoding != 'utf-8':  
        return s.decode('utf-8', errors).encode(encoding, errors)  
    else:  
        return s 

"""
 * 除去数组中的空值和签名参数
 * @param  签名参数组
 * return 去掉空值与签名参数后的新签名参数组
"""
def params_filter(params):  
    ks = params.keys()  
    ks.sort()  
    newparams = {}  
    prestr = ''  
    for k in ks:  
        v = params[k]  
        k = smart_str(k)  
        if k not in ('sign','sign_type') and v != '':  
            newparams[k] = smart_str(v)  
            prestr += '%s=%s&' % (k, newparams[k])  
    prestr = prestr[:-1]  
    return newparams, prestr


"""
 * 除去数组中的空值和签名参数
 * @param  签名参数组
 * return 去掉空值与签名参数后的新签名参数组
"""
def params_filter_add(params):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k)
        if k and v != '':
            newparams[k] = smart_str(v)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr









"""
 * 把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
 * @param $para 需要拼接的数组
 * return 拼接完成以后的字符串
  函数没有用到，先放着
"""
def createLinkstring(values):
    res = ""
    for k,v in values.iteritems():
        res += k + "=" + v + "&"
    res = res[:-1]
    return res

"""
 * 把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串，并对字符串做urlencode编码
 * @param $para 需要拼接的数组
 * return 拼接完成以后的字符串
"""
def createLinkstringUrlencode(values):
    res = ""
    for k,v in values.iteritems():
        res += k+"="+urlencode(v)+"&"
    res = res[:-1]
    return res
