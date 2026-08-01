# 今天的任务：优化Day5_practice1写的 build_test_case_prompt 函数
# 基于Day17的对比实验，加入以下改进：
# 1. 加入Few-shot示例（给AI看一个标准格式的例子）
# 2. 加入思维链引导（让AI先分析再输出）
# 3. 加强格式约束（严格要求表格格式）

import requests
import os
import sys 
import time # 429限流sleep等待
from dotenv import load_dotenv #从.env文件加载配置
load_dotenv()

#======从环境变量取api key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") #从环境变量取key

#======函数定义
def call_llm(prompt:str,system:str = "你是一名资深的测试工程师") -> str: #定义函数，传参：问题、角色设定，不设就是默认；函数返回一个字符串
    headers = {
        "Authorization":f"Bearer {DEEPSEEK_API_KEY}", #身份证明
        "Content-Type" : "application/json", #告诉服务器我要发的是json
    }
    data = {
        "model":"deepseek-chat", #用哪个模型
        "messages":[
            {"role":"system","content":system}, #角色设定
            {"role":"user","content":prompt}, #你的问题
        ],
        "temperature":0.7, #创意值
    }
    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,json=data,timeout=30,
    )
    r.raise_for_status() #如果返回4xx/5xx直接抛异常，不往下执
    response_json = r.json()
    content = response_json["choices"][0]["message"]["content"]
    tokens = response_json["usage"]["total_tokens"]
    print(f"token消耗:{tokens}")
    return content

# ===== 带重试机制的 LLM 调用 =====
def call_llm_safe(prompt:str,system = "你是一名资深的测试工程师",max_retries:int = 3) -> str:
    for attempt in range(max_retries):
        try:
            return call_llm(prompt,system) #调用call_llm函数
        except requests.exceptions.Timeout:
            print(f"尝试{attempt+1} 请求超时，重试...")
        except requests.exceptions.HTTPError as e: #抓http错误，存在变量e)
            if e.response.status_code == 429:
                wait = 2 ** attempt
                print(f"尝试{attempt+1}] API限流(429)，等待{wait}秒后重试...")
                time.sleep(wait)
            else:
                raise
    raise Exception(f"调用失败，已重试{max_retries}次")


def build_test_case_prompt_v2(feature,platform="Android",test_type="normal",case_count=5,example_case=None):
    """构建测试用例prompt
    feature:功能名称
    platform: 平台,Android/iOS/Web
    test_type:  normal/exception/boundary/security
    case_count: 生成用例数量
    examle_case: 用例参考范例
    """
    type_guide = {
        "normal": f"重点覆盖正常业务流程，包含{case_count}条核心场景",
        "exception": f"重点覆盖异常场景（网络/服务器/参数异常），共{case_count}条",
        "boundary":  f"重点覆盖边界值（最大/最小/空值/特殊字符），共{case_count}条",
        "security":  f"重点覆盖安全场景（越权/注入/敏感信息泄露），共{case_count}条",
    }

    #-----默认参考范例（如果用户没传example_case,用内置的）
    if example_case is None:
        example_case = (
             "| 编号 | 用例标题 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |\n"
             "|------|---------|---------|---------|---------|-------|\n"
             "| TC-PAY-EX-001 | 扫码支付-网络超时场景 | "
             "1.App版本v5.2.1已安装 "
             "2.已登录且余额>100元 "
             "3.WiFi网络延迟>5秒 | "
             "1.打开扫码页面 2.扫描有效商户码 "
             "3.输入金额10元 4.点击确认支付 "
             "5.在请求发送后立即断开网络 | "
             "页面5秒内弹出[网络异常，请检查网络后重试]提示，"
             "不扣款，支付按钮恢复可点击状态 | P1 |"
    )
    #---拼接返回v2prompt
    return (
        f"【角色】你是一名拥有10年经验的资深测试架构师,"
        f"精通{platform}端自动化测试和探索性测试，"
        f"擅长发现深层缺陷。\n\n"

        f"【参考范例】请严格模仿以下范例的格式和细节程度:\n\n"
        f"{example_case}\n\n"

        f"【思考步骤】请先分析再编写:\n"
        f"1.列出{feature}在{platform}端的3个关键异常风险点\n"
        f"2.将风险点转化为具体测试场景\n"
        f"3.为每个场景编写完整用例\n\n"

        f"【任务】为{platform}端-{feature}设计{case_count}条用例\n\n"

        f"【要求】{type_guide[test_type]}\n\n"

        f"【格式约束】\n"
        f"1.必须用markdown表格,含6列:编号/标题/前置条件/步骤/预期/优先级\n"
        f"2.前置条件三要素:App版本+网络状态+数据准备\n"
        f"3.预期结果必须可量化验证,禁用模糊描述\n"
        f"4.步骤用1.2.3编号,每步不超过1句话\n"
        f"5.优先级标注判定理由"
    )

#========== 导入 Day 5 的 Prompt 构建函数 =====
sys.path.insert(0,"/Users/songmumu/ai-test-journey")
from day5_practice1 import build_test_case_prompt

#======住程度
if __name__ == "__main__":
    feature = "扫描支付"
    prompt_v1 = build_test_case_prompt(feature,"Android","exception",5)
    prompt_v2 = build_test_case_prompt_v2(feature,"Android","exception",5)

    result_v1 = call_llm_safe(prompt_v1)
    result_v2 = call_llm_safe(prompt_v2)

    with open("/Users/songmumu/ai-test-journey/test_cases_v1.md", "w", encoding="utf-8") as f:
        f.write(f"# v1 原始版输出\n\n{result_v1}")
    with open("/Users/songmumu/ai-test-journey/test_cases_v2.md", "w", encoding="utf-8") as f:
        f.write(f"# v2 增强版输出\n\n{result_v2}")