from fastapi import FastAPI,HTTPException #导入fastapi和错误处理
from pydantic import BaseModel,Field
from day15_llm_api import call_llm
from day5_practice1 import build_test_case_prompt

#创建FastAPI 应用
app = FastAPI(title="AI测试用例生产服务 v2")

#定义请求数据模型
class GenerateRequest(BaseModel):
    feature: str = Field(..., min_length=1)  # 不能为空字符串
    platform: str = "Android"
    test_type: str = "normal"
    case_count: int = Field(default=5, ge=1)  # ge=1 表示必须 >= 1

#GET接口:健康检查
@app.get("/") #访问服务的根路径 /
def root():
    return{"message":"AI测试用例生成服务运行中","status":"ok"}

#GET:带路径参数
@app.get("/features/{feature_name}") #访问服务的路径，查询功能信息
def get_feature_info(feature_name:str):
    return{"feature":feature_name,"description":f"这是{feature_name}功能的信息"}

#Post接口:
@app.post("/generate")
def generate(req: GenerateRequest): #FastAPI 自动把请求 body 解析成 GenerateRequest 对象，自动校验类型
    try:
        #构建prompt
        prompt = build_test_case_prompt(
            req.feature,req.platform,req.test_type,req.case_count
        )
        #调AI
        result = call_llm(prompt)
        #返回结果
        return{
            "success": True,
            "feature": req.feature,
            "case_markdown": result
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"生成失败:{str(e)}")