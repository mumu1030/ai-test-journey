#=======AI测试用例生成器=======
import json #把python字典变成json字符串，方便存文件
import os #检查/创建文件夹用（os.makedirs)
from datetime import datetime #给生成结果打时间戳

class LLMTestCaseGenerator:
    """AI测试用例生成器"""
    def __init__(self):
        from llm_client import call_llm_safe
        from prompt_builder import build_test_case_prompt_v2

        #把这两个函数挂在self上，变成对象的能力
        self.call_llm = call_llm_safe
        self.build_prompt = build_test_case_prompt_v2
    #=====核心方法

    def generate(self,feature:str,platform:str = "Android",test_types: list = None, case_count: int = 5
                 ) -> dict: #返回一个大字典，包含所有结果和元数据
        if test_types is None:
            test_types = ["normal","exception","boundary"]
            print(f"开始生成[{feature}]的测试用例...")

        all_cases = {} #空字典，准备装结果

        for t in test_types: # 遍历 ["normal", "exception", "boundary"]
            prompt = self.build_prompt(feature,platform,t,case_count)   # 步骤1：让（prompt_builder）拼一条精准的 promp
            result = self.call_llm(prompt)  # 步骤2：把拼好的 prompt 交给（llm_client），调 DeepSeek 拿结果
            all_cases[t] = result
            print(f"{t}类型生成完成")

        return{
        "feature":feature,
        "platform":platform,
        "generated_at":datetime.now().isoformat(),
        "total_types":len(test_types),
        "cases":all_cases
    }

    def save(self,result:dict,output_dir:str = "output")->str:
        """将生成结果保存为 JSON 文件"""
        # 如果 output/ 文件夹不存在，自动创建
        # exist_ok=True → 如果文件夹已经有了也不报错
        os.makedirs(output_dir,exist_ok=True)

        # 生成文件名：功能名_时间戳.json
        # 比如 "扫码支付_20260727_113000.json"
        # 时间戳的作用：同一天多次生成，文件名不重，不会覆盖旧的
        ts = datetime.now().strftime('%Y%m%d"_%H%M%S')

        #存json
        filename = f"{result['feature']}_{ts}.json"
        filepath = os.path.join(output_dir,filename)
        # 写入文件
        # json.dump 把 Python 字典变成 JSON 字符串写入文件
        # ensure_ascii=False → 中文正常显示，不变成 \uxxxx 乱码
        # indent=2 → 缩进 2 格，方便人眼看
        with open(filepath,"w",encoding="utf-8") as f:
            json.dump(result,f,ensure_ascii=False, indent=2)
        return filepath