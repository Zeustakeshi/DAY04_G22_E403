from __future__ import annotations

import json
import re
from typing import Any
from tools._shared import err

def analyze_token_usage(text: str = "", detail_level: str = "basic") -> dict[str, Any]:
    """
    Tính toán ước lượng số lượng token, số từ, số ký tự của đoạn văn bản hoặc dữ liệu JSON,
    đưa ra phân tích mật độ thông tin và cảnh báo nếu context quá lớn.
    """
    try:
        if isinstance(text, (dict, list)):
            text_str = json.dumps(text, ensure_ascii=False)
        else:
            text_str = str(text or "")

        char_count = len(text_str)
        words = re.findall(r'\w+', text_str)
        word_count = len(words)

        # Estimate tokens (approx 1 token ~= 4 chars or 0.75 words for standard EN/VN mixed text)
        estimated_tokens = int(round(char_count / 4.0))

        # Context health indicator
        if estimated_tokens < 1000:
            status = "optimal"
            recommendation = "Kích thước token tối ưu cho LLM Context Window."
        elif estimated_tokens < 4000:
            status = "moderate"
            recommendation = "Kích thước trung bình, có thể nén bằng 'smart_compress' nếu làm việc đa lượt."
        else:
            status = "heavy"
            recommendation = "Kích thước văn bản lớn (>4000 tokens). Khuyến nghị dùng 'smart_compress' hoặc 'summarize' trước khi trả về."

        result = {
            "tool": "token_stats",
            "char_count": char_count,
            "word_count": word_count,
            "estimated_tokens": estimated_tokens,
            "status": status,
            "recommendation": recommendation
        }

        if detail_level == "detailed":
            result["lines_count"] = text_str.count("\n") + 1
            result["avg_word_length"] = round(char_count / max(1, word_count), 2)

        return result
    except Exception as exc:
        return err("token_stats", exc)
