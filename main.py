import csv
import datetime
import sqlite3
import comm
import os.path

def get_file_route():
    options = ["speedtest自选", "speedtest默认", "CloudflareST"]
    print("请选择一个选项：")
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")
    choice = input("请输入选项号码：")
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        choice = int(choice)
        selected_option = options[choice - 1]
        print(f"您选择了选项 {choice}，即：{selected_option}")
        if choice == 1:
            return r'output\ip_filtered.csv', 'utf-8', True  # 返回默认文件路径、编码和端口标记
        elif choice == 2:
            return r'G:\v2\优选IP\ip.csv', 'gbk', True  # 返回用户选择的文件路径、编码和端口标记
        elif choice == 3:
            return r'G:\v2\0718workers部署裂变节点IP库\2\result.csv', 'utf-8', True  # 返回用户选择的文件路径、编码和端口标记
    else:
        print("无效的选项号码")

def insert_or_update_ip(cur, conn, ip_txt, mark_timestamp):
    cur.execute("SELECT ID FROM IP WHERE IP = ?", (ip_txt,))
    values = cur.fetchall()
    if len(values) == 0:
        lot = comm.get_location(ip_txt)
        print(ip_txt + "-" + lot['country'] + "-插入")  # 打印插入的IP和国家
        sql = ("INSERT INTO ip(lot_num, IP, country, regionName, creation_date, modification_date) VALUES (?, ?, ?, ?, ?, '')")
        cur.execute(sql, (mark_timestamp, ip_txt, lot['country'], lot['regionName'], datetime.datetime.now().date()))
    else:
        sql = "UPDATE IP SET modification_date = current_date WHERE IP = ?"
        cur.execute(sql, (ip_txt,))
        print(ip_txt + '-更新')  # 打印更新的IP

def generate_v_txt(v_Node, v_ip, v_today, v_notes, v_country):
    v_name = v_today + "-" + v_notes + "-" + v_country
    v_txt = v_Node.replace('{ip}', v_ip).replace('{name}', v_name)
    return v_txt

def main():
    route, coding, x_port = get_file_route()  # 获取文件路径、编码和端口标记
    mark_timestamp = int(os.path.getmtime(route))
    print(mark_timestamp)  # 打印文件的修改时间戳
    conn = sqlite3.connect('v2.s3db')  # 连接到SQLite数据库
    cur = conn.cursor()
    with open(route, 'r', encoding=coding) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row[0]) < 8:
                continue
            ip_txt = row[0]
            insert_or_update_ip(cur, conn, ip_txt, mark_timestamp)  # 插入或更新IP到数据库
    currently_all = conn.execute("SELECT IP, country FROM IP WHERE lot_num = ?", (mark_timestamp,))
    currently_ip = currently_all.fetchall()
    today_sql = conn.execute("SELECT * FROM Node")
    v_all = today_sql.fetchall()
    conn.commit()
    conn.close()
    for row_v in v_all:
        for ip in currently_ip:
            v_today = datetime.datetime.now().date().strftime("%m-%d")
            v_Node = row_v[1]
            v_notes = row_v[2]
            v_ip = ip[0] + ":2096"
            v_country = ip[1]
            v_txt = generate_v_txt(v_Node, v_ip, v_today, v_notes, v_country)
            print(v_txt)  # 打印生成的v_txt
            print(v_txt.replace(':2096', ':443'))
            print(v_txt.replace(':2096', ':8443'))
            print(v_txt.replace(':2096', ':2053'))
            print(v_txt.replace(':2096', ':2083'))
            print(v_txt.replace(':2096', ':2087'))

if __name__ == "__main__":
    main()