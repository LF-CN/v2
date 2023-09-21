options = ["speedtest自选", "speedtest默认", "CloudflareST"]

# 显示选项列表
print("请选择一个选项：")
for index, option in enumerate(options, 1):
    print(f"{index}. {option}")

# 获取用户输入
choice = input("请输入选项号码：")

# 检查用户输入是否有效
if choice.isdigit() and 1 <= int(choice) <= len(options):
    choice = int(choice)
    selected_option = options[choice - 1]
    print(f"您选择了选项 {choice}，即：{selected_option}")

    # 根据选项执行相应的操作
    if choice == 1:
        # speedtest自选
        return r'G:/v2/优选IP/ip_filtered.csv', 'utf-8', True  # 返回默认文件路径、编码和端口标记
    elif choice == 2:
        # speedtest默认
    elif choice == 3:
        # CloudflareST
else:
    print("无效的选项号码")