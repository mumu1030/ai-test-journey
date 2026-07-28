#编写函数：filter_cases_by_priority(cases.priority);输入用例表+优先级，输出筛选后的用例表
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

def filter_cases_by_priority(cases,priority=None):
     """筛选指定优先级的用例"""
     if priority:
          return[c for c in cases if c["priority"]==priority]
     return cases #不传priority,返回全部

P3_filter_cases = filter_cases_by_priority(test_cases,"P3")
print(P3_filter_cases)

#函数2：generate_report_summary(cases)
#输入：执行完的用例列表（含status字段）
#输出：dict，包含 total/pass/fail/skipp/pass_rate

def generate_report_summary(cases):
    total = len(cases) #算总用例
    pass_cases = sum(1 for c in cases if c["result"]=="pass")#算成功用例
    fail_cases = sum(1 for c in cases if c["result"]=="fail")#算失败用例
    skip_cases = sum(1 for c in cases if c["result"]=="skip")#算跳过用例
    rate = pass_cases/total if total>0 else 0 #算通过率，三元表达式
    return total, pass_cases,fail_cases,skip_cases,rate #返回4个值

total, pass_cases,fail_cases,skip_cases,rate = generate_report_summary(test_cases) #调用函数，返回的元组自动解包到4个变量
print(f"总用例条数:{total},通过:{pass_cases},失败:{fail_cases},跳过:{skip_cases}通过率:{rate:.1%}")

# 函数3：format_case_as_markdown(case)
# # 输入：单条用例dict
# # 示例输出：
# # ## TC001: 正常账号密码登录
# # **优先级：** P0
# # **前置条件：** 用户已注册
# # **步骤：** 1. 打开App 2. 输入账号 3. 输入密码 4. 点击登录
# # **预期结果：** 成功登录，跳转首页

test_cases2 = [
    {"id": "TC001","title": "用账号密码登录","priority": "P0","result": "pass"}]

def format_case_as_markdown(cases):
    case = cases[0] #取列表的第一条
    return(
         f"用例如下：\n"
         f"id:{case["id"]}\n"
         f"title:{case["title"]}\n"
         f"priority:{case["priority"]}\n"
         f"result:{case["result"]}\n"
    )
test_cases3 = format_case_as_markdown(test_cases2)
print(test_cases3)
