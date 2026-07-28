#把python字典写入JSON文件
import json, os #导入两个内置模块，json处理json文件，os处理文件目录操作
test_suite={
    "suite_name":"用户登录模块测试集",
    "version":"v1.0",
    "cases":[
        {"id":"TC001","title":"正常账号密码登录","priority":"p0","steps":["打开app", "输入正常账号", "输入正确密码","点击登录"],"expected":"成功登录，跳转首页，显示用户昵称"},
        {"id":"TC002","title":"密码输入错误","priority": "P1","steps": ["打开App", "输入正确账号", "输入错误密码", "点击登录"],"expected": "提示'密码错误'，页面不跳转，密码框清空"}
    ]#一条用例一个字典
}
os.makedirs("data",exist_ok=True) #创建data文件夹，如果存在不报错，直接跳过
with open("data/test_suite_login.json","w",encoding="utf-8") as f: #打开 data/test_suite_login.json 文件，往里写东西，编码用 utf-8，文件小名叫 f。块里的代码执行完，自动关掉
    json.dump(test_suite,f,ensure_ascii=False, indent=2) #把 test_suite ，倒进文件 f 里，中文直接写不用转码，每层缩进2格方便阅读
print("写入成功:data/test_suite_login.json")

#从文件夹里读JSON文件到python
with open("data/test_suite_login.json","r",encoding="utf-8") as f: #打开data/test_suite_login.json 文件，读里面内容，编码用 utf-8，文件小名叫 f。块里的代码执行完，自动关闭
    loaded = json.load(f) #从f文件读取JSON,转成python对象 
print(f"套件名称:{loaded["suite_name"]}") # loaded["suite_name"]取字典里suite_name的值
print(f"用例数量：{len(loaded["cases"])}")
for case in loaded["cases"]:
    print(f"{case["priority"]}-{case["id"]}:{case["title"]}")

#把读写json文件封装成工具函数，
def save_json(data:dict|list,filepath:str) -> str: #data:dict-要保存的数据类型是dict里别表,filepath:str-文件路径字符串，-> str — 返回文件路径
    """保存数据到JSON文件,自动创建目录"""
    os.makedirs(os.path.dirname(filepath) or ".",exist_ok=True) #从完整路径里提取目录部分，如果目录是空字符串，就用.当前目录
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"已保存:{filepath}")
    return filepath

def load_json(filepath:str)->dict: 
    """接受文件路径，返回字典"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在:{filepath}") #先检查文件是否存在，不存在抛异常结束，
    with open(filepath,"r",encoding="utf-8") as f:
        return json.load(f) #读取json文件，直接返回
#验证函数
test_data= {"test":"data"}
save_json(test_data,"data/test_output.json")
loaded_back = load_json("data/test_output.json")
print(f"读验证:{loaded_back["test"]}") #保存，读取，验证，test字段值是data

# 独立任务：写一个"测试结果记录器"
# 功能1：每次执行用例后，把结果append到 data/test_results.json
# 功能2：读取记录文件，统计总通过率
# 功能3：找出所有失败用例，单独输出到 data/failed_cases.json
# 注意：要用上面封装好的 save_json / load_json 工具函数

#功能1，追加记录，每次跑完用例，把结果加到data/test_results.json,比如：test_results=[{"case_id":"tc001","status":"pass","duration":"0.2"}]
#先用load_json读取现有记录，如果文件不存在，先建空列表
#用.append()把新结果加到列表末尾
#用save_json 写回文件

def record_results(new_results,filepath="data/test_results.json"):
    try:
        results = load_json(filepath) #读取现有记录
    except FileNotFoundError:
        results = [] #文件不存在，从空列表开始
    results.append(new_results) #追加结果
    save_json(results,filepath) #写回文件
    return new_results 

#功能2，统计通过率，读取test_results 算通过率和失败率

def calc_pass_rate(filepath="data/test_results.json"):
    results = load_json(filepath) #读取文件内容
    total = len(results)
    if total == 0:
        return 0
    pass_count = sum(1 for c in results if c["status"]=="pass")
    return round(pass_count/total *100,1)

#功能3，提取失败用例，不是计算失败率
#读取test_reuslts.json，然后筛选状态为fail, 写入failed_cases.json
def extract_failed(filepath="data/test_results.json",out="data/failed_cases.json"):
    results = load_json(filepath)
    failed = [c for c in results if c["status"]=="fail"]
    save_json(failed,out)
    return failed

def reset_results(filepath="data/test_results.json"):
    """清空测试结果文件，每次跑测试前调用"""
    save_json([], filepath)
    print("已清空旧记录")

# ===== 主流程 =====

# 1. 先清空旧数据（"新建一轮测试"）
reset_results()


# 2. 开始记录这一轮的测试结果
record_results({"case_id": "TC001", "status": "pass", "duration": 1.2})
record_results({"case_id": "TC002", "status": "fail", "duration": 1.5})
record_results({"case_id": "TC003", "status": "fail", "duration": 1.2})
record_results({"case_id": "TC004", "status": "pass", "duration": 1.6})
record_results({"case_id": "TC005", "status": "fail", "duration": 1.2})

# 3. 统计通过率
rate = calc_pass_rate()
print(f"通过率:{rate}%")

# 4. 导出失败用例
extract_failed()

