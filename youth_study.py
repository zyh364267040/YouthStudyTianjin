import requests
import ddddocr


class YouthStudyTianjin:

    def __init__(self, JSESSIONID, name, tel, section_id):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.7.1(0x13070114) XWEB/30419 Flue',
            'Cookie': f'HWWAFSESID=ae5d573f418e8e1d1d; HWWAFSESTIME=1682684736743; JSESSIONID={JSESSIONID}',
        }

        self.name = name
        self.tel = tel
        self.section_id = section_id

    # 获取已经学习完的人员姓名
    def get_learned_name(self):
        return requests.get(
            'http://admin.ddy.tjyun.com/zm/rank',
            headers=self.headers)

    # 发送更改信息请求,获取验证码图片
    def get_code(self):
        requests.get('http://admin.ddy.tjyun.com/zm/info', headers=self.headers)
        res = requests.get('http://admin.ddy.tjyun.com/entry/identifyingCode', headers=self.headers)

        return ddddocr.DdddOcr(show_ad=False).classification(res.content)

    # 绑定信息
    def post_req(self):
        print(f'开始学习{self.name}...')
        if self.name in self.get_learned_name().text:
            print(f'{self.name}已经学习完成...')
            return True

        data = {
            'deptId': self.section_id,
            'qingnianType': '1',
            'truename': self.name,
            'sex': '1',
            'tel': self.tel,
            'imageCode': self.get_code(),
        }
        requests.post('http://admin.ddy.tjyun.com/zm/infosub', data=data, headers=self.headers)

    # 发送学习请求,达到学习的目的
    def request_learn(self):
        requests.get('http://admin.ddy.tjyun.com/zm/jump/1', headers=self.headers, verify=False)
