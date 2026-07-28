#练习 1：统计测试数据中的字段.给你一段接口返回的测试结果，任务：统计共有多少条测试记录,列出唯一的测试状态有哪些统计每种状态的用例数量
#共 7 条测试记录；状态类型：pass, fail, skip, error。pass: 3条, fail: 2条, skip: 1条, error: 1条
results = [
    {"case_id": "TC001", "status": "pass", "duration": 1.2},
    {"case_id": "TC002", "status": "fail", "duration": 3.5},
    {"case_id": "TC003", "status": "pass", "duration": 0.8},
    {"case_id": "TC004", "status": "skip", "duration": 0},
    {"case_id": "TC005", "status": "fail", "duration": 2.1},
    {"case_id": "TC006", "status": "pass", "duration": 1.5},
    {"case_id": "TC007", "status": "error", "duration": 0.3},
]
def analyze_test_result(cases):
    total = len(cases) #算总用例
    pass_cases = sum(1 for c in cases if c["status"]=="pass") #算成功条数
    fail_cases = sum(1 for c in cases if c["status"]=="fail") #算失败条数
    skip_cases = sum(1 for c in cases if c["status"]=="skip") #算skip条数
    error_cases = sum(1 for c in cases if c["status"]=="error") #算error条数
    return total,pass_cases,fail_cases,skip_cases,error_cases

total,pass_cases,fail_cases,skip_cases,error_cases = analyze_test_result(results)

print(f"共{total}条测试记录") #使用len()
print(f"测试结果:pass:{pass_cases}条,fail:{fail_cases}条,skip:{skip_cases}条,error:{error_cases}条")

#统计状态类型，用三种方法：
test_status = [] #建空列表来存状态
for case in results:
    if case["status"] not in test_status: #如果状态没出现过
        test_status.append(case["status"]) #加入这个状态
print("状态类型:" + ",".join(test_status))

test_status = [case["status"] for case in results] #列表推导式，不去重
print("状态类型不去重-列表推导式:" + ",".join(test_status))

test_status = {case["status"] for case in results} #集合推导式，会去重
print("状态类型-集合推导式:" + ",".join(test_status))


#练习2平均耗时计算
#定义函数，传用例，筛选不通结果的用例
def calc_avg_duration(cases,status=None):
    if status:
        filter_cases = [c for c in cases if c["status"]==status] #筛选状态cases列表
    else:
        filter_cases = cases #不传status,返回全部 不筛选
    if len(filter_cases)==0: #符合条件的用例数为0，直接返回0
        return 0

    total = len(filter_cases) #统计条数
    total_duration = sum(c["duration"] for c in filter_cases) #把所有duration加起来）
    avg = total_duration/total
    return round(avg,2)
    
#调用函数
print(calc_avg_duration(results))
print(calc_avg_duration(results,"pass"))
print(calc_avg_duration(results,"fail"))

#练习3:根据测试结果筛选用例按优先级 P0 > P1 > P2 > P3 排序后输出
def get_cases_by_status(cases, status):
    """提取指定测试结果的用例ID"""
    filter_cases = [c for c in cases if c["status"]==status]   #筛选相同status的用例
    ids = [c["case_id"] for c in filter_cases] #在筛选出来的用例里，把case ID的值，存到ids列表里 ,['TC001', 'TC003', 'TC006']
    result = ", ".join(ids)
    print(f"{status}: {result}")

for s in ["pass","fail","skip","error"]:
    get_cases_by_status(results,s)

#练习4:测试报告格式化
#写一个函数 generate_report(title, **stats)，接收报告标题和任意数量的统计数据（关键字参数），输出格式化的报告

#得先字典把stats的放进去
stats = {"总计":50,"通过":38,"失败":10,"跳过":2,"通过率":"76.0%"}

print(stats)
for k, v in stats.items():
    print(k, v)


def generate_report(title, stats): 
    """生成格式化测试报告"""
    lines = [f"======{title}======"] #把标题做成一个普通字符串，通过f-string取指后放在line列表
    for k , v in stats.items(): #使用.item()把字典拆成键值对,for k, v in ...同时取键、值
        lines.append(f"{k}:{v}") #遍历stats字典，每项一行 继续往lines里加 
    lines.append("=" * 30) #最后加尾部等号线
    return "\n".join(lines) #把列表里的每个元素用换行符\n连起来，变成一段完整文本

#调用
print(generate_report("登录测试报告",stats))

#lines 是一个「清单」，先把标题放进去，再逐行加统计，最后加尾线，全部攒齐后用换行符粘成一段话。样写的好处是：不用写很多个 print，攒齐后一次性返回。

#练习6 用例冲突检测，给定两份用例列表，找出 ID 相同的冲突用例（交集）。
cases = [
    {"case_id": "TC001", "status": "pass"},
    {"case_id": "TC002", "status": "fail"},
    {"case_id": "TC003", "status": "pass"},
    {"case_id": "TC001", "status": "fail"},   # TC001又出现，但结果不同 → 冲突
    {"case_id": "TC004", "status": "skip"},
    {"case_id": "TC002", "status": "pass"},   # TC002又出现，结果不相同 → 冲突
    {"case_id": "TC005", "status": "pass"},
]

seen = {} #建空字典,存见过的用例
conflicts = []
for case in cases: #遍历列表
    case_id = case["case_id"]
    status = case["status"]
    if case_id not in seen: #判断case_id 这个键不在seen这个字典里
        seen[case_id] = status #往字典里存一条，key是case_id,value是status
    else:
        if status != seen[case_id]:
            conflicts.append(f"{case_id}:({seen[case_id]}->{status})")

for t in conflicts:
    print(t)
        