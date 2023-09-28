import datetime
import os
import pandas as pd
import glob

# 计算日期文件夹路径
current_date = datetime.date.today() # 获取当前日期
date_string = current_date.strftime("%Y-%m-%d") # 格式化日期为字符串
folder_path = os.path.join("IP", "output", date_string) # 拼接文件夹路径


# 获取文件夹中所有CSV文件的路径
csv_files = glob.glob(folder_path + '/*.csv')

# 创建一个空列表来存储所有数据
data = []

# 遍历每个CSV文件并获取除表头的第一列数据
for file in csv_files:
    df = pd.read_csv(file, header=1)  # 指定表头所在的行数
    first_column = df.iloc[:, 0]  # 获取第一列数据
    data.extend(first_column.tolist())

# 将数据写入文件
output_file = folder_path + '/today-ip.csv'
df_output = pd.DataFrame({'IP': data})  # 创建包含 'IP' 列的 DataFrame
df_output.to_csv(output_file, index=False)
print("完成！")