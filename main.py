import csv
import datetime
import sqlite3
import comm
import os.path

def insert_or_update_ip(cur, ip_txt, mark_timestamp):
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
    current_date = datetime.date.today() # 获取当前日期
    date_string = current_date.strftime("%Y-%m-%d") # 格式化日期为字符串
    folder_path = os.path.join("IP", "output", date_string,"today-ip.csv") # 拼接文件夹路径
    print(folder_path)
    route = folder_path
    mark_timestamp = int(os.path.getmtime(route))
    print(mark_timestamp)  # 打印文件的修改时间戳
    conn = sqlite3.connect('v2.s3db')  # 连接到SQLite数据库
    cur = conn.cursor()
    with open(route, 'r', encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row[0]) < 8:
                continue
            ip_txt = row[0]
            insert_or_update_ip(cur, ip_txt, mark_timestamp)  # 插入或更新IP到数据库
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