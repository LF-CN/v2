import csv
import subprocess
import re

port = '2096'
command = [
    r"G:\v2\0718workers部署裂变节点IP库\2\CloudflareST.exe",
    "-url", "https://cs.1312266.link/test",
    "-tp", port,
    "-sl", "1",
    "-tl", "1000",
    "-f", "IP/ip.txt",
    "-o", "IP/result.csv",
    "-p", "0",
    "-dd", "1"
]
subprocess.run(command)

coding = 'utf-8'
route = r'IP/result.csv'
output_file_ip = 'output/ip.txt'

with open(route, 'r', encoding=coding) as csv_file:
    reader = csv.reader(csv_file)
    data = list(reader)

first_column = [row[0] for row in data[1:2000]]

with open(output_file_ip, 'w', encoding='utf-8') as file:
    for ip in first_column:
        file.write(ip + '\n')

print("")
print(f"数据已成功写入到 {output_file_ip} 文件中。")

# 输出文件处理
input_file = r'output\ip.csv'
output_file_speed = r'output\ip_filtered.csv'
command = [
    r"G:\py\v2ray\output\iptest.exe",
    "-port", "2096",
    "-file", r"output\ip.txt",
    "-outfile", input_file,
]
subprocess.run(command)
print(f"IP数据测试完成")


with open(input_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]  # 获取标题行
filtered_data = [row for index, row in enumerate(data) if index != 0 and row[7] and int(re.sub(r'\D', '', row[7])) >= 1500]

with open(output_file_speed, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # 写入标题行
    writer.writerows(filtered_data)

print(f"已成功删除数值小于1500的行，并将结果保存到 {output_file_speed} 文件中。")
