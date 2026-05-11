"""项目级常量定义。"""

FIELDNAMES = [
    "文件名",
    "发票号码",
    "开票日期",
    "出发站",
    "到达站",
    "车次",
    "乘车日期",
    "开车时间",
    "车厢号",
    "座位号",
    "席别",
    "票价(元)",
    "乘车人",
    "证件号(脱敏)",
    "电子客票号",
    "备注",
]

REIMBURSEMENT_FIELD = "报销状态"
FIELDNAMES_EXT = FIELDNAMES + [REIMBURSEMENT_FIELD]

STATUS_OK = "ok"
STATUS_EMPTY_TEXT = "empty_text"
STATUS_UNRECOGNIZED = "unrecognized"
STATUS_ERROR = "error"

DEFAULT_PENDING_REIMBURSEMENT = "未报销"
DONE_REIMBURSEMENT = "已报销"

ALLOWED_EXTENSIONS = {".pdf"}
