import json,os,random
from datetime import datetime

#定义2个json读写函数

def load_json(filepath): #读文件存为python对象
    with open(filepath,"r",encoding="utf-8") as f:
        return json.load(f)


def save_json(data,filepath): #把python data写到filepath
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok = True) ##从完整路径里提取目录部分，如果目录是空字符串，就用.当前目录
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=2)

#核心函数
def run_test_suite(suite_file):
    suite = load_json(suite_file) #读取json文件到python
    for case in suite["cases"] :   #遍历用例
        case["status"] = random.choice(["pass","fail","skip"]) #给用例状态随机测试结果
        case["executed_at"] = datetime.now().isoformat() #增加新key执行时间
    passed = sum(1 for c in suite["cases"] if c["status"]=="pass")
    failed = sum(1 for c in suite["cases"] if c["status"]=="fail")
    total = len(suite["cases"])
    rate = passed/total * 100
    pass_rate = f"{rate:.1f}%" #格式化字符串


    summary = {
        "用例总数":total,
        "通过":passed,
        "失败":failed,
        "通过率":pass_rate
        }
    
    report = {
        "suite_name":suite["suite_name"],
        "executed_at":datetime.now().isoformat(),
        "summary":summary,
        "cases":suite["cases"]
        }
    
    report_path = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"  #拼文件路径，格式 "reports/report_年月日_时分秒.json"
    save_json(report,report_path) #调用函数

    print(f"\n=== 测试执行报告 ===")
    print(f"套件:{suite['suite_name']}")
    print(f"总计:{summary['用例总数']}｜通过:{summary['通过']}｜失败:{summary['失败']}")
    print(f"通过率:{summary['通过率']}")
    return report_path

#入口
if __name__=="__main__": # 双下划线 × 2
    run_test_suite("data/test_suite_login.json") #使用test_suite_login.json调用  run_test_suite函数