# 变更记录

遵循语义化版本：修 bug → patch，新增能力 → minor，改变契约 → major。

## v1.0.3 — 2026-11-04

影响面：memo-cardlink(技能名称、调用示例与系列引用) / memo-ankigo / memo-txt

- 将 Anki 迁移技能标识统一为 `memo-ankigo`，TXT 技能标识统一为 `memo-txt`，更新安装路径与系列引用。
- 本次仅调整命名与文档；Anki 历史迁移包格式保持兼容。

## v1.0.2 — 2026-11-03

影响面：memo-cardlink(README.md, references/satellites.md)

### 变更

- MEMO-CARDLINK: 系列清单更新为墨兰迪 Memo-Canvas。

## v1.0.1 — 2026-10-31

影响面：memo-cardlink(SKILL.md, scripts/secret_resolver.py, references/credentials.md, version.json)

### 修复

- 凭证读取不再只依赖进程环境变量：统一经 `secret_resolver.py` 读取进程环境、Windows 用户级环境、`%LOCALAPPDATA%\MaimemoSecrets` 与工作区 `.memo-secrets`，支持工作区沙箱。

## v1.0.0 — 2026-10-30

影响面：memo-cardlink(SKILL.md, README.md, CHANGELOG.md, version.json, references/workflow.md) / 6 个 Memo 仓库(README.md, references/satellites.md)

### 新增

- 首次发布「卡跳跳 Memo-CardLink」，由 Memo-Link 更名并独立建仓。
- 单向 A → B、双向 A ↔ B 与引用审计/修复三种模式。
- API 回读、客户端渲染、实际点击三层验证，明确区分未验证项。

### 变更

- 移除对已退役 `memo-api` 技能的硬依赖；改为直接核对当前官方 MaiMemo OpenAPI。
