"""
接口自动化服务
被测服务:day23_fastapi_with_llm（AI测试用例生成服务v2)
前提：启动FastAPI 服务；启动实例：uvicorn day23_fastapi_with_llm:app --reload
确保服务跑在：http://127.0.0.1:8000/

"""
import requests

base_URL = "http://127.0.0.1:8000/"

passed = 0
failed = 0

def run_test(name, test_func):
    global passed,failed
    try:
        test_func()
        print(f" PASS{name}")
        passed +=1
    except Exception as e:
        print(f" FAIL{name} ->{e}")
        failed +=1

#测试1：健康检查接口 GET/, 对应@app.get("/")
def test_health_check():
    response = requests.get(f"{base_URL}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "AI测试用例生成服务运行中"

#测试2:路径参数接口 GET/feature/{feature_name}
#对应你的 @app.get("/features/{feature_name}")

def test_get_feature_info():
    response = requests.get(f"{base_URL}/features/login")
    assert response.status_code == 200, f"期望200,实际{response.status_code},返回:{response.text}"
    data = response.json()
    assert data["feature"] == "login"

#测试3:参数校验 - feature 为空  POST /generate
def test_generate_empty_feature():
    payload = {
        "feature": "",
        "platform": "Android",
        "test_type": "normal",
        "case_count": 5,
    }
    response = requests.post(f"{base_URL}/generate", json = payload)
    assert response.status_code == 422

#测试4:参数校验 - case_count 为0  POST /generate
def test_generate_zero_count():
    payload = {
        "feature": "",
        "platform": "Android",
        "test_type": "normal",
        "case_count": 0,
    }
    response = requests.post(f"{base_URL}/generate", json = payload)
    assert response.status_code == 422

# ============================================================
# 测试5：正常生成  POST /generate（需要 LLM 服务正常运行）
# ============================================================
def test_generate_success():
    payload = {
        "feature": "登录",
        "platform": "Android",
        "test_type": "normal",
        "case_count": 5,
    }
    response = requests.post(f"{base_URL}/generate", json = payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["feature"] == "登录"
    assert len(data["case_markdown"]) > 0

# ============================================================
# 主流程：跑所有测试，打印汇总
# ============================================================
if __name__ == "__main__":
    print("=="*20)
    print("接口自动化用例")
    print("=="*20)

    run_test("健康检查 GET /", test_health_check)
    run_test("路径参数 GET /features/login", test_get_feature_info)
    run_test("参数校验-feature为空", test_generate_empty_feature)
    run_test("参数校验-case_count=0", test_generate_zero_count)
    run_test("正常生成(需LLM)", test_generate_success)

    total = passed + failed
    rate = round(passed/total * 100, 1) if total >0 else 0.0

    print("=="*20)
    print(f"总计:{total}个测试,通过{passed},失败{failed}")
    print(f"通过率:{rate}%")
    print("=="*20)



