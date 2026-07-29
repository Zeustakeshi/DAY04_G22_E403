from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def send_telegram(text: str = "", confirmed: bool = False, chat_id: str | None = None) -> dict[str, Any]:
    if not confirmed:
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "message": "Only send after the user explicitly confirms.",
        }
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN", "8614785084:AAFodmLHytuXLqK4e1RBdnQosW9-hQHORKY")
        target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        # Nếu chưa có chat_id, tự động gọi getUpdates để tìm chat_id của người dùng đã nhắn tin cho bot
        if not target_chat_id:
            try:
                updates_res = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=TIMEOUT).json()
                if updates_res.get("ok") and updates_res.get("result"):
                    for update in reversed(updates_res["result"]):
                        msg = update.get("message") or update.get("channel_post") or update.get("edited_message")
                        if msg and "chat" in msg and "id" in msg["chat"]:
                            target_chat_id = str(msg["chat"]["id"])
                            # Tự động lưu vào environment để sử dụng lại
                            os.environ["TELEGRAM_CHAT_ID"] = target_chat_id
                            break
            except Exception:
                pass

        if not target_chat_id:
            raise RuntimeError(
                "Missing TELEGRAM_CHAT_ID. Vui lòng mở Telegram, tìm bot @ahjfdhsdjfh_bot và nhấn /start hoặc gửi 1 tin nhắn cho bot, sau đó thử lại."
            )

        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": target_chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=TIMEOUT,
        )
        if response.status_code == 400:
            # Fallback mà không dùng Markdown nếu bị lỗi parse Markdown
            response = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": target_chat_id, "text": text},
                timeout=TIMEOUT,
            )
        response.raise_for_status()
        return {"tool": "send_telegram", "status": "sent", "chat_id": target_chat_id}
    except Exception as exc:
        return err("send_telegram", exc)


