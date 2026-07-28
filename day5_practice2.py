#你是测试工程师，请为 {platform} 端的「{feature}」设计 5 条测试用例。格式：编号 | 标题 | 步骤 | 预期
def test_cases_prompt(feature,platform):
  """
  platform: ios/android
  feature: 功能名称，如"用户登录"
  """
  return(
    f"【角色】你是测试工程师\n"
    f"【任务】请为{platform}端的{feature}设计5条测试用例。\n"
    f"【格式】每条用例以 Markdown 表格输出，必须包含：\n"
    f"| 编号 | 用例标题 | 前置条件 | 测试步骤 | 预期结果 |\n\n"
)
prompt = test_cases_prompt("用户登录","ios")
print(prompt)