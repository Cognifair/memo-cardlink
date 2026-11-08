# CLI 契约

卡跳跳只暴露这些稳定入口；不要临时拼 `[Card#...]` 字符串。

## 参考串

```text
python -B scripts/cli.py ref --root-id <目标 root_id> --label <显示文字>
python -B scripts/cli.py ref --root-id ... --label ... --json
```

- 只接受合法 root_id 和单行 label；
- 输出唯一的 `[Card#ID/<root_id>#<label>]`；
- `--json` 返回 `{"reference": "..."}`；
- 生成后仍要按 workflow 读取目标卡、核对 root_id、检查重复引用。

## 校验

```text
python -B scripts/cli.py check "[Card#ID/<root_id>#<label>]"
```

返回 `root_id`、`label`、`reference`；不合法时退出 1。

## 只读探测

```text
python -B scripts/cl_probe.py decks
python -B scripts/cl_probe.py chapters <deck_id>
python -B scripts/cl_probe.py probe <deck_id> <card_id>
python -B scripts/cl_probe.py dumptree <deck_id>
```

这些命令使用 `MAIMEMO_TOKEN`，只读，不写入。

## 退出码

- `0`：成功；
- `1`：输入/格式/操作失败；
- `2`：缺少凭证或依赖。

## 禁止

- 不让模型手写 `[Card#ID/...]` 后直接写入；
- 不把网页深链当 Card 语法；
- 不在 skill 里临时写脚本“拼格式”；
- 不把 `card_id` 当 `root_id`。
