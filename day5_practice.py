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

#功能：传入用例列表，测试用例总数，按照结果筛选通过条数，失败条数，跳过条数计算通过率

def filter_cases(cases,result=None): 
    """构建用例筛选函数，在用例里按照结果筛选指定结果的用例"""
    if result:
        return[c for c in cases if c["result"]==result]
    return cases #不传result,返回全部用例

total_cases = filter_cases(test_cases)
pass_cases = filter_cases(test_cases,"pass")
fail_cases = filter_cases(test_cases,"fail")
skip_cases = filter_cases(test_cases,"skip")

print("执行情况如下:")
print(f"总用例条数:{len(total_cases)}条")
print(f"通过:{len(pass_cases)}条,失败:{len(fail_cases)}条,跳过:{len(skip_cases)}条")

def pass_rate(pass_list,fail_list,precision=1):
    """计算测试通过率"""
    total = len(pass_list) + len(fail_list) + len(skip_cases)
    if total == 0:
       return 0
    rate = len(pass_list)/total * 100
    return round(rate, precision)
rate = pass_rate(pass_cases,fail_cases)
print(f"通过率:{rate}%")




print("\n"+"第二种方法:")
def analyze_test_result(cases):
    total = len(cases) #算列表总数
    pass_cases = sum(1 for c in cases if c["result"] == "pass") #算成功，遍历每条用例，符合条件就计数1
    fail_cases = sum(1 for c in cases if c["result"] == "fail") #算失败
    rate = pass_cases/total if total >0 else 0 #算通过率，三元表达式
    return total, pass_cases,fail_cases,skip_cases,rate #返回4个值

case = [{"result":"pass"},{"result":"fail"}] 
total, pass_cases,fail_cases,skip_cases,rate = analyze_test_result(test_cases) #调用函数，返回的元组自动解包到4个变量
print(f"总用例条数:{total},通过:{pass_cases},失败:{fail_cases},通过率:{rate:.1%}")
