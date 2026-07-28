from datetime import datetime
import random,os,json

def save_json(data,filepath): #把python data写到filepath
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok = True) #从完整路径里提取目录部分，如果目录是空字符串，就用.当前目录
    with open(filepath,"w",encoding="utf-8") as f:
       json.dump(data,f,ensure_ascii=False, indent=2)

class TestCase:
    """测试用例类"""
    def __init__(self,id:str,title:str,priority:str): #创建实例
        self.id = id
        self.title = title
        self.priority = priority
        self.status = "pending" #默认状态
    
    def execute(self,result:bool)-> str: #定义方法，方法访问自己实例
        """执行用例，传入结果"""
        self.status = "pass" if result else "fail"
        return self.status
    
    def to_dict(self)->dict: #定义方法，把实例自己变成字典
        """转化为dict,方便JSON"""
        return{"id":self.id,"title":self.title,"priority":self.priority,"status":self.status} #把我身上的四个属性（id、title、priority、status），打包成一个字典还回去。
    
    def __repr__(self):
        return f"TestCase({self.id}:{self.title}[{self.status}])"
    
#使用
tc = TestCase("TC001","正常登录","P0") # 调用 TestCase 模板，造一个叫 tc 的实例
print(tc)
tc.execute(True)
print(tc.to_dict())
print(tc.status)


# 独立任务：写一个 TestSuite 类
# # 属性：name / cases（list）/ created_at
# # 方法：
# #   add_case(case: TestCase)       → 添加用例
# #   run_all()                      → 模拟执行所有用例，随机pass/fail
# #   get_summary()                  → 返回统计结果dict
# #   save(filepath: str)            → 保存到JSON文件（复用day5的save_json）


class TestSuite:
    def __init__(self,name:str,cases:list):
        self.name = name
        self.cases = cases
        self.created_at = datetime.now().isoformat()

    def add_case(self,case:'TestCase') ->None: 
        self.cases.append(case)  #添加用例
    
    def run_all(self):
        """执行所有用例，返回结果列表"""
        results = [] #空列表，收集结果
        for case in self.cases:
            result = random.choice([True,False]) 
            case.execute(result) #调用例自己的execute
            results.append(case.to_dict()) #收集执行后调用例转成dict
        return results
    
    def get_summary(self):
        passed = sum(1 for c in self.cases if c.status == "pass" )
        failed = sum(1 for c in self.cases if c.status == "fail")
        pending = sum(1 for c in self.cases if c.status == "pending")
        total = len(self.cases)
        rate = passed/total * 100
        pass_rate = f"{rate:.1f}%" #格式化字符串
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pending": pending,
            "pass_rate": pass_rate
            }
    
    def save(self,filepath:str):
        data = {
            "name":self.name,
            "created_at" : self.created_at,
            "summary" : self.get_summary(),
            "cases" : [case.to_dict() for case in self.cases]
        }
        save_json(data,filepath)
        

if __name__ == "__main__":
    # 入口：创建 suite、add_case、run_all、save
    tc1 = TestCase("TC001","用账号密码登录","P0")
    tc2 = TestCase("TC002","用邮箱登录","P1")
    tc3 = TestCase("TC003","用微信登录","P2")
    #创建套件
    suite = TestSuite("登录模块回归测试",[tc1,tc2,tc3])
    #用add_case再加一个
    tc4 = TestCase("TC004","用手机号登录","P2")
    suite.add_case(tc4)
    #执行
    results = suite.run_all()
    print("=" * 40)
    for r in results:
        print(f"{r['id']}:{r['title']}→ {r['status']}")
    #统计
    print("=" * 40)
    for k, v in suite.get_summary().items():
        print(f"{k}:{v}")
    #保存
    suite.save("data/test_suite_result.json")
    print("=" * 40)
    print("已保存")