# -*- coding: utf-8 -*-
"""
cron: 30 8 * * *
new Env('什么值得买');
"""
import requests
from requests import utils
import os

class Smzdm(object):
    def __init__(self, cookie):
        self.cookie = cookie

    @staticmethod
    def sign(session):
        """
        执行什么值得买的签到操作
        :param session: requests.Session 对象，包含用户的 cookie 信息
        :return: 签到结果信息列表
        """
        try:
            # 获取用户当前信息
            current = session.get(url="https://zhiyou.smzdm.com/user/info/jsonp_get_current").json()
            if current["checkin"]["has_checkin"]:
                # 已经签到的情况，返回用户信息
                msg = [
                    {"name": "账号信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "碎银子数", "value": current.get("silver", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("level", "")},
                    {"name": "已经签到", "value": f"{current.get('checkin', {}).get('daily_checkin_num', '')} 天"},
                ]
            else:
                # 未签到，执行签到操作
                response = session.get(url="https://zhiyou.smzdm.com/user/checkin/jsonp_checkin").json().get("data", {})
                msg = [
                    {"name": "账号信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "增加积分", "value": current.get("add_point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("rank", "")},
                    {"name": "已经签到", "value": f"{response.get('checkin_num', {})} 天"},
                ]
        except Exception as e:
            # 签到失败，返回错误信息
            msg = [
                {"name": "签到信息", "value": "签到失败"},
                {"name": "错误信息", "value": str(e)},
            ]
        return msg

    def main(self):
        """
        主函数，处理 cookie 并执行签到操作
        :return: 签到结果信息字符串
        """
        # 将 cookie 字符串转换为字典
        smzdm_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")}
        session = requests.session()
        # 将 cookie 字典添加到 session 的 cookies 中
        requests.utils.add_dict_to_cookiejar(session.cookies, smzdm_cookie)
        # 设置请求头
        session.headers.update(
            {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": "zhiyou.smzdm.com",
                "Referer": "https://www.smzdm.com/",
                "Sec-Fetch-Dest": "script",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            }
        )
        # 执行签到操作
        msg = self.sign(session=session)
        # 将签到结果信息列表转换为字符串
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg

def main(*args, **kwargs):
    """
    入口函数，从环境变量中获取 cookie 并执行签到操作
    :param args: 位置参数
    :param kwargs: 关键字参数
    :return: 签到结果信息字符串
    """
    # 从环境变量中获取 cookie
    cookie = os.getenv("SMZDM_COOKIE")
    if not cookie:
        return "未设置什么值得买的 cookie，请在青龙面板添加环境变量 SMZDM_COOKIE"
    smzdm = Smzdm(cookie=cookie)
    return smzdm.main()

if __name__ == "__main__":
    result = main()
    print(result)
