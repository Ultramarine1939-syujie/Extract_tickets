# 贡献指南

感谢你愿意改进这个项目。提交变更前，请优先保证：

- 不提交真实票据 PDF、身份证号、报销明细等敏感数据。
- 解析规则变更需要补充或更新 `tests/test_parser.py`。
- Web 接口改动需要保留旧接口兼容，除非 README 明确说明破坏性变更。

## 本地开发

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## 代码约定

- 解析逻辑放在 `src/extract_tickets/parser.py`。
- CSV / Excel 导出逻辑放在 `src/extract_tickets/export.py`。
- Flask 路由放在 `src/extract_tickets/web.py`。
- 根目录 `app.py`、`extract_tickets.py`、`parser.py` 仅用于兼容旧入口。
