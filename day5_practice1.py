#根据输入的参数，自动拼接一段标准化的Prompt文本
def build_test_case_prompt(feature,platform = "android",test_type = "normal",case_count = 5):
    """构建测试用例prompt
    feature:功能名称
    platform: 平台,Android/iOS/Web
    test_type:  normal/exception/boundary/security
    case_count: 生成用例数量
    """
    type_guide = {
        "normal": f"重点覆盖正常业务流程，包含{case_count}条核心场景",
        "exception": f"重点覆盖异常场景（网络/服务器/参数异常），共{case_count}条",
        "boundary":  f"重点覆盖边界值（最大/最小/空值/特殊字符），共{case_count}条",
        "security":  f"重点覆盖安全场景（越权/注入/敏感信息泄露），共{case_count}条",
    }
    return (
        f"【角色】你是一名有5年{platform}端测试经验的测试工程师，"
        f"专注于【{feature}】功能的质量保障。\n\n"
        f"【任务】请为【{platform}端 - {feature}】设计测试用例\n\n"
        f"【要求】{type_guide.get(test_type, type_guide['normal'])}\n\n"
        f"【格式】每条用例以 Markdown 表格输出，必须包含：\n"
        f"| 编号 | 用例标题 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |\n\n"
        f"优先级标准:P0=核心功能/P1=重要功能/P2=一般功能\n"
        f"步骤必须编号(1. 2. 3),不少于3步。"
    )
# 测试4种类型的Prompt
if __name__ == "__main__":
    for t in ["normal", "exception", "boundary", "security"]:
        prompt = build_test_case_prompt("用户登录", test_type=t, case_count = 6)
        print(f"\n{'='*50}\n类型: {t}")
        print(prompt[:200] + "...")