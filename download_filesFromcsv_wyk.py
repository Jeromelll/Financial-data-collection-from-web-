# -*- coding: utf-8 -*-
# description:下载csv中列出的pdf年报

'''
下载前要对csv文件做一些调整：
1.公告标题里的英文引号要去掉
2.下载地址里的www替换为static
'''


import csv
import os
import time
import requests

def download_pdf(path,MAX_COUNT = 5):
    LIST_FILE=path
    assert (os.path.exists(LIST_FILE)), 'No such list file \"' + LIST_FILE + '\"!'
    DST_DIR=os.path.dirname(LIST_FILE)
    assert (os.path.exists(DST_DIR)), 'No such destination directory \"' + DST_DIR + '\"!'
    if DST_DIR[len(DST_DIR) - 1] != '/':
        DST_DIR += '/'
    # 读取待下载文件列表
    with open(LIST_FILE, 'r') as csv_in:
        reader = csv.reader(csv_in)
        for each in enumerate(reader):
            download_count = 1
            download_token = False
            while download_count <= MAX_COUNT:
                try:
                    download_count += 1
                    r = requests.get(each[1][1])
                    download_token = True
                    break
                except:
                    # 下载失败则报错误
                    print(str(each[0] + 1) + '::' + str(download_count) + ':\"' + each[1][0] + '\" failed!')
                    download_token = False
                    time.sleep(3)
            if download_token:
                # 下载成功则保存
                with open(DST_DIR + each[1][0], 'wb') as file:
                    file.write(r.content)
                    print(str(each[0] + 1) + ': \"' + each[1][0] + '\" downloaded.')
            else:
                # 彻底下载失败则记录日志
                with open(DST_DIR + 'error.log', 'a') as log_file:
                    log_file.write(
                        time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())) + 'Failed to download\"' +
                        each[1][0] + '\"\n')
                    print('...' + str(each[0] + 1) + ':\"' + each[1][0] + '\" finally failed ...')




if __name__ == '__main__':
    LIST_FILE = r'D:\Documents\我的坚果云\PyLearn\A股负向舆情报告2020/工作簿1.csv'
    download_pdf(LIST_FILE)
