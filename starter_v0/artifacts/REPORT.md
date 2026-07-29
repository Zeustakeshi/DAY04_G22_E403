# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
>
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 16:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: G22
- Members:

| STT | Họ và tên            | Mã học viên |
| :-: | -------------------- | ----------- |
|  1  | Đặng Nguyên Giáp     | 2A202601486 |
|  2  | Mai Tuấn Quang       | 2A202601484 |
|  3  | Nguyễn Thị Thu Trang | 2A202601172 |
|  4  | Phạm Minh Hiếu       | 2A202601562 |
|  5  | Hoàng Thị Thuyên     | 2A202601910 |
|  6  | Dương Tiến Dũng      | 2A202602020 |
|  7  | Đặng Quang Trung     | 2A202601510 |

- Provider/model: Openrouter

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent: Chuyên tìm kiếm thông tin tổng hợp trên web, tài liệu học thuật và mạng xã hội, sau đó đọc hiểu URL, tóm tắt nội dung cốt lõi và định dạng thành báo cáo để gửi qua Telegram.

**Link dùng thử (truy cập được trong showdown):**


URL: [http://localhost:8000](http://localhost:8000)

## A2. Tool agent có

| Tên tool            | Làm được gì                                                                                                | Tool mới nhóm thêm? |
| ------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------- |
| clarify             | Hỏi lại người dùng khi thiếu thông tin hoặc cần xác nhận trước hành động (yes/no)                          | không               |
| timeline            | Lấy các bài đăng gần đây của một tài khoản cụ thể (theo screenname)                                        | không               |
| social_search       | Tìm bài đăng trên mạng xã hội theo từ khóa/chủ đề                                                          | không               |
| lookup              | Tra cứu thông tin/tin tức trên internet (web)                                                              | không               |
| fetch               | Lấy nội dung từ một URL cụ thể                                                                             | không               |
| format              | Trình bày dữ liệu đã có (từ tool khác) thành văn bản markdown                                              | không               |
| send                | Gửi một đoạn văn bản lên Telegram (cần confirmed=true)                                                     | không               |
| policy              | Tìm trong tài liệu policy nội bộ công ty                                                                   | không               |
| papers              | Tìm bài báo khoa học trên arXiv (qua API có key)                                                           | không               |
| paper_text          | Lấy nội dung text của một bài báo arXiv (tải PDF + trích text)                                             | không               |
| web_search          | Tìm kiếm trên web qua DuckDuckGo, không cần API key, khi chưa có URL cụ thể                                | **có**              |
| paper_search        | Tìm bài báo khoa học trực tiếp trên arXiv, không cần API key                                               | **có**              |
| summarize           | Tóm tắt trích xuất (extractive) một đoạn văn bản dài thành các câu chính                                   | **có**              |
| keyword_extract     | Rút ra các từ khóa quan trọng nhất từ một đoạn văn bản                                                     | **có**              |
| smart_compress      | Nén thông minh văn bản dài dựa trên từ khóa truy vấn nghiên cứu, tiết kiệm 60–80% token context window     | **có (bonus)**      |
| evidence_synthesize | Hợp nhất, lọc trùng lặp (deduplication) và cô đọng danh sách bài viết/bằng chứng nghiên cứu từ nhiều nguồn | **có (bonus)**      |
| token_stats         | Phân tích và đo lường lượng token, số từ, độ dài văn bản để kiểm soát context window                       | **có (bonus)**      |

## A3. Câu hỏi mẫu để thử

1. "Tìm trên web giúp mình thông tin về giá vé máy bay Tết 2026."
2. "Tìm giúp mình vài bài báo khoa học về reinforcement learning from human feedback."
3. "Tóm tắt đoạn văn bản này thành đúng 2 câu chính: 'OpenAI released GPT-5 today. It brings major improvements in reasoning. The model is also faster than before. Many developers are excited about new API features.'"
4. "Đọc giúp mình bài này: https://openai.com/index/gpt-5/ — rồi tóm tắt lại thành 3 câu chính."
5. "Tìm trên web tin tức AI hôm nay, tóm tắt rồi gửi qua Telegram giúp mình."

## A4. Kịch bản demo đã rehearse

| Scenario                                                                                | Tool trace cần thấy                                                                      | Câu chuyện cải thiện version                                                                                                                                                                                                              | Fallback run/transcript       |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| Câu hỏi toán học / Out-of-scope (vd: tính tích phân, viết code Fibonacci, câu hỏi meta) | Không gọi tool nào (từ chối hoặc trả lời trực tiếp)                                      | Ở v0, agent vẫn cố gắng tìm kiếm công cụ hoặc gọi tool không phù hợp. Lên v1, nhờ bổ sung quy tắc "Scope & Non-Research Queries", agent đã biết trả lời trực tiếp mà không gọi tool.                                                      | Run v1 / Non-research queries |
| Tìm kiếm tin tức (xử lý lỗi ghép thừa từ khóa)                                          | `lookup(query="AI", topic="news")`                                                       | Ở v0/v1, khi tìm tin tức, agent ghép cả cụm "tin tức AI" vào tham số `query`. Lên v2, bổ sung quy tắc không đưa từ "news" hoặc "tin tức" vào `query` khi `topic="news"`, giúp trích xuất truy vấn chính xác hơn.                          | Run v2 / Test case R03, R10   |
| Xin xác nhận trước khi thực hiện hành động (vd: ghi hoặc gửi tin nhắn qua Telegram)     | `clarify(question="...", response_type="yes_no")`                                        | Ở v0/v1, tool `clarify` chưa có tham số ràng buộc kiểu phản hồi. Lên v2 và v3, `tools.yaml` bổ sung trường bắt buộc `response_type`, đồng thời prompt quy định rõ phải sử dụng `yes_no` khi cần xác nhận hành động.                       | Run v2, v3                    |
| Đổi ý trong hội thoại (Multi-turn Tool Switching: bỏ Twitter để tìm trên Web)           | `lookup(query="OpenAI", topic="news")` (không gọi lại tool mạng xã hội đã dùng trước đó) | Ở v2, agent dễ bị ảnh hưởng bởi ngữ cảnh trước và tiếp tục gọi công cụ đã sử dụng. Lên v3, bổ sung quy tắc "Tool Switching / Dropping", yêu cầu agent ngừng hoàn toàn tool cũ khi người dùng thay đổi yêu cầu và chỉ sử dụng công cụ mới. | Run v3 / Test case M06        |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

| Version | Prompt/tool change                   | Hypothesis                                                                                                                         | Metric name   | Before | After | Run File                                             |
| ------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ------------- | -----: | ----: | ---------------------------------------------------- |
| v0      | baseline (cấu hình khởi tạo ban đầu) | Test prompt và tool mặc định để đạt benchmark 14/20                                                                                | case_accuracy |   0.00 |  0.70 | runs/v0_B_base_openrouter_20260729T151336264806.json |
| v1      | system_prompt.md                     | Bổ sung routing và xử lý out-of-scope; phân biệt rõ các tool và từ chối câu hỏi không thuộc scope giúp tăng accuracy               | case_accuracy |   0.70 |  0.75 | runs/v1_B_base_openrouter_20260729T154809950796.json |
| v2      | system_prompt.md + tools.yaml        | Bắt buộc `response_type` và chuẩn hóa query `lookup` giúp sửa R10, R03                                                             | case_accuracy |   0.75 |  0.90 | runs/v2_B_base_openrouter_20260729T162820218051.json |
| v3      | system_prompt.md                     | Fix tool switching (M06) và ranh giới `clarify`; quy định ngừng gọi tool cũ khi bỏ Twitter, bắt buộc confirm yes_no giúp đạt 20/20 | case_accuracy |   0.90 |  1.00 | runs/v3_B_base_openrouter_20260729T163838890677.json |

**Ghi chú thêm (v5 — cải tiến sau khi đạt điểm tuyệt đối, ngoài phạm vi bảng chính thức của template):**

- Thay đổi: `system_prompt.md`, bổ sung Rule "Language & Output Formatting" (bắt buộc trả lời 100% Tiếng Việt) và Rule "Anti-Hallucination & Fact-Grounding Guardrails" (cấm bịa URL/handle/ID, bắt buộc trích dẫn nguồn, dùng `clarify` khi thiếu dữ liệu).
- Metric: case_accuracy giữ nguyên 1.00 nhưng siết chặt fact-grounding.

## B2. Failure analysis

> Gộp các case từ cả hai lần chạy thử nghiệm baseline v0.

| Case ID   | Failure Type                  | Actual Tool Calls (baseline v0)                                                                                                                                                           | What Failed                                                                                                                                                                                         | Fix (version)                                                                                                                                                                                          |
| --------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R08 / R14 | out_of_scope                  | Agent vẫn cố gắng tìm/gọi tool cho câu hỏi toán học, code Fibonacci                                                                                                                       | Không nhận diện được câu hỏi ngoài phạm vi research. Nguyên nhân: prompt cũ có chỉ thị _"Always finish the request in a single step. Pick one tool"_, ép agent luôn phải hành động thay vì từ chối. | v1: thêm Rule 1 (Scope & Non-Research Queries) vào `system_prompt.md` — định nghĩa rõ phạm vi Out of Scope (bao gồm cả toán học, lập trình), yêu cầu từ chối tuyệt đối                                 |
| R09       | unnecessary_tool              | Agent gọi tool cho câu hỏi meta "bạn là ai"                                                                                                                                               | Không phân biệt được câu hỏi meta không cần tool                                                                                                                                                    | v1: cùng Rule 1                                                                                                                                                                                        |
| R10 / R12 | missing_info / wrong_boundary | `clarify` được gọi nhưng thiếu tham số `response_type`; hoặc gọi `timeline` với handle tự đoán (vd Sam Altman) do prompt cũ chỉ đạo _"do not ask them back... pick a well-known account"_ | Tool `clarify` không ràng buộc kiểu phản hồi (text/yes_no) → agent hỏi lại sai form kỳ vọng; hoặc agent tự ý đoán bừa thông tin thay vì hỏi lại                                                     | v2: thêm `response_type` vào `required` của `clarify` trong `tools.yaml`, enum `[text, yes_no, choice]`; thêm luật MISSING INFO bắt buộc gọi clarify khi thiếu thông tin quan trọng                    |
| R11       | missing_info                  | Gọi `fetch` với URL giả định/bịa ra do prompt cũ chỉ đạo _"assume a likely URL and read it"_                                                                                              | Agent tự động giả định URL thay vì xin link từ người dùng                                                                                                                                           | v2: gỡ bỏ chỉ thị "assume a likely URL", yêu cầu agent bắt buộc dùng `clarify` để hỏi link cụ thể                                                                                                      |
| R03 / R06 | wrong_arg_value               | `lookup` được gọi với `query="tin tức AI"` dù đã có `topic="news"`                                                                                                                        | Agent ghép trùng từ khóa "tin tức"/"news" vào `query` gây trùng lặp                                                                                                                                 | v2: bổ sung Rule 3 (Lookup query rule) — `query` chỉ chứa keyword chính, không thêm "news"/"tin tức"                                                                                                   |
| R13       | wrong_tool                    | Chỉ gọi 1 tool (hoặc `lookup` hoặc `social_search`) dù câu lệnh yêu cầu tìm 2 nguồn độc lập, do prompt cũ giới hạn cứng _"Pick one tool"_                                                 | Agent không thể gọi song song nhiều tool khi cần thiết                                                                                                                                              | v2/v3: xóa bỏ dòng "Pick one tool", bổ sung luật PARALLEL TOOLS cho phép và khuyến khích gọi đồng thời nhiều tool khi cần                                                                              |
| M06       | wrong_tool                    | Agent vẫn gọi lại `social_search` dù user đã nói "bỏ Twitter, chuyển sang web"                                                                                                            | Không dừng hẳn tool cũ khi người dùng đổi ý (tool switching) trong hội thoại đa lượt                                                                                                                | v3: thêm Rule 4 (Multi-turn Carryover & Tool Switching/Dropping)                                                                                                                                       |
| R12 / G09 | wrong_boundary                | Ranh giới giữa `response_type="text"` và `"yes_no"` chưa rõ ràng; agent có thể gọi `send` trực tiếp do prompt cũ xúi giục _"When the user wants to send... just go ahead and do it"_      | Agent có thể gọi `send` trước khi xác nhận, hoặc dùng sai kiểu clarify                                                                                                                              | v3: cập nhật Rule 2 (Clarification & Confirmation Boundary) — phân định rõ text (thiếu input) vs yes_no (xác nhận hành động ghi/gửi), bắt buộc `clarify(response_type="yes_no")` trước khi dùng `send` |

## B3. Team eval cases

10 case do nhóm tự viết (`data/eval_group.json`) — 5 single-turn (G01–G05) + 5 multi-turn (G06–G10), tập trung vào 4 tool mới (`web_search`, `paper_search`, `summarize`, `keyword_extract`) và pipeline research → tổng hợp → gửi Telegram.

| Case ID                                    | What it tests                                                                                                         | Expected tool/behavior                                     | Result                                                                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `G01_web_search_routing`                   | Tìm kiếm thông tin chung trên web khi chưa có URL cụ thể; agent phải chọn `web_search` thay vì `lookup` hoặc `fetch`. | Gọi `web_search`                                           | Tránh `wrong_tool`; tham số: `{"query": "giá vé máy bay Tết 2026"}`                                                       |
| `G02_paper_search_routing`                 | Tìm kiếm bài báo khoa học; agent phải chọn `paper_search` thay vì `web_search` hoặc `lookup`.                         | Gọi `paper_search`                                         | Tránh `wrong_tool`; tham số: `{"query": "reinforcement learning from human feedback"}`                                    |
| `G03_summarize_arg_value`                  | Người dùng yêu cầu tóm tắt đúng 2 câu; `max_sentences` phải bằng 2 thay vì giá trị mặc định.                          | Gọi `summarize`                                            | Tránh `wrong_arg_value`; tham số: `{"max_sentences": 2}`                                                                  |
| `G04_keyword_extract_routing`              | Người dùng yêu cầu trích xuất từ khóa từ một đoạn văn bản; phải dùng `keyword_extract` thay vì `summarize`.           | Gọi `keyword_extract`                                      | Tránh `wrong_tool`; tool không cần tham số đầu vào.                                                                       |
| `G05_out_of_scope_math`                    | Yêu cầu giải toán nằm ngoài phạm vi của research agent; không được gọi bất kỳ tool nào.                               | Không gọi tool (`no_tool`); hành vi: `refuse`              | Tránh `out_of_scope`; từ chối hoặc định hướng lại một cách phù hợp.                                                       |
| `G06_multi_fetch_then_summarize`           | Sau khi đã `fetch` ở lượt trước, người dùng yêu cầu tóm tắt; agent chỉ gọi `summarize`, không `fetch` lại.            | Gọi `summarize`                                            | Tránh `wrong_tool`; tham số: `{"max_sentences": 3}`                                                                       |
| `G07_multi_fetch_then_keyword_extract`     | Sau khi đã `fetch`, người dùng yêu cầu trích xuất từ khóa; phải dùng `keyword_extract` thay vì `summarize`.           | Gọi `keyword_extract`                                      | Tránh `wrong_tool`; tool không cần tham số đầu vào.                                                                       |
| `G08_multi_missing_info_then_paper_search` | Ban đầu thiếu thông tin về chủ đề, sau khi người dùng bổ sung mới thực hiện tìm kiếm bài báo.                         | Gọi `paper_search`                                         | Tránh `missing_info`; tham số: `{"query": "diffusion models in image generation"}`                                        |
| `G09_multi_confirm_before_send`            | Chỉ gọi `send` sau khi người dùng xác nhận "gửi luôn đi"; không được gửi trước khi có xác nhận.                       | Gọi `send`                                                 | Tránh `wrong_boundary`; tham số: `{"confirmed": true}`. Đã test thật: agent research xong và gửi thành công qua Telegram. |
| `G10_multi_unnecessary_tool_meta`          | Câu hỏi meta về khả năng của agent; trả lời trực tiếp, không gọi tool không cần thiết.                                | Không gọi tool (`no_tool`); hành vi: `answer_without_tool` | Tránh `unnecessary_tool`; trả lời trực tiếp bằng văn bản.                                                                 |

## B4. Live chat evidence

| Scenario/Turn                              | Version | Tool Calls + Args                                                                                        | Transcript/Run                                           | Outcome                                                                                                                   |
| ------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Câu hỏi toán học (Out-of-scope) / Lượt 1   | v3      | `no_tool`                                                                                                | `transcripts/math_fallback.transcript.json`              | Agent lịch sự từ chối giải phương trình/tích phân và giải thích rõ giới hạn phạm vi là tra cứu thông tin (Research).      |
| Xin xác nhận trước khi gửi / Lượt 2        | v3      | `clarify(question="Bạn có chắc chắn muốn gửi nội dung này qua Telegram không?", response_type="yes_no")` | `transcripts/telegram_confirm.transcript.json`           | Agent chặn lại hành động `send`, gọi `clarify` đúng chuẩn với `yes_no`. Chờ người dùng "Ok" mới gửi.                      |
| Thiếu thông tin tra cứu / Lượt 1           | v3      | `clarify(question="Bạn muốn tìm bài báo về chủ đề/lĩnh vực cụ thể nào?", response_type="text")`          | `transcripts/missing_paper_query.transcript.json`        | Agent không tự bịa từ khóa, dùng `clarify` loại `text` để hỏi lại đúng ý định của người dùng.                             |
| Đổi ý giữa chừng (Tool Switching) / Lượt 2 | v3      | `lookup(query="OpenAI", topic="news")`                                                                   | `transcripts/tool_switch_twitter_to_web.transcript.json` | Người dùng bảo "Bỏ Twitter đi, tìm trên web", agent lập tức ngừng gọi `social_search` và chuyển sang `lookup` thành công. |

## B5. Tool capability evidence

> Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng. UI là core deliverable, không phải bonus, nên không liệt kê ở đây.

| Category                                                       | Evidence file                              | What worked                                                                                                                                                  | Risk / Guardrail                                                                                                                                                                               |
| -------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Must-have: Tool mới đầu tiên (`web_search`, `paper_search`)    | `data/eval_group.json`, `tools.yaml`       | Định tuyến chính xác giữa tìm kiếm thông tin trên web và tìm kiếm bài báo khoa học, giúp agent lựa chọn đúng công cụ và thu thập được nguồn dữ liệu phù hợp. | **Risk:** LLM có thể sinh DOI hoặc URL không tồn tại. **Guardrail:** chỉ cho phép truyền `query` dưới dạng từ khóa thay vì URL; giới hạn số lượng kết quả thông qua `max_results`.             |
| Optional built-in (`clarify`, `lookup`)                        | `artifacts/system_prompt.md`, `tools.yaml` | `clarify` giúp xử lý tốt các trường hợp cần xác nhận khi có `response_type`; `lookup` chuẩn hóa truy vấn và loại bỏ các từ khóa dư thừa trước khi tìm kiếm.  | **Risk:** agent hỏi xác nhận lặp lại hoặc sử dụng sai kiểu phản hồi. **Guardrail:** ràng buộc `response_type` bằng `enum` (`text`, `yes_no`) và mô tả rõ từng trường hợp sử dụng trong prompt. |
| Bonus: Tool mới thứ tư trở đi (`summarize`, `keyword_extract`) | `data/eval_group.json`, `tools.yaml`       | Hỗ trợ xử lý văn bản sau khi thu thập dữ liệu; `summarize` tạo tóm tắt đúng số câu yêu cầu và `keyword_extract` trích xuất các từ khóa chính từ nội dung.    | **Risk:** LLM tóm tắt dựa trên kiến thức nội tại thay vì nội dung đầu vào. **Guardrail:** prompt yêu cầu thực hiện _extractive summarization_, chỉ sử dụng thông tin có trong tham số `text`.  |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  Các thay đổi liên quan đến hành vi của agent và quy tắc ra quyết định (behavioral rules) nên được đặt trong `system_prompt.md`, vì chỉ khai báo schema tool không đủ để xử lý các quy tắc "khi nào không nên gọi tool" hoặc "cách carry context qua nhiều lượt". Bao gồm:
    - Quy định phạm vi hoạt động (Scope & Non-Research Queries) — từ chối các yêu cầu ngoài phạm vi như giải toán hoặc viết code (v1).
    - Chuẩn hóa truy vấn `lookup` — không ghép từ "news"/"tin tức" vào `query` khi đã có `topic` (v2).
    - Thiết lập ranh giới xác nhận (Clarification & Confirmation Boundary) — phân định rõ `response_type` text (thiếu input) vs yes_no (xác nhận hành động ghi/gửi) (v3).
    - Bổ sung quy tắc chuyển đổi công cụ trong hội thoại nhiều lượt (Multi-turn Carryover & Tool Switching/Dropping) khi người dùng thay đổi yêu cầu (v3).
    - Rule ngôn ngữ và chống bịa đặt (Language & Anti-Hallucination Guardrails) — bắt buộc trả lời tiếng Việt, cấm bịa URL/handle/ID, bắt buộc trích dẫn nguồn (v5).

- **Which fixes belonged in `tools.yaml`?**
  Các thay đổi liên quan đến schema và ràng buộc tham số nên được đặt trong `tools.yaml`. Bao gồm:
    - Khai báo trường bắt buộc `response_type` trong tool `clarify` (v2), tránh agent tự sáng tạo giá trị không hợp lệ.
    - Ràng buộc các giá trị hợp lệ bằng `enum` (`text`, `yes_no`, `choice`).
    - Bổ sung mô tả chi tiết cho từng tham số nhằm hướng dẫn LLM truyền dữ liệu đúng định dạng, chẳng hạn không đưa từ "news" vào `query` khi `topic="news"`.

- **Which failure needed manual review instead of automatic grading?**
  Các case liên quan đến `tool_results` có lỗi (do provider hoặc dữ liệu mock) cần review thủ công, vì routing PASS (gọi đúng tool) không đảm bảo tool execution đã trả về đúng dữ liệu thực tế — đúng như điều kiện metric hợp lệ đã nêu ở đầu Phần B. Cụ thể:
    - Tool được gọi đúng nhưng dữ liệu trả về là trang lỗi (404) hoặc nội dung không hợp lệ.
    - Tool `summarize` được gọi đúng nhưng bản tóm tắt làm sai lệch ý nghĩa của văn bản gốc (hallucination).

    Hệ thống chấm điểm tự động chủ yếu kiểm tra việc lựa chọn tool và tham số đầu vào, trong khi chất lượng nội dung đầu ra vẫn cần được đánh giá thủ công.

- **What would you improve next?**
    1. Ranh giới công cụ (Tool Boundaries): khai báo schema là chưa đủ, cần behavioral rules rõ ràng trong system prompt để agent biết khi nào KHÔNG nên gọi tool.
    2. Multi-turn Context Persistence: trong hội thoại nhiều lượt, agent dễ "dính bẫy" lặp lại tool cũ; cần rule tường minh chỉ đạo việc drop/abandon tool cũ khi intent thay đổi.
    3. Strict Enums: bắt buộc tham số điều hướng như `response_type` giúp tránh LLM tự sáng tạo giá trị không hợp lệ.
    4. Cải thiện xử lý lỗi: bổ sung cơ chế fallback để agent tự động chuyển sang công cụ hoặc nguồn dữ liệu khác khi một API trả về lỗi hoặc hết thời gian chờ.
    5. Quản lý ngữ cảnh: áp dụng cơ chế chunking hoặc rút gọn nội dung khi kết hợp nhiều nguồn dữ liệu nhằm tránh vượt quá giới hạn token trong các cuộc hội thoại dài.
    6. Tiếp tục siết chặt fact-grounding (v5): đảm bảo mọi số liệu, trích dẫn, URL trong output đều xuất phát từ dữ liệu tool trả về, không bịa đặt.
