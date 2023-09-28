import subprocess
import os
import datetime
import time
import os
import shutil
import requests
import zipfile


# 下载压缩包并解压
url = "https://zip.baipiao.eu.org"
zip_file_path = "archive.zip"
extract_folder = "txt"


response = requests.get(url)
with open(zip_file_path, 'wb') as file:
    file.write(response.content)

print("文件下载完成！")

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# 合并txt文件
output_folder = "IP/IP库"
output_file = "baipiao-ip.txt"

with open(os.path.join(output_folder, output_file), 'w') as outfile:
    for foldername, _, filenames in os.walk(extract_folder):
        for filename in filenames:
            if filename.endswith('.txt'):
                filepath = os.path.join(foldername, filename)
                with open(filepath, 'r') as infile:
                    outfile.write(infile.read())

# 删除原始的txt文件夹
shutil.rmtree(extract_folder)

print("文件合并完成，并已保存到指定目录。")


# 在output文件夹下创建当前日期文件夹
# 获取当前日期
current_date = datetime.date.today()

# 格式化日期为字符串
date_string = current_date.strftime("%Y-%m-%d")

# 拼接文件夹路径
folder_path = os.path.join("IP", "output", date_string)

# 检查文件夹是否存在
if not os.path.exists(folder_path):
    # 创建文件夹
    os.makedirs(folder_path)
    print(f"文件夹'{folder_path}'已创建成功！")
else:
    print(f"文件夹'{folder_path}'已存在，无需创建。")




def run_cloudflarest(file_path, output_path):
    port = '2096'
    command = [
        r"G:\v2\0718workers部署裂变节点IP库\2\CloudflareST.exe",
        "-url", "https://cs.1312266.link/test",
        "-tp", port,
        "-t", "1",
        "-sl", "1",
        "-dn", "30",
        "-tl", "1000",
        "-f", file_path,
        "-o", output_path,
        "-p", "0",
    ]
    subprocess.run(command)
    print("测试完成！")


# 定义一个包含多个文件路径的数组
file_paths = ["IP/IP库/baipiao-ip.txt", "IP/IP库/ip.txt", "IP/IP库/ip2.txt", "IP/IP库/ip3.txt"]

# 遍历文件路径数组，并调用函数处理每个文件
for file_path in file_paths:
    output_path = f"{folder_path}/{int(time.time())}.csv"
    run_cloudflarest(file_path, output_path)


