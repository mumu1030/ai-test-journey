#====目标：用三种不同的prompt写法问同一个问题

import requests #导入requests库，发http请求用，call_llm需要
import os #读取环境变量api Key
import time # 429限流sleep等待
import sys #往sys.path 加路径，实现跨目录导入

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

#========== 导入 Day 5 的 Prompt 构建函数 =====
sys.path.insert(0,"/Users/songmumu/ai-test-journey")
from day5_practice1 import build_test_case_prompt


#=========构建基础问题======
base_festure = "用户登录" #要测试功能
base_platform = "Android" #目标平台
base_type = "exception" #异常场景测试
base_count = 3 #每种模式生成3条用例

base_prompt = build_test_case_prompt(base_festure,base_platform,base_type,base_count)


#======定义三种prompt
#核心思路：不只在user prompt里简单说“你是测试工程师。。。”，而是把system角色描述得非常具体，专业，有约束性

#======模式1:角色提示
role_system = (
    "你是一名拥有 15 年经验的资深软件测试架构师,"          # 画一个具体的人设
    "精通 Android/iOS/Web 全平台测试，"                     # 明确技能范围
    "擅长黑盒测试、探索性测试和异常场景分析。"               # 突出这次任务的强项
    "你的测试用例严格遵循以下标准：\n"                       # 给输出加约束
    "1. 前置条件必须可复现，包含具体的环境版本号\n"          # 前置条件要具体
    "2. 测试步骤编号清晰，每步不超过一句话\n"                # 步骤要简洁
    "3. 预期结果必须可量化、可验证（不是功能正常这种模糊描述）\n"  # 结果要有判断标准
    "4. 优先级按真实业务影响判定，不是随便标 P0"             # 优先级要有依据
    )

#======模式2:Few-shot Prompting（少样本提示）
#核心思路：在user prompt里嵌入1-2个范例用例，让AI参考模仿写

fewshot_example = (
    "【请严格参考以下范例的格式来生成测试用例】\n\n"
    "=====范例用例=====\n"
        "| 编号 | 用例标题 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |\n"
    "|------|---------|---------|---------|---------|-------|\n"
    "| TC-LOGIN-EX-001 | 登录接口-网络超时场景 | "             # 一个有编号的范例
    "1.App版本v3.2.1已安装 2.设备已连接WiFi但网络延迟>5秒 | "  # 具体的前置条件
    "1. 打开App进入登录页 2. 输入正确账号密码 3. 点击登录 4. 在请求过程中手动断开网络 | "  # 带编号的步骤
    "系统在5秒内弹出网络连接超时,请重试提示，不跳转首页，已输入内容不清空 | "  # 具体可验证的预期
    "P1 |\n\n"                                                # 优先级

    "=== 你的任务 ===\n")
#把范例拼在 base_prompt前面
fewshot_prompt = fewshot_example + base_prompt

#======模式3:chain of thouht====
# 核心思路：在user prompt里加入步骤，不让AI直接写答案，让它分步思考分析

cot_instruction = (
   "【请按以下三个步骤思考并生成测试用例，每一步的输出都要写出来】\n\n"

    "步骤一 — 风险分析：\n"                                   # 第一步：先想清楚测什么
    "先分析「用户登录-Android端」的核心功能和关键风险点，"     # 分析功能风险
    "列出至少 3 个最容易出问题的环节，"                        # 至少 3 个风险点
    "按风险严重程度排序。\n\n"                                # 排优先级

    "步骤二 — 场景设计：\n"                                   # 第二步：把风险变成场景
    "基于步骤一的风险分析，列出需要覆盖的测试场景，"           # 从风险到场景
    "确保每个高风险环节都至少有一个对应的异常场景。\n\n"       # 高风险必须覆盖

    "步骤三 — 用例编写：\n"                                   # 第三步：才真正写用例
    "为上一步列出的每个场景，设计具体的测试用例，"             # 场景 → 用例
    "用 Markdown 表格输出。\n\n"                               # 输出格式

    "下面开始：\n"
)

#把分布思考拼在base_prompt前面
cot_prompt = cot_instruction + base_prompt


#=====测试调用
if __name__=="__main__":
        # 保存根目录
    save_dir = "/Users/songmumu/ai-test-journey"

    # --- 模式 1：角色提示 ---
    print("=" * 60)
    print("模式 1: Role Prompting(角色提示)")
    print("=" * 60)
    result_role = call_llm_safe(base_prompt, role_system)
    
    with open(f"{save_dir}/test_cases_role.md","w",encoding="utf-8") as f:
        f.write(f"#模式1:Role Prompting(角色提示)\n\n{result_role}")
    print("已保存,test_case_role.md\n")

    # ----模式2:范例提示----
    print("=" * 60)
    print("模式 2: Few-shot Prompting(少样本提示)")
    print("=" * 60)
    result_fewshot = call_llm_safe(fewshot_prompt)

    with open(f"{save_dir}/test_cases_fewshot.md","w",encoding="utf-8") as f:
        f.write(f"#模式2:Few-shot Prompting(少样本提示)\n\n{result_fewshot}")
    print("已保存,test_case_fewshot.md\n")

    #---模式3:思维链
    print("=" * 60)
    print("模式 3: Chain of Thought(思维链)")
    print("=" * 60)
    result_cot = call_llm_safe(cot_prompt)

    with open(f"{save_dir}/test_cases_cot.md","w",encoding="utf-8") as f:
        f.write(f"#模式3:Chain of Thought(思维链)\n\n{result_cot}")
    print("已保存,test_case_cot.md\n")

    #---总结对比提示
    print("=" * 60)
    print("三种模式已全部生成完毕，对比文件：")
    print(f"  1️⃣  test_cases_role.md    — Role Prompting")
    print(f"  2️⃣  test_cases_fewshot.md  — Few-shot Prompting")
    print(f"  3️⃣  test_cases_cot.md      — Chain of Thought")
    print("=" * 60)
    print("\n💡 对比时关注这几点：")
    print("  · 用例格式是否规范统一？")
    print("  · 步骤是否具体可执行？")
    print("  · 预期结果是否可验证？")
    print("  · 异常场景覆盖是否全面？")