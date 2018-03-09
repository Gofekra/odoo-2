/**
 * Created by zengfajun on 2018-1-3.
 */
odoo.define('field_verify.FieldVerify', function (require) {
    'use strict';

    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var basic_fields = require('web.basic_fields')
    var QWeb = core.qweb;
    var _lt = core._lt;
    var _t = core._t;

    var FieldVerify = basic_fields.FieldChar.extend({
        _onChange: function () {
            var self = this;
            var data = self._verify(this.$input[0].value);
            if (!data['is_pass']) {
                if (!self.$el[0].nextElementSibling) {
                    $("<span style='color: #FF0000;'>" + data['message'] + "</span>").insertAfter(this.$input[0]);
                }
                this.$input.attr("style", "border-color:red;border-bottom-width:unset");
                return false;
            }
            else {
                this.$input.removeAttr('style');
                if (self.$el[0].nextElementSibling) {
                    self.$el[0].nextElementSibling.remove();
                }
            }
            this._setValue(this.$input[0].value);
        },

        _verify: function (value) {
            var data = {
                'message': '',
                'is_pass': true
            };
            return data;
        },

        _setValue: function (value, options) {
            var data = this._verify(value);
            if (this.lastSetValue === value || (this.value === false && value === '' || !data['is_pass'])) {
                return $.when();
            }
            return this._super.apply(this, arguments)
        },

    });

    var FieldVerifyEmail = FieldVerify.extend({
        _verify: function (value) {
            var data = this._super.apply(this, arguments);
            //对电子邮件的验证
            var verify_e = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            if (!verify_e.test(value)) {
                data['message'] = '请输入有效的E_mail!';
                data['is_pass'] = false;
            }
            return data;
        }
    });
    field_registry.add("field_email", FieldVerifyEmail);

    var FieldVerifyIDCard = FieldVerify.extend({
        /*
         根据〖中华人民共和国国家标准 GB 11643-1999〗中有关公民身份号码的规定，公民身份号码是特征组合码，由十七位数字本体码和一位数字校验码组成。排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位数字校验码。
         地址码表示编码对象常住户口所在县(市、旗、区)的行政区划代码。
         出生日期码表示编码对象出生的年、月、日，其中年份用四位数字表示，年、月、日之间不用分隔符。
         顺序码表示同一地址码所标识的区域范围内，对同年、月、日出生的人员编定的顺序号。顺序码的奇数分给男性，偶数分给女性。
         校验码是根据前面十七位数字码，按照ISO 7064:1983.MOD 11-2校验码计算出来的检验码。

         出生日期计算方法。
         15位的身份证编码首先把出生年扩展为4位，简单的就是增加一个19或18,这样就包含了所有1800-1999年出生的人;
         2000年后出生的肯定都是18位的了没有这个烦恼，至于1800年前出生的,那啥那时应该还没身份证号这个东东，⊙﹏⊙b汗...
         下面是正则表达式:
         出生日期1800-2099  (18|19|20)?\d{2}(0[1-9]|1[12])(0[1-9]|[12]\d|3[01])
         身份证正则表达式 /^\d{6}(18|19|20)?\d{2}(0[1-9]|1[12])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)$/i
         15位校验规则 6位地址编码+6位出生日期+3位顺序号
         18位校验规则 6位地址编码+8位出生日期+3位顺序号+1位校验位

         校验位规则     公式:∑(ai×Wi)(mod 11)……………………………………(1)
         公式(1)中：
         i----表示号码字符从由至左包括校验码在内的位置序号；
         ai----表示第i位置上的号码字符值；
         Wi----示第i位置上的加权因子，其数值依据公式Wi=2^(n-1）(mod 11)计算得出。
         i 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1
         Wi 7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 1
         */
        _verify: function (value) {
            var data = this._super.apply(this, arguments);
            var city_code = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古",
                21: "辽宁", 22: "吉林", 23: "黑龙江", 31: "上海", 32: "江苏",
                33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东",
                41: "河南", 42: "湖北", 43: "湖南", 44: "广东", 45: "广西",
                46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南",
                54: "西藏 ", 61: "陕西", 62: "甘肃", 63: "青海", 64: "宁夏",
                65: "新疆", 71: "台湾", 81: "香港", 82: "澳门", 91: "国外 "};
            var data = {
                "message": "",
                "is_pass": true
            };

            if (!value || (value.length != 15 && value.length != 18) || !/^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X|x)?$/i.test(value)) {
                data['message'] = "身份证号格式错误!";
                data['is_pass'] = false;
            }
            else if (!city_code[value.substr(0, 2)]) {
                data['message'] = "地址编码错误(身份证起始两位)!";
                data['is_pass'] = false;
            }
            else {
                //18位身份证需要验证最后一位校验位
                if (value.length == 18) {
                    value = value.split('');
                    //∑(ai×Wi)(mod 11)
                    //加权因子
                    var factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
                    //校验位
                    var parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2];
                    var sum = 0;
                    var ai = 0;
                    var wi = 0;
                    for (var i = 0; i < 17; i++) {
                        ai = value[i];
                        wi = factor[i];
                        sum += ai * wi;
                    }
                    var last = parity[sum % 11];
                    if (last != value[17]) {
                        data['message'] = "校验位错误(身份证最后一位)!";
                        data['is_pass'] = false;
                    }
                }
            }

            return data;
        }
    });
    field_registry.add("field_ID_card", FieldVerifyIDCard);

    var FieldVerifyPhone = FieldVerify.extend({
        _verify: function (value) {
            var data = this._super.apply(this, arguments);
            var verify_p = /^1[3|4|5|7|8|9]\d{9}$/;
            if (!verify_p.test(value)) {
                data['message'] = '请输入有效的手机号码!';
                data['is_pass'] = false;
            }
            return data;
        }
    });
    field_registry.add("field_phone", FieldVerifyPhone);
    return FieldVerify
});
