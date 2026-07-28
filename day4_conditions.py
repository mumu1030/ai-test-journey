#if-elif-else ，练习针对不同优先级确定执行
priority = str(input("请输入优先级P0-P3:"))
if priority == "P0":
    print("执行操作1")
elif priority == "P1":
    print("执行操作2")
elif priority == "P2":
    print("执行操作3")
elif priority == "P3":
    print("执行操作4")
else:
    print("无效的优先级")
#for 循环，练习遍历用例列表，按照优先级筛选，统计测试通过率的脚本
test_cases = [
    {"id": "TC001", "title": "正常登录",   "priority": "P0", "status": "pass"},
    {"id": "TC002", "title": "密码错误",   "priority": "P1", "status": "fail"},
    {"id": "TC003", "title": "账号为空",   "priority": "P0", "status": "pass"},
    {"id": "TC004", "title": "记住密码",   "priority": "P2", "status": "skip"},
    {"id": "TC005", "title": "第三方登录", "priority": "P1", "status": "pass"},
]
print("\n"+"="*20)
print("遍历测试用例列表：")
print("="*20)

for case in test_cases:#用case["id"],case["title"],case["priority"],case["status"]来访问字典中的值
    print(f"{case['id']},{case['title']},{case['priority']}:{case['status']}")

print("="*20)
print("使用普通方法筛选P0优先级用例")
test_cases_P0 = [] #建个空列表装P0优先级的用例
for case in test_cases: #遍历
    if case["priority"] == "P0": #判断
        test_cases_P0.append(case) #收集
        print(f"{case['id']},{case['title']},{case['priority']}:{case['status']}")
print(f"PO用例:{len(test_cases_P0)}条")

print("="*20)
print("统计测试通过率") #只算pass和fail的用例，skip不算

pass_count = 0
fail_count = 0

for case in test_cases:
    if case["status"] == "pass":
        pass_count = pass_count + 1
    elif case["status"] == "fail":
        fail_count = fail_count + 1
print(f"测试通过率为：{pass_count/(pass_count+fail_count)*100:.2f}%")

#使用列表推导式，练习筛选并打印P0优先级的用例
print("="*20)
print("使用列表推导式筛选并打印P0优先级的用例")
test_cases_P0 = [case for case in test_cases if case["priority"] == "P0"]

for case in test_cases_P0:
    print(f"P0用例:{case['id']},{case['title']}")

#使用列表推导式，练习统计测试通过率
pass_count = len([case for case in test_cases if case["status"] == "pass"])
fail_count = len([case for case in test_cases if case["status"] == "fail"])
pass_rate = pass_count/(pass_count+fail_count)*100
print(f"列表推导式统计的通过率：{pass_rate:.1f}%")

#使用列表推导式，筛选pass的cases并打印
test_cases_pass = [case for case in test_cases if case["status"] == "pass"]
print("\n")
print("="*20)
print("通过的用例")
for case in test_cases_pass:
    print(f"{case['id']},{case['title']}")

print(f"PO用例:{len(test_cases_pass)}条")