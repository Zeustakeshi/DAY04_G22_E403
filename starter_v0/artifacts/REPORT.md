# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 16:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: G22
- Members:

| STT | Họ và tên            | Mã học viên |
|:---:|----------------------|-------------|
| 1   | Đặng Nguyên Giáp     | 2A202601486 |
| 2   | Mai Tuấn Quang       | 2A202601484 |
| 3   | Nguyễn Thị Thu Trang | 2A202601172 |
| 4   | Phạm Minh Hiếu       | 2A202601562 |
| 5   | Hoàng Thị Thuyên     | 2A202601910 |
| 6   | Dương Tiến Dũng      | 2A202602020 |
| 7   | Đặng Quang Trung     | 2A202601510 |


- Provider/model: Openrouter

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì.

Research agent: Chuyên tìm kiếm thông tin tổng hợp trên web, tài liệu học thuật và mạng xã hội, sau đó đọc hiểu URL, tóm tắt nội dung cốt lõi và định dạng thành báo cáo để gửi qua Telegram.

**Link dùng thử (truy cập được trong showdown):**

> Dán public URL nếu người khác cần mở từ máy riêng; localhost cũng được nếu demo trực tiếp trên máy trình chiếu. Streamlit được khuyến nghị, nhưng nhóm có thể dùng bất kỳ framework nào.
>
> URL: [http://localhost:8000](http://localhost:8000)

## A2. Tool agent có

> Liệt kê các tool agent đang dùng. Mỗi tool 1 dòng: tên + làm được gì.


| Tên tool | Làm được gì | Tool mới nhóm thêm? |
| --- | --- | --- |
| clarify | Hỏi lại người dùng thông tin còn thiếu hoặc xin xác nhận trước khi thực hiện hành động. | không |
| timeline | Lấy các bài đăng gần đây của một tài khoản Twitter/X. Dùng duy nhất khi biết cụ thể tài khoản/handle. | không |
| social_search | Tìm kiếm các bài đăng trên mạng xã hội Twitter/X theo chủ đề hoặc từ khóa. | không |
| lookup | Tra cứu thông tin tin tức hoặc tìm kiếm trên internet. | không |
| fetch | Đọc nội dung từ một địa chỉ URL. | không |
| format | Trình bày dữ liệu đã có thành văn bản. | không |
| send | Gửi một đoạn văn bản lên Telegram. | không |
| policy | Tìm trong tài liệu nội bộ. | không |
| papers | Tìm bài báo khoa học. | không |
| paper_text | Lấy nội dung text của một bài báo. | không |
| web_search | Tìm kiếm trên web (DuckDuckGo, không cần API key) khi chưa có URL cụ thể. Không dùng khi đã có link (fetch) hoặc khi cần bài báo khoa học (paper_search). | có |
| paper_search | Tìm bài báo khoa học trực tiếp trên arXiv (không cần API key). Dùng khi người dùng muốn tài liệu/paper học thuật, không dùng cho tin tức hay web thường. | có |
| summarize | Tóm tắt trích xuất (extractive) một đoạn văn bản dài (thường là kết quả fetch) thành các câu chính. Dùng sau khi đã fetch/có văn bản dài, trước khi format/send. | có |
| keyword_extract | Rút ra các từ khóa quan trọng nhất từ một đoạn văn bản. Dùng khi người dùng hỏi về chủ đề chính/từ khóa/thuật ngữ quan trọng của nội dung đã có. | có |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm giúp mình vài bài báo khoa học về reinforcement learning from human feedback.
2. Tìm trên web tin tức AI hôm nay, tóm tắt rồi gửi qua Telegram giúp mình.
3. Tóm tắt đoạn văn bản này thành đúng 2 câu chính: 'OpenAI released GPT-5 today. It brings major improvements in reasoning. The model is also faster than before. Many developers are excited about new API features.

## A4. Kịch bản demo đã rehearse

> Chuẩn bị 3–5 scenario. Mỗi scenario cần cho thấy tool đã làm gì và một thay đổi cụ thể giữa các version.

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
| --- | --- | --- | --- |
| 1. Câu hỏi toán học / Out-of-scope (vd: tính tích phân, viết code Fibonacci, câu hỏi meta) | Không gọi tool nào (từ chối hoặc trả lời trực tiếp) | Ở v0, agent vẫn cố gắng tìm kiếm công cụ hoặc gọi tool không phù hợp. Lên v1, nhờ bổ sung quy tắc "Scope & Non-Research Queries", agent đã biết trả lời trực tiếp mà không gọi tool. | Run v1 / Non-research queries |
| 2. Tìm kiếm tin tức (xử lý lỗi ghép thừa từ khóa) | `lookup(query="AI", topic="news")` | Ở v0/v1, khi tìm tin tức, agent ghép cả cụm "tin tức AI" vào tham số `query`. Lên v2, bổ sung quy tắc không đưa từ "news" hoặc "tin tức" vào `query` khi `topic="news"`, giúp trích xuất truy vấn chính xác hơn. | Run v2 / Test case R03, R10 |
| 3. Xin xác nhận trước khi thực hiện hành động (vd: ghi hoặc gửi tin nhắn qua Telegram) | `clarify(question="...", response_type="yes_no")` | Ở v0/v1, tool `clarify` chưa có tham số ràng buộc kiểu phản hồi. Lên v2 và v3, `tools.yaml` bổ sung trường bắt buộc `response_type`, đồng thời prompt quy định rõ phải sử dụng `yes_no` khi cần xác nhận hành động. | Run v2, v3 |
| 4. Đổi ý trong hội thoại (Multi-turn Tool Switching: bỏ Twitter để tìm trên Web) | `lookup(query="OpenAI", topic="news")` (không gọi lại tool mạng xã hội đã dùng trước đó) | Ở v2, agent dễ bị ảnh hưởng bởi ngữ cảnh trước và tiếp tục gọi công cụ đã sử dụng. Lên v3, bổ sung quy tắc "Tool Switching / Dropping", yêu cầu agent ngừng hoàn toàn tool cũ khi người dùng thay đổi yêu cầu và chỉ sử dụng công cụ mới. | Run v3 / Test case M06 |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run file |
| --- | --- | --- | --- | ---: | ---: | --- |
| v0 | Baseline | Prompt mặc định kết hợp với định nghĩa tool cơ sở sẽ giúp agent đạt khoảng 70% độ chính xác. | `case_accuracy` | 0.00 | 0.70 | `runs/v0_B_base_openrouter_20260729T151336264806.json` |
| v1 | `system_prompt.md` | Bổ sung hướng dẫn phân biệt chức năng của từng tool và quy tắc xử lý câu hỏi ngoài phạm vi sẽ giảm số lần gọi tool không cần thiết và cải thiện độ chính xác. | `case_accuracy` | 0.70 | 0.75 | `runs/v1_B_base_openrouter_20260729T154809950796.json` |
| v2 | `system_prompt.md` + `tools.yaml` | Cập nhật schema của tool (bắt buộc trường `response_type`) và chuẩn hóa truy vấn tìm kiếm tin tức sẽ khắc phục các lỗi ở test case R03 và R10. | `case_accuracy` | 0.75 | 0.90 | `runs/v2_B_base_openrouter_20260729T162820218051.json` |
| v3 | `system_prompt.md` | Bổ sung quy tắc chuyển đổi công cụ trong hội thoại nhiều lượt (Multi-turn Tool Switching) và làm rõ cách sử dụng `clarify`, giúp agent đạt độ chính xác tối đa trên bộ kiểm thử. | `case_accuracy` | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20260729T163838890677.json` |

## B2. Failure analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | Cố gắng trả lời trực tiếp hoặc gọi tool bất kỳ (ví dụ: `lookup`). | Agent không từ chối câu hỏi toán học. Nguyên nhân do prompt cũ có chỉ thị: *"Always finish the request in a single step. Pick one tool"*, ép agent luôn phải hành động thay vì từ chối (`no_tool`). | Cập nhật Prompt: Định nghĩa rõ phạm vi (Out of Scope). Hướng dẫn Agent bắt buộc từ chối lịch sự và KHÔNG gọi tool đối với các yêu cầu toán học, vật lý. |
| R10_missing_handle | missing_info | Gọi `timeline` với một handle tự đoán (như Sam Altman). | Thiếu handle nhưng Agent không hỏi lại người dùng, tự ý đoán bừa thông tin do bị ảnh hưởng bởi câu: *"do not ask them back... pick a well-known account"*. | Cập nhật Prompt: Thêm luật `MISSING INFO`, bắt buộc gọi tool `clarify` (response_type: text) khi thiếu thông tin quan trọng như tên người dùng. |
| R11_missing_url | missing_info | Gọi `fetch` với URL giả định/bịa ra. | Agent tự động giả định URL thay vì xin link từ người dùng vì prompt cũ chỉ đạo: *"assume a likely URL and read it"*. | Cập nhật Prompt: Gỡ bỏ chỉ thị "assume a likely URL". Yêu cầu Agent bắt buộc dùng `clarify` để hỏi link cụ thể. |
| R12_confirm_before_send | wrong_boundary | Gọi trực tiếp tool `send`. | Agent vi phạm ranh giới an toàn (boundary) khi tự ý gửi tin mà không xác nhận, do prompt cũ xúi giục: *"When the user wants to send... just go ahead and do it"*. | Cập nhật Prompt: Thêm luật `CONFIRMATION BOUNDARY`, bắt buộc Agent gọi `clarify` (với response_type: yes_no) để xác nhận trước khi dùng tool `send`. |
| R13_parallel_web_and_tweets | wrong_tool | Chỉ gọi 1 tool (hoặc `lookup` hoặc `social_search`). | Câu lệnh yêu cầu tìm 2 nguồn độc lập nhưng Agent chỉ chọn 1 tool do prompt cũ giới hạn cứng: *"Pick one tool"*. | Cập nhật Prompt: Xóa bỏ dòng "Pick one tool". Bổ sung luật `PARALLEL TOOLS`, cho phép và khuyến khích gọi đồng thời nhiều tool khi cần thiết. |
| R14_out_of_scope_coding | out_of_scope | Cố gắng viết code Fibonacci trực tiếp hoặc gọi tool tìm kiếm. | Agent không nhận diện được yêu cầu lập trình nằm ngoài phạm vi năng lực (Research/News Agent) nên không chịu từ chối (`no_tool`). | Cập nhật Prompt: Đưa rõ các tác vụ viết code/lập trình (coding tasks) vào danh sách `OUT OF SCOPE` và yêu cầu từ chối tuyệt đối. |

## B3. Team eval cases

List the 10 cases added to `data/eval_group.json`:

- 5 single-turn
- 5 multi-turn

This section is for the mandatory team-authored eval set. Optional built-ins do
not belong here.

File template để trống có chủ đích; nhóm phải tự thiết kế đủ 10 case.

| Case ID | What it tests | Expected tool/behavior | Result |
| --- | --- | --- | --- |
| `G01_web_search_routing` | Tìm kiếm thông tin chung trên web khi chưa có URL cụ thể; agent phải chọn `web_search` thay vì `lookup` hoặc `fetch`. | Gọi `web_search` | Tránh `wrong_tool`; tham số: `{"query": "giá vé máy bay Tết 2026"}` |
| `G02_paper_search_routing` | Tìm kiếm bài báo khoa học; agent phải chọn `paper_search` thay vì `web_search` hoặc `lookup`. | Gọi `paper_search` | Tránh `wrong_tool`; tham số: `{"query": "reinforcement learning from human feedback"}` |
| `G03_summarize_arg_value` | Người dùng yêu cầu tóm tắt đúng 2 câu; `max_sentences` phải bằng 2 thay vì giá trị mặc định. | Gọi `summarize` | Tránh `wrong_arg_value`; tham số: `{"max_sentences": 2}` |
| `G04_keyword_extract_routing` | Người dùng yêu cầu trích xuất từ khóa từ một đoạn văn bản; phải dùng `keyword_extract` thay vì `summarize`. | Gọi `keyword_extract` | Tránh `wrong_tool`; tool không cần tham số đầu vào. |
| `G05_out_of_scope_math` | Yêu cầu giải toán nằm ngoài phạm vi của research agent; không được gọi bất kỳ tool nào. | Không gọi tool (`no_tool`); hành vi: `refuse` | Tránh `out_of_scope`; từ chối hoặc định hướng lại một cách phù hợp. |
| `G06_multi_fetch_then_summarize` | Sau khi đã `fetch` ở lượt trước, người dùng yêu cầu tóm tắt; agent chỉ gọi `summarize`, không `fetch` lại. | Gọi `summarize` | Tránh `wrong_tool`; tham số: `{"max_sentences": 3}` |
| `G07_multi_fetch_then_keyword_extract` | Sau khi đã `fetch`, người dùng yêu cầu trích xuất từ khóa; phải dùng `keyword_extract` thay vì `summarize`. | Gọi `keyword_extract` | Tránh `wrong_tool`; tool không cần tham số đầu vào. |
| `G08_multi_missing_info_then_paper_search` | Ban đầu thiếu thông tin về chủ đề, sau khi người dùng bổ sung mới thực hiện tìm kiếm bài báo. | Gọi `paper_search` | Tránh `missing_info`; tham số: `{"query": "diffusion models in image generation"}` |
| `G09_multi_confirm_before_send` | Chỉ gọi `send` sau khi người dùng xác nhận "gửi luôn đi"; không được gửi trước khi có xác nhận. | Gọi `send` | Tránh `wrong_boundary`; tham số: `{"confirmed": true}` |
| `G10_multi_unnecessary_tool_meta` | Câu hỏi meta về khả năng của agent; trả lời trực tiếp, không gọi tool không cần thiết. | Không gọi tool (`no_tool`); hành vi: `answer_without_tool` | Tránh `unnecessary_tool`; trả lời trực tiếp bằng văn bản. |


## B4. Live chat evidence

Use `transcripts/*.transcript.json`.

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
| --- | --- | --- | --- | --- |
| Câu hỏi toán học (Out-of-scope) / Lượt 1 | v3 | `no_tool` | `transcripts/math_fallback.transcript.json` | Agent lịch sự từ chối giải phương trình/tích phân và giải thích rõ giới hạn phạm vi là tra cứu thông tin (Research). |
| Xin xác nhận trước khi gửi / Lượt 2 | v3 | `clarify(question="Bạn có chắc chắn muốn gửi nội dung này qua Telegram không?", response_type="yes_no")` | `transcripts/telegram_confirm.transcript.json` | Agent chặn lại hành động `send`, gọi `clarify` đúng chuẩn với `yes_no`. Chờ người dùng "Ok" mới gửi. |
| Thiếu thông tin tra cứu / Lượt 1 | v3 | `clarify(question="Bạn muốn tìm bài báo về chủ đề/lĩnh vực cụ thể nào?", response_type="text")` | `transcripts/missing_paper_query.transcript.json` | Agent không tự bịa từ khóa, dùng `clarify` loại `text` để hỏi lại đúng ý định của người dùng. |
| Đổi ý giữa chừng (Tool Switching) / Lượt 2 | v3 | `lookup(query="OpenAI", topic="news")` | `transcripts/tool_switch_twitter_to_web.transcript.json` | Người dùng bảo "Bỏ Twitter đi, tìm trên web", agent lập tức ngừng gọi `social_search` và chuyển sang `lookup` thành công. |


## B5. Tool capability evidence

Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng.

UI is core deliverable, not bonus. Do not list it here.

| Category | Evidence file | What worked | Risk / Guardrail |
| --- | --- | --- | --- |
| Must-have: Tool mới đầu tiên (`web_search`, `paper_search`) | `data/eval_group.json`, `tools.yaml` | Định tuyến chính xác giữa tìm kiếm thông tin trên web và tìm kiếm bài báo khoa học, giúp agent lựa chọn đúng công cụ và thu thập được nguồn dữ liệu phù hợp. | **Risk:** LLM có thể sinh DOI hoặc URL không tồn tại. **Guardrail:** Chỉ cho phép truyền `query` dưới dạng từ khóa thay vì URL; giới hạn số lượng kết quả thông qua `max_results`. |
| Optional built-in (`clarify`, `lookup`) | `artifacts/system_prompt.md`, `tools.yaml` | `clarify` giúp xử lý tốt các trường hợp cần xác nhận khi có `response_type`; `lookup` chuẩn hóa truy vấn và loại bỏ các từ khóa dư thừa trước khi tìm kiếm. | **Risk:** Agent hỏi xác nhận lặp lại hoặc sử dụng sai kiểu phản hồi. **Guardrail:** Ràng buộc `response_type` bằng `enum` (`text`, `yes_no`) và mô tả rõ từng trường hợp sử dụng trong prompt. |
| Bonus: Tool mới thứ tư trở đi (`summarize`, `keyword_extract`) | `data/eval_group.json`, `tools.yaml` | Hỗ trợ xử lý văn bản sau khi thu thập dữ liệu; `summarize` tạo tóm tắt đúng số câu yêu cầu và `keyword_extract` trích xuất các từ khóa chính từ nội dung. | **Risk:** LLM tóm tắt dựa trên kiến thức nội tại thay vì nội dung đầu vào. **Guardrail:** Prompt yêu cầu thực hiện *extractive summarization*, chỉ sử dụng thông tin có trong tham số `text`. |

## B6. Reflection

### Which fixes belonged in `system_prompt.md`?

Các thay đổi liên quan đến hành vi của agent và quy tắc ra quyết định nên được đặt trong `system_prompt.md`. Bao gồm:
- Quy định phạm vi hoạt động (Scope), ví dụ từ chối các yêu cầu ngoài phạm vi như giải toán hoặc viết code.
- Thiết lập ranh giới xác nhận (Confirmation Boundary), xác định khi nào cần hỏi lại người dùng trước khi thực hiện hành động.
- Bổ sung quy tắc chuyển đổi công cụ trong hội thoại nhiều lượt (Multi-turn Tool Switching / Dropping) khi người dùng thay đổi yêu cầu.

### Which fixes belonged in `tools.yaml`?

Các thay đổi liên quan đến schema và ràng buộc tham số nên được đặt trong `tools.yaml`. Bao gồm:
- Khai báo các trường bắt buộc như `response_type`.
- Ràng buộc các giá trị hợp lệ bằng `enum` (ví dụ: `text`, `yes_no`, `choice`) để tránh sinh tham số không hợp lệ.
- Bổ sung mô tả chi tiết cho từng tham số nhằm hướng dẫn LLM truyền dữ liệu đúng định dạng, chẳng hạn không đưa từ `"news"` vào `query` khi `topic="news"`.

### Which failure needed manual review instead of automatic grading?

Một số trường hợp cần đánh giá thủ công dù hệ thống chấm điểm tự động báo đạt. Ví dụ:
- Tool được gọi đúng nhưng dữ liệu trả về là trang lỗi (404) hoặc nội dung không hợp lệ.
- Tool `summarize` được gọi đúng nhưng bản tóm tắt làm sai lệch ý nghĩa của văn bản gốc (hallucination).

Hệ thống chấm điểm tự động chủ yếu kiểm tra việc lựa chọn tool và tham số đầu vào, trong khi chất lượng nội dung đầu ra vẫn cần được đánh giá thủ công.

### What would you improve next?

- **Cải thiện xử lý lỗi:** Bổ sung cơ chế fallback để agent tự động chuyển sang công cụ hoặc nguồn dữ liệu khác khi một API trả về lỗi hoặc hết thời gian chờ.
- **Quản lý ngữ cảnh:** Áp dụng cơ chế chunking hoặc rút gọn nội dung khi kết hợp nhiều nguồn dữ liệu nhằm tránh vượt quá giới hạn token trong các cuộc hội thoại dài.
