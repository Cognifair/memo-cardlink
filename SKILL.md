---
name: memo-cardlink
description: 卡跳跳 Memo-CardLink（原 Memo-Link），通过官方 MaiMemo OpenAPI 为现有墨墨记忆卡创建、修复和核验单向跳转或双向链接。用于目录卡导航、相关卡互链和 Card 引用审计；不负责仅打开卡片、移动卡片或新建卡片正文。
metadata:
  version: "1.0.7"
---

# 卡跳跳 Memo-CardLink v1.0.7

调用名：`$memo-cardlink`。原名 Memo-Link；用户沿用旧名称时按本技能处理，无需另建双向链接技能。旧 `$memo-link` 不再是独立安装入口。

在现有 Markji 卡片之间建立幂等、可核验的 Card 引用，保留无关正文与格式。

## 链接格式速查

- **正文跳转引用（卡跳跳写入）**：`[Card#ID/<目标 root_id>#显示文字]`。单向和双向语法相同，区别只在修改哪张卡；正文不能用 `card_id` 代替 `root_id`。
- **网页卡片定位（不是卡跳跳产出）**：`https://www.markji.com/deck/editor/<牌组网页 ID>?cardId=<卡片网页 ID>`。这是网页深链，使用网页 ID，不是 `mkjd_` API 牌组 ID 或 `root_id`。
- **牌组入口**：`https://www.markji.com/deck/<牌组网页 ID>`，不是单卡跳转。

详细对照、常见错误和交付边界见 [references/card-link-formats.md](references/card-link-formats.md)。不要把网页深链当 Card 语法，也不要把 Card 引用说成可分享 URL。

**样式不是链接语法**：`[Card#...]` 只负责跳转；默认绿色小标签版式是可选的 `[T#...]` 内容模板，不会由 CardLink 自动注入。模板里的分节标题和链接组标签由 AI 根据内容生成，不固定“考点直击/题目”；内容不支持具体标签时用“相关卡片”，不要硬贴考点或真题。已有卡片优先保留原样式，详细模板见上引。

## 只允许稳定 CLI

不要临时手写 `[Card#...]` 字符串或另建拼格式脚本。参考串统一由：

```text
python -B scripts/cli.py ref --root-id <root_id> --label <文字>
python -B scripts/cli.py check "<引用>"
```

生成/校验；只读查询用 `scripts/cl_probe.py`。命令、退出码和边界见 [references/cli-contract.md](references/cli-contract.md)。引用生成后仍按 [references/workflow.md](references/workflow.md) 读取目标、检查唯一性和重复引用。

## 选择链接模式

| 用户意图 | 模式 | 修改范围 |
|---|---|---|
| 从 A 跳到 B、目录指向详情、添加一个跳转 | 单向 A → B | 只修改 A，读取 B 以核实目标 |
| 双向链接、互链、来回跳转 | 双向 A ↔ B | A 引用 B，B 引用 A |
| 修复或审计现有引用 | 沿用已指定或能确定的原有方向 | 只修复已授权方向；审计不写入 |

用户只说“添加链接”且给出来源和目标时默认单向，并在预览中说明；来源、目标或对应关系不明确时先查找，仍无法确定才询问。不得仅因调用旧名称 Memo-Link 就推断双向。

单向操作不新增返回链接，也不删除目标卡已有的返回链接。把现有双向关系改成“仅单向”涉及删除：只有用户明确要求移除反向引用时才执行。混合批次逐条标明方向。目录与详情双向关联是逐对互链，不是把所有详情卡彼此全连接。

## 能力与资料

- API 操作前确认当前官方 MaiMemo OpenAPI 的认证、分页与更新规则；本技能自带 [references/workflow.md](references/workflow.md)。若本地有 `memo-cardest` 的 API 参考可对照，但缺失不阻断；找不到当前权威接口资料时暂停并说明，不猜测接口或自动切换私有 Web API。
- 读取 `MAIMEMO_TOKEN` 时用 `scripts/secret_resolver.py`：进程环境 → Windows 用户级环境变量 → `%LOCALAPPDATA%\MaimemoSecrets` → 工作区 `.memo-secrets`；工作区沙箱说明见 [references/credentials.md](references/credentials.md)。
- 规划、写入、修复或审计前读取 [references/workflow.md](references/workflow.md)。
- 客户端已登录且浏览器工具可用时，按工具文档检查渲染和点击。若当前环境要求 computer-use 技能，先读取该技能；不依赖已不存在的浏览器技能名称。

## 核心约束

- `[Card#ID/<root_id>#<label>]` 中使用目标的稳定 `root_id`；更新请求使用被修改卡所属牌组的实际 `card_id`，不能混用。
- 不输出或保存令牌，不把真实卡片、牌组 ID 固化到技能和示例中。当前任务需要的 ID 可用于本地变更清单和核验报告，不夹带无关卡片内容。
- 用户已明确要求执行的链接操作即为该范围的授权，不因尚需解析 ID 或选择普通插入位置重复求确认。只有请求含糊、需新增范围或删除未授权引用时，完成可读预览后再询问。只读审计不能变成修复。
- 写前刷新每张待修改卡片，保留最新正文、`grammar_version`、图片与无关语法；锚点不唯一、目标歧义或并发冲突时停止受影响写入。
- 已正确的引用视为无操作，不重复插入。双向只缺一端时仅补缺失端。
- 区分 API 回读、客户端渲染、实际点击到达目标三种验证，不把显示成链接等同于跳转成功。

## 交付

说明模式、实际修改卡片、已核验的有向关系、无操作与未完成项，以及三类验证各自的结果。批次部分失败不得宣称整批或双向关系完成。
