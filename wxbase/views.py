# coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from wxbase.config import *
from wechat_sdk import WechatBasic
from django.views.decorators.csrf import csrf_exempt


'''
def __init__(self, token=None, appid=None, appsecret=None, partnerid=None,
                 partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None,
                 jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False):
'''

wechat = WechatBasic(token=WEIXIN_TOKEN, appid=WEIXIN_APPID,
                     appsecret=WEIXIN_APPSECRET)


@csrf_exempt
def main(request):
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
    # 对签名进行校验, 微信服务器联通业务服务器
        if wechat.check_signature(signature=signature, timestamp=timestamp,
                                  nonce=nonce):
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin index")
    elif request.method == "POST":
        # 微信服务器发送过来的xml包体
        body_text = request.body
        # xml包体解析成dict,实例化Message类
        wechat.parse_data(body_text)
        message = wechat.get_message()
        response = None
        if message.type == 'text':
            if message.content == 'wechat':
                response = wechat.response_text(u'^_^')
            else:
                response = wechat.response_text(u'文字' + message.content)
        elif message.type == 'image':
            response = wechat.response_text(u'图片' + str(message.media_id))
        elif message.type == 'voice':
            response = wechat.response_text(u'语音' + str(message.media_id))
        elif message.type == 'shortvideo':
            response = wechat.response_text(u'小视频' + str(message.media_id))
        elif message.type == 'location':
            response = wechat.response_text(u'地理位置' + str(message.location))
        elif message.type == 'click':
            if message.key == 'V1001_CLICK':
                response = wechat.response_text(u'点击推送' + str(message.key) + u"\n欢迎来到全栈工程师项目")
            elif message.key == 'V1001_GOOD':
                response = wechat.response_text(u'点击推送' + str(message.key) + u"\n谢谢点赞")
        else:
            response = wechat.response_text(u'未知')
        return HttpResponse(response)


def create_menu(request):
    wechat.create_menu({
        'button': [
            {
                       'type': 'view',
                       'name': '我自己',
                       'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + WEIXIN_APPID + '&redirect_uri=' + CREATE_MENU_URL + '&response_    type=code&scope=snsapi_userinfo&state=snsapi_userinfo#wechat_redirect'
            },
            {
                'type': 'click',
                'name': '点击推送',
                'key': 'V1001_CLICK'
            },
            {
                'name': '菜单',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': '传智',
                        'url': 'http://www.itcast.cn/'
                    },
                    {
                        'type': 'view',
                        'name': 'C++学院',
                        'url': 'http://c.itcast.cn/'
                    },
                    {
                        'type': 'click',
                        'name': '赞下老邢',
                        'key': 'V1001_GOOD'
                    }
                ]
            }
        ]})
    return HttpResponse("ok")


def userinfo(request):
    code = request.GET.get('code', '')
    if code == '':
        return HttpResponse('你得先授权')
    state = request.GET.get('state', '')

    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + WEIXIN_APPID + \
        '&secret=' + WEIXIN_APPSECRET + '&code=' + \
        code + '&grant_type=authorization_code'
    content = wechat._get(url)
    dict_user = wechat._transcoding_dict(content)
    if state == 'snsapi_userinfo':
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + \
            dict_user['access_token'] + '&openid=' + \
            dict_user['openid'] + '&lang=zh_CN'
        content = wechat._get(url)
        dict_user2 = wechat._transcoding_dict(content)
        dict_user.update(dict_user2)
        print "*****************"
        print dict_user
        print "*****************"
        return render(request, 'user_info.html', dict_user)

    return HttpResponse('err: state')


def index(request):
    return HttpResponse("hello")
