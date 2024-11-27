import json
import csv
# 打开JSON文件
with open('data.json',encoding='utf-8') as file:
    # 使用load函数将文件内容转换为字典
    data = json.load(file)


with open('data.csv', 'r',encoding='utf-8') as file:
    # 创建CSV读取器
    reader = csv.reader(file)
    # 遍历每一行
    for row in reader:
        # 打印每一行数据
        for i in data.keys():
            if row[2] in data[i]:
                row.append(i)
                break
        da = [
            row
        ]
        with open('data11.csv', 'a', newline='',encoding='utf-8') as file1:
            writer = csv.writer(file1)
            writer.writerows(da)