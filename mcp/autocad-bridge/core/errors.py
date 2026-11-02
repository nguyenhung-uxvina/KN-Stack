"""Lỗi có mã ổn định — agent đọc `code`, không đoán theo câu chữ."""

CODES = {
    "ACAD_NOT_RUNNING": "AutoCAD chưa chạy",
    "ACAD_BUSY": "AutoCAD đang bận (đang chạy lệnh / mở hộp thoại)",
    "ACAD_TIMEOUT": "Hết giờ trước khi lời gọi được chạy — chưa có gì thay đổi",
    "UNKNOWN_COMMIT": "Hết giờ khi lời gọi đang chạy — có thể đã ghi; kiểm bản vẽ trước khi làm lại",
    "DOCUMENT_CHANGED": "Bản vẽ hiện hành không phải bản vẽ đã chỉ định",
    "DOCUMENT_NOT_FOUND": "Không thấy bản vẽ đã chỉ định",
    "READ_ONLY_TARGET": "Bản vẽ đích đang mở chỉ đọc",
    "PATH_DENIED": "Đường dẫn nằm ngoài vùng được phép",
    "COMMAND_DENIED": "Lệnh không nằm trong allow-list",
    "CONFIRM_REQUIRED": "Thao tác phá huỷ cần plan_token hợp lệ",
    "COM_ERROR": "Lỗi COM từ AutoCAD",
    "INVALID_ARGUMENT": "Tham số không hợp lệ",
    "INTERNAL_ERROR": "Lỗi ngoài dự kiến trong bridge",
}


class BridgeError(Exception):
    def __init__(self, code, message="", hint=None, data=None):
        super().__init__(message or CODES.get(code, code))
        self.code = code
        self.message = message or CODES.get(code, code)
        self.hint = hint
        self.data = data or {}

    def to_dict(self):
        d = {"ok": False, "code": self.code, "message": self.message}
        if self.hint:
            d["hint"] = self.hint
        if self.data:
            d["data"] = self.data
        return d
