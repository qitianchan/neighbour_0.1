# -*- coding: utf-8 -*-
__author__ = 'Chan'

from wechat_sdk import WechatBasic
from wechat_sdk.lib import disable_urllib3_warning
import redis
import time
from urllib import quote

class WechatBasicCache(WechatBasic):
    """
    使用redis缓存缓存auth_token和jsticket_token
    """
    def __init__(self, token=None, appid=None, appsecret=None,partnerid=None,
                 partnerkey=None, paysignkey=None, checkssl=None, redishost='localhost', redisport=6379, redispasswd=None):

        """
        :param token: 微信 Token
        :param appid: App ID
        :param appsecret: App Secret
        :param partnerid: 财付通商户身份标识, 支付权限专用
        :param partnerkey: 财付通商户权限密钥 Key, 支付权限专用
        :param paysignkey: 商户签名密钥 Key, 支付权限专用
        :param checkssl: 是否检查 SSL, 默认为 False, 可避免 urllib3 的 InsecurePlatformWarning 警告
        :param redishost:redis主机地址
        :param redisport:redis端口
        :param redispasswd:redis访问密码
        """
        if not checkssl:
            disable_urllib3_warning()  # 可解决 InsecurePlatformWarning 警告

        self.__token = token
        self.__appid = appid
        self.__appsecret = appsecret
        self.__partnerid = partnerid
        self.__partnerkey = partnerkey
        self.__paysignkey = paysignkey
        self.__redishost = redishost
        self.__redisport = redisport
        self.__redispasswd = redispasswd

        #网页授权票据的参数
        self.__wechat_host = 'https://open.weixin.qq.com'
        self.__code_method = '/connect/oauth2/authorize?'
        self.__access_token_method = '/sns/oauth2/access_token?'


        r = redis.Redis(host=redishost,port=redisport, db=0, password=redispasswd)

        access_token_key = appid + '_access_token'
        access_token = r.get(access_token_key)
        access_token_expires_at_key = appid + '_access_token_expires_at'
        access_token_expires_at = r.get(access_token_expires_at_key)
        jsapi_ticket_key = appid + '_jsapi_ticket'
        jsapi_ticket = r.get(jsapi_ticket_key)
        jsapi_ticket_expires_at_key = appid + '_jsapi_ticket_expires_at'
        jsapi_ticket_expires_at = r.get(jsapi_ticket_expires_at_key)
        if access_token_expires_at == None:
            access_token_expires_at = 0
        if jsapi_ticket_expires_at == None:
            jsapi_ticket_expires_at = 0

        self.__access_token = access_token
        self.__access_token_expires_at = int(access_token_expires_at)
        self.__jsapi_ticket = jsapi_ticket
        self.__jsapi_ticket_expires_at = int(jsapi_ticket_expires_at)
        self.__is_parse = False
        self.__message = None

        super(WechatBasicCache, self).__init__(token=token, appid=appid, appsecret=appsecret, partnerid=partnerid,
                 partnerkey=partnerkey, paysignkey=paysignkey, access_token=access_token, access_token_expires_at=self.__access_token_expires_at,
                 jsapi_ticket=jsapi_ticket, jsapi_ticket_expires_at=self.__jsapi_ticket_expires_at, checkssl=checkssl)


    def grant_token(self, override=True):
        """
        获取 Access Token
        详情请参考 http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        :param override: 是否在获取的同时覆盖已有 access_token (默认为True)
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        response_json = super(WechatBasicCache, self).grant_token()
        r = redis.Redis(host=self.__redishost, port=self.__redisport, db=0, password=self.__redispasswd)
        access_token = response_json['access_token']
        expires_time = int(time.time()) + response_json['expires_in'] - 8
        access_token_key = self.__appid + '_access_token'
        expires_time_key = self.__appid + '_access_token_expires_at'
        r.set(access_token_key, access_token)
        r.set(expires_time_key, expires_time)
        r.save()
        return response_json


    def grant_jsapi_ticket(self, override=True):
        """
        获取 Jsapi Ticket
        详情请参考 http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html#.E9.99.84.E5.BD.951-JS-SDK.E4.BD.BF.E7.94.A8.E6.9D.83.E9.99.90.E7.AD.BE.E5.90.8D.E7.AE.97.E6.B3.95
        :param override: 是否在获取的同时覆盖已有 jsapi_ticket (默认为True)
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        response_json = super(WechatBasicCache, self).grant_jsapi_ticket()
        r = redis.Redis(host=self.__redishost, port=self.__redisport, db=0, password=self.__redispasswd)
        ticket = response_json['ticket']
        expires_time = int(time.time()) + response_json['expires_in'] - 8
        ticket_key = self.__appid + '_jsapi_ticket'
        expires_time_key = self.__appid + '_jsapi_ticket_expires_at'
        r.set(ticket_key, ticket)
        r.set(expires_time_key, expires_time)
        r.save()
        return response_json

    def reset(self):
        """
        如果redis的access_token或者jsapi_ticket被别人重置过导致redis的数据过期的话，可以使用这个函数重置
        """
        self.grant_token()
        self.grant_jsapi_ticket()

    def _get_code(self, redirect_uri='' ,scope='snsapi_base', state=1):
        """
            获取网页收取的票据
        """
        #https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
        data = {
            'appid' : self.__appid,
            'redirect_uri' : quote(redirect_uri),
            'response_type' : 'code',
            'scope' : scope,
            'state' : state
        }
        keys = data.keys()
        keys.sort()
        params = '&'.join(['%s=%s' % (key, data[key]) for key in keys])
        url = self.__wechat_host + self.__code_method + params + '#wechat_redirect'
        return url




if __name__ == "__main__":
    w = WechatBasicCache(appid='wx86b3751ad43f4062', appsecret='f52a587fefed285df9244f310eee8a34')
    print w._get_code(scope='snsapi_userinfo', redirect_uri='http://subcribe.ecare-easy.com/Service/wechat/home_page')
    pass

