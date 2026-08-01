# Day 24 — Postman 接口测试报告

## 测试目标

对 `day23_fastapi_with_llm.py` 的三个接口进行完整测试，验证正常场景和异常场景的响应。

## 接口清单

| 接口 | 方法 | URL |
|------|------|-----|
| 健康检查 | GET | `/` |
| 查询功能信息 | GET | `/features/{feature_name}` |
| 生成测试用例 | POST | `/generate` |

---

## 测试结果汇总

| 编号 | 测试场景 | 请求 | 预期结果 | 实际结果 | 状态 |
|------|---------|------|---------|---------|------|
| 1 | 健康检查 | GET `/` | 200，返回服务状态 | 200 OK，`{"message": "AI测试用例生成服务运行中", "status": "ok"}` | 通过 |
| 2 | 查询功能信息 | GET `/features/登录` | 200，返回功能信息 | 200 OK，`{"feature": "登录", "description": "这是登录功能的信息"}` | 通过 |
| 3 | 正常生成用例 | POST `/generate` 正常参数 | 200，AI 生成测试用例 | 200 OK，`case_markdown` 包含 5 条登录用例 | 通过 |
| 4 | feature 为空字符串 | POST `/generate` `{"feature": ""}` | 应报错（空值无意义） | Bug：200 OK，AI 乱生成内容 | 已修复 |
| 5 | case_count 类型错误 | POST `/generate` `{"case_count": "abc"}` | 422 类型校验失败 | 422，`int_parsing` | Pydantic 自动拦截 |
| 6 | 缺少必填参数 | POST `/generate` 无 `feature` | 422 字段缺失 | 422，`missing` | Pydantic 自动拦截 |
| 7 | case_count 为负数 | POST `/generate` `{"case_count": -1}` | 应报错（负数无意义） | Bug：200 OK，浪费 API 调用 | 已修复 |

---

## Bug 详情与修复

### Bug 1：feature 传空字符串通过（测试4）

**问题**：`feature: str` 只校验类型，空字符串 `""` 也是合法字符串，导致 AI 收到空功能描述后乱生成内容。

**修复**：给 `feature` 加 `min_length=1` 限制：

```python
feature: str = Field(..., min_length=1, description="功能名称（必填）")
```

**修复后验证**：
- 请求：`{"feature": ""}`
- 返回：422 Unprocessable Content
- 错误：`"msg": "String should have at least 1 character"`

---

### Bug 2：case_count 传负数通过（测试7）

**问题**：`case_count: int` 只校验整数类型，`-1` 是合法整数，导致传入负数后 AI 生成无意义内容，浪费 API Token。

**修复**：给 `case_count` 加 `ge=1`（greater than or equal）限制：

```python
case_count: int = Field(default=5, ge=1, description="用例数量（至少1条）")
```

**修复后验证**：
- 请求：`{"feature": "登录", "case_count": -1}`
- 返回：422 Unprocessable Content
- 错误：`"msg": "Input should be greater than or equal to 1"`

---

## 学到的知识点

### Pydantic 自动校验 vs 业务校验

| 场景 | 谁负责 | 示例 |
|------|--------|------|
| 类型校验 | Pydantic 自动 | `case_count` 传 `"abc"` -> 422 `int_parsing` |
| 必填校验 | Pydantic 自动 | 缺少 `feature` -> 422 `missing` |
| 业务校验 | 手动加 Field 限制 | 空字符串、负数 -> 用 `min_length`、`ge` 限制 |

### Field 常用校验参数

| 参数 | 含义 | 适用类型 |
|------|------|---------|
| `min_length` | 最小长度 | `str` |
| `max_length` | 最大长度 | `str` |
| `ge` | >=（greater than or equal） | `int`、`float` |
| `gt` | >（greater than） | `int`、`float` |
| `le` | <=（less than or equal） | `int`、`float` |
| `lt` | <（less than） | `int`、`float` |

---

## 关键结论

1. Pydantic 能自动拦类型和必填问题，但拦不住业务层面的不合理值（如空字符串、负数）。
2. 业务校验要用 `Field(...)` 显式声明，比如 `min_length=1`、`ge=1`。
3. 测试异常场景和正常场景一样重要，Bug 往往藏在边缘 case 里。
4. Postman 的 Body 里 JSON 字符串必须加引号，`abc` 是非法 JSON，`"abc"` 才是合法字符串。
