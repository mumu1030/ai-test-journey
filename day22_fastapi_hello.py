from fastapi import FastAPI
from pydantic import BaseModel #数据类型模版，请求/响应结构时用来当模版
from typing import Optional

app = FastAPI(title="AI测试用例生成服务",version="0.1.0") #用FastAPI造了个实例对象

# Pydantic模型：定义POST请求的body结构
class TestRequest(BaseModel): #定义请求"用户传给我的数据长什么样"
    fetuare: str
    platform: str = "Android"
    test_type: str = "normal"
    case_count: int = 5

class TestResponse(BaseModel): #定义响应"我返回给用户的数据长什么样"
    feature: str
    platform: str
    cases: list
    message: str = "生成成功"

#GET接口:健康检查
@app.get("/") #访问服务的根路径 /
def root():
    return{"message":"AI测试用例生成服务运行中","status":"ok"}

#GET:带路径参数
@app.get("/features/{feature_name}") #访问服务的路径，查询功能信息
def get_feature_info(feature_name:str):
    return{"feature":feature_name,"description":f"这是{feature_name}功能的信息"}

#POST接口：生成测试用例
@app.post("/generate",response_model=TestResponse) #生产测试用例
def generate_test_cases(request:TestRequest):
    mock_cases = [
        f"用例{i+1}:【{request.test_type}】{request.feature}场景{i+1}"
        for i in range(request.case_count)
    ]
    return TestResponse(
        feature = request.feature,
        platform = request.platform,
        cases = mock_cases
    )