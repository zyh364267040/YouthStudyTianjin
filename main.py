import openpyxl
import argparse

from youth_study import YouthStudyTianjin


# 引入参数
def get_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--cookie', type=str, required=True, help='cookie')

    return parse.parse_args()


def main():
    JSESSIONID = get_args().cookie

    # 读取需要学习的人员名单
    section_id_dic = {
        'qipu': '1001016017022000',
        'minzhu': '1001016017009000',
        'liupu': '1001016017024000'
    }
    wb = openpyxl.load_workbook('团员信息.xlsx')
    sheet = wb.active

    for num, _ in enumerate(sheet['A']):
        if num:
            section_id = section_id_dic[sheet[f'B{num + 1}'].value]
            name = sheet[f'C{num + 1}'].value
            tel = sheet[f'D{num + 1}'].value

            study = YouthStudyTianjin(JSESSIONID, name, tel, section_id)
            study.post_req()
            study.request_learn()


if __name__ == '__main__':
    main()
