import time
import requests
import ddddocr
import socket
import openpyxl


def get_learned_name(JSESSIONID):
    url = 'http://admin.ddy.tjyun.com/zm/rank'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.7.1(0x13070114) XWEB/30419 Flue',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://admin.ddy.tjyun.com/zm/youth',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Cookie': f'HWWAFSESID=ae5d573f418e8e1d1d; HWWAFSESTIME=1682684736743; JSESSIONID={JSESSIONID}',
        'Connection': 'keep-alive'
    }
    return requests.get(url, headers=headers)


def load_info(index):
    wb = openpyxl.load_workbook('七堡村团员信息.xlsx')
    sheet = wb.active
    name = sheet[f'A{index}'].value
    phone_num = sheet[f'C{index}'].value

    return name, phone_num


def ddddocr_code():
    ocr = ddddocr.DdddOcr()

    with open("../../Python/code/YouthStudyTianjin/code.png", 'rb') as f:
        image = f.read()

    return ocr.classification(image)


def get_code(JSESSIONID):
    url1 = 'http://admin.ddy.tjyun.com/zm/info'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.7.1(0x13070114) XWEB/30419 Flue',
        'Referer': 'http://admin.ddy.tjyun.com/zm/study',
        'Cookie': f'HWWAFSESID=ae5d573f418e8e1d1d; HWWAFSESTIME=1682684736743; JSESSIONID={JSESSIONID}',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
    }
    requests.get(url1, headers=headers)

    url2 = 'http://admin.ddy.tjyun.com/entry/identifyingCode'
    resp = requests.get(url2, headers=headers)
    with open('../../Python/code/YouthStudyTianjin/code.png', 'wb') as f:
        f.write(resp.content)


def post_req(code_num, JSESSIONID, i, resp):
    name, phone_num = load_info(i)
    if name in resp.text:
        print(f'{name}已经学习...')
        return True

    print(f'开始学习{name}...')
    url = 'http://admin.ddy.tjyun.com/zm/infosub'
    data = {
        'deptId': '1001016017022000',
        'qingnianType': '1',
        'truename': name,
        'sex': '1',
        'tel': phone_num,
        'imageCode': code_num,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.7.1(0x13070114) XWEB/30419 Flue',
        'Referer': 'http://admin.ddy.tjyun.com/zm/info',
        'Cookie': f'HWWAFSESID=ae5d573f418e8e1d1d; HWWAFSESTIME=1682684736743; JSESSIONID={JSESSIONID}',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Origin': 'http://admin.ddy.tjyun.com',
    }
    resp = requests.post(url, data=data, headers=headers)
    print(resp.text)


def visit(req):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('admin.ddy.tjyun.com', 80))

    conn.send(req)
    r = conn.recv(400)
    print(r)
    if b'HTTP/1.1 302' not in r:
        if b'HTTP/1.1 403' in r:
            print(403)
        elif b'HTTP/1.1 502' in r:
            print(502)
    if b'JSESSIONID' in r:
        print('cookie过期')

    conn.close()
    print('完成学习!')


if __name__ == '__main__':
    JSESSIONID = '81ACF01D1835E820909E7C37EAD011E8'
    req_content = bytes(
        f'GET /zm/jump/1 HTTP/1.1\r\nHost: admin.ddy.tjyun.com\r\nCookie: JSESSIONID={JSESSIONID}\r\n\r\n',
        encoding='utf-8')
    resp = get_learned_name(JSESSIONID)

    for i in range(1, 36):
        print(f'开始第{i}个')
        get_code(JSESSIONID)
        code_num = ddddocr_code()
        flag = post_req(code_num, JSESSIONID, i, resp)
        if flag:
            continue
        visit(req_content)
        time.sleep(5)
