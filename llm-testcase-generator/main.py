from generator import LLMTestCaseGenerator

gen = LLMTestCaseGenerator()

#生成用户登录功能的测试用例（三种类型）
result = gen.generate(
    feature = "用户登录",
    platform = "Android",
    test_types = ["normal","exception","boundary"],
    case_count = 6
    )

path = gen.save(result)
print(f"生成完成,JSON文件保存在:{path}")
