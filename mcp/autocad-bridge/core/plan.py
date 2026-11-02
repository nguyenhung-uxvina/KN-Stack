"""Token xác nhận cho thao tác phá huỷ (save ghi đè, close bỏ thay đổi).

Bước thử trả plan_token = HMAC(bí mật theo tiến trình, hành động|doc_id|revision|tham số|hạn).
Bước thật chỉ chạy khi token khớp ĐÚNG hành động, bản vẽ, revision và tham số — bản vẽ bị sửa sau
bước thử thì token mất hiệu lực. Không phụ thuộc elicitation của client (spec MCP đổi qua các bản).
"""
import hashlib
import hmac
import json
import os
import time


class PlanTokens:
    def __init__(self, ttl: float = 120.0):
        self.ttl = ttl
        self._key = os.urandom(32)

    def _mac(self, action, doc_id, revision, params, exp) -> str:
        msg = json.dumps([action, doc_id, revision, params, exp], sort_keys=True, default=str)
        return hmac.new(self._key, msg.encode("utf-8"), hashlib.sha256).hexdigest()

    def issue(self, action, doc_id, revision, params) -> str:
        exp = f"{time.time() + self.ttl:.3f}"
        return f"{exp}~{self._mac(action, doc_id, revision, params, exp)}"

    def verify(self, token, action, doc_id, revision, params) -> bool:
        exp, sep, mac = str(token).partition("~")
        if not sep:
            return False
        try:
            if float(exp) < time.time():
                return False
        except ValueError:
            return False
        return hmac.compare_digest(mac, self._mac(action, doc_id, revision, params, exp))
