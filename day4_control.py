#从零写一个"测试执行报告生成器"
#构造测试用例用例
test_cases = [
    {"id": "TC001","title": "用账号密码登录","priority": "P0","result": "pass"},
    {"id": "TC002","title": "用验证码登录",  "priority": "P0","result": "fail"},
    {"id": "TC003","title": "用微信登录","priority": "P1","result": "fail"},
    {"id": "TC004","title": "用微博登录","priority": "P2","result": "pass"},
    {"id": "TC005","title": "用小红书登录","priority": "P0","result": "fail"},
    {"id": "TC006","title": "用邮箱登录","priority": "P1","result": "pass"},
    {"id": "TC007","title": "用扫脸登录",  "priority": "P3","result": "fail"},
    {"id": "TC008","title": "用苹果登录","priority": "P1","result": "skip"},
    {"id": "TC009","title": "用搜狐登录","priority": "P2","result": "pass"},
    {"id": "TC010","title": "用拼多多登录","priority": "P3","result": "fail"},
]
print("=" * 5 + "测试执行报告" + "=" * 5)
total_cases = [case for case in test_cases] #遍历用例
pass_cases = [case for case in test_cases if case['result']=="pass"] #遍历判断pass用例
fail_cases = [case for case in test_cases if case['result']=="fail"] #遍历判断fail用例
skip_cases = [case for case in test_cases if case['result']=="skip"] #遍历判断skip用例
fail_cases_P0 = [case for case in fail_cases if case['priority']=="P0"] #遍历 判断fail且为p0 用例
fail_cases_P1 = [case for case in fail_cases if case['priority']=="P1"] #遍历 判断fail且为p1 用例

print(f"总用例条数：{len(total_cases)}条")
print(f"通过：{len(pass_cases)}条,失败:{len(fail_cases)}条,跳过:{len(skip_cases)}条")
print("\n"+"P0失败用例(需立即关注):")
for case in fail_cases_P0: #遍历打印fail且为p0 用例
    print(f"{case['id']},{case['title']}")

print("\n"+"P1失败用例:")
for case in fail_cases_P1:#遍历打印fail且为p1 用例
    print(f"{case['id']},{case['title']}")
    
