import sqlite3
import datetime
from datetime import date
import pyperclip

def generate_v_txt(i_Node, i_ip, i_today, i_notes, i_country):
    v_name = f"{i_today}-{i_notes}-{i_country}"
    i_txt = i_Node.replace('{ip}', i_ip).replace('{name}', v_name)
    return i_txt

# 连接到数据库
with sqlite3.connect('v2.s3db') as conn:
    cursor = conn.cursor()

    # 获取今天的日期
    today = date.today()

    # 执行查询
    cursor.execute("SELECT IP, country FROM IP WHERE creation_date = ?", (today,))
    currently_ip = cursor.fetchall()

    cursor.execute("SELECT IP, country FROM IP WHERE modification_date = ?", (today,))
    currently_ip += cursor.fetchall()

    today_sql = conn.execute("SELECT * FROM Node")
    v_all = today_sql.fetchall()

    # 定义要写入的变量
    output = ""

    for row_v in v_all:
        for ip in currently_ip:
            v_today = datetime.datetime.now().date().strftime("%m-%d")
            v_Node = row_v[1]
            v_notes = row_v[2]
            v_ip = f"{ip[0]}:2096"
            v_country = ip[1]
            v_txt = generate_v_txt(v_Node, v_ip, v_today, v_notes, v_country)
            
            output += f"{v_txt}\n"
            output += f"{v_txt.replace(':2096', ':443')}\n"
            output += f"{v_txt.replace(':2096', ':8443')}\n"
            output += f"{v_txt.replace(':2096', ':2053')}\n"
            output += f"{v_txt.replace(':2096', ':2083')}\n"
            output += f"{v_txt.replace(':2096', ':2087')}\n"

    print(output)  # 打印生成的v_txt

    # 将结果写入剪贴板
    pyperclip.copy(output)