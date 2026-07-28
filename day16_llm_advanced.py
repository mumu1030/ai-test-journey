import requests #导入requests库，发http请求用
import os 
import time
import sys

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

# ===== 今天的核心：带重试机制的 LLM 调用 =====
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

#=====测试调用
if __name__=="__main__":
    prompt = build_test_case_prompt("用户登录","Android","exception",5)
    result = call_llm_safe(prompt)
    with open("test_cases.md","w",encoding="utf-8") as f:
        f.write(result)
        print("测试用例保存到test_cases.md")