import openpyxl

from youth_study import YouthStudyTianjin


def main():
    JSESSIONID = 'D7C616BB218F5A7C90AD7F667F1A8967'

    # 读取需要学习的人员名单
    code_dic = {
        'qipu': '1001016017022000',
    }
    wb = openpyxl.load_workbook('七堡村团员信息.xlsx')
    sheet = wb.active

    for num, _ in enumerate(sheet['A']):
        if num:
            code = code_dic[sheet[f'B{num + 1}'].value]
            name = sheet[f'C{num + 1}'].value
            tel = sheet[f'D{num + 1}'].value

            study = YouthStudyTianjin(JSESSIONID, name, tel, code)
            study.post_req()
            study.request_learn()


if __name__ == '__main__':
    main()
