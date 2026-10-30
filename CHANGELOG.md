# 变更记录

遵循语义化版本：修 bug → patch，新增能力 → minor，改变契约 → major。

## v1.0.0 — 2026-10-30

影响面：memo-cardlink(SKILL.md, README.md, CHANGELOG.md, version.json, references/workflow.md) / 6 个 Memo 仓库(README.md, references/satellites.md)

### 新增

- 首次发布「卡跳跳 Memo-CardLink」，由 Memo-Link 更名并独立建仓。
- 单向 A → B、双向 A ↔ B 与引用审计/修复三种模式。
- API 回读、客户端渲染、实际点击三层验证，明确区分未验证项。

### 变更

- 移除对已退役 `memo-api` 技能的硬依赖；改为直接核对当前官方 MaiMemo OpenAPI。
