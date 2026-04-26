# Book Voice & Style Guide

> Reference cho tất cả block-skills `book-*`, đặc biệt P4 (book-write) và P5/P6 (review/revise).
> **Standard:** voice của sách O'Reilly senior — expert peer review, không tutorial, không marketing.

## Voice

### Expert peer, không phải giáo viên
Giọng văn như senior engineer làm code review sâu cho đồng nghiệp — người đọc không phải học sinh. Không cần "Welcome!", không cần "In this chapter you will learn...".

**Tốt:**
> "The dispatcher's single responsibility is to route events to handlers without blocking. Everything else — retries, logging, fan-out — lives elsewhere. This separation is why the system scales."

**Xấu:**
> "Welcome to Chapter 5! In this chapter, we will learn about the dispatcher. The dispatcher is a very important component. Let's dive in!"

### Direct và opinionated

Dám nói: "This is clever because...", "This is the wrong abstraction for...", "The reason this exists is...". Không phòng thủ, không "it depends" khi có câu trả lời rõ ràng.

**Tốt:**
> "Storing the event queue in Redis was the wrong call. The team paid for a year in debugging race conditions before migrating to Postgres LISTEN/NOTIFY. The lesson isn't Redis vs Postgres — it's that at-most-once delivery semantics were a hidden assumption nobody owned."

**Xấu:**
> "There are multiple options for event queues. Some teams use Redis, while others prefer Postgres. Each has trade-offs depending on your use case."

### Không có filler

Mỗi câu phải TEACH something hoặc SET UP câu tiếp theo. Nếu câu nào bỏ đi không mất ý nghĩa → cắt.

**Câu filler điển hình cần cắt:**
- "As we will see..." (chỉ nói khi sắp nói xong)
- "It's important to note that..." (nếu quan trọng, nói thẳng)
- "In this section, we will discuss..." (heading đã nói rồi)
- "Before we dive in, let's review..." (viết tiếp đi)
- "That being said..." (thừa)

### Show the trade-offs

Không chỉ mô tả CÁI GÌ được xây. Giải thích cái gì KHÔNG được xây và VÌ SAO. "The road not taken" thường dạy nhiều hơn.

**Tốt:**
> "The team rejected a plugin system early. A plugin system would have been the obvious answer for extensibility, but it locks the team into a public API they can't change. Instead, extensibility lives inside the monolith through a compile-time feature registry. Slower to add a feature, but every feature stays in-tree and refactorable."

## Tone theo ngôn ngữ

### Tiếng Việt (default — `--lang vi`)

- Dùng "hệ thống" thay vì "the system" không cần thiết
- Technical terms giữ nguyên tiếng Anh: dispatcher, queue, handler, state machine, pipeline
- Không dịch forced: "async" không cần dịch thành "bất đồng bộ"
- Tone: chuyên gia Việt viết cho kỹ sư Việt. Không sáng sủa kiểu textbook, không bí hiểm kiểu academic.
- Avoid: "chúng ta sẽ tìm hiểu...", "trong chương này..."
- Prefer: đi thẳng vào vấn đề

### Tiếng Anh (`--lang en`)

- US English spelling (color, not colour)
- Technical neutrality — no "awesome", "amazing", "super cool"
- Active voice preferred
- Sentences under 30 words when possible

## Code Block Rules

### Quy tắc vàng: **Pseudocode only, never verbatim**

P7 audit phase sẽ catch vi phạm này. Tốt hơn là tuân thủ từ đầu.

#### Bắt buộc:
1. **Variable renaming** — `config_manager` → `configRegistry`, `HandlerImpl` → `Dispatcher`
2. **Comment labels** — mỗi block bắt đầu bằng `// Pseudocode — illustrates the <pattern>` hoặc `// Simplified for clarity`
3. **Length** — 5-15 dòng mỗi block, 3-5 blocks/chapter max
4. **Context sandwich** — 1 câu trước (WHAT block này show), 1 đoạn sau (WHY pattern này matter)

#### Cấm:
- Copy-paste function signature y hệt source
- Giữ nguyên string constants từ source (prompt text, regex patterns, magic numbers)
- Giữ nguyên struct/class tên trùng 100% với source
- Code block dài > 20 dòng (người đọc nhảy qua)

### Example

**Source code (KHÔNG được viết như thế này):**
```python
class AnthropicClient:
    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com"):
        self.api_key = api_key
        self.base_url = base_url
    
    def messages_create(self, model: str, max_tokens: int, messages: list, ...):
        response = requests.post(f"{self.base_url}/v1/messages", ...)
        return response.json()
```

**Pseudocode (ĐƯỢC viết như thế này):**
```python
# Pseudocode — illustrates the client wrapper pattern
class ApiClient:
    def __init__(self, credentials, endpoint):
        self._auth = credentials
        self._endpoint = endpoint
    
    def send(self, request):
        # retry + auth + serialization handled here
        return self._transport.post(self._endpoint, request)
```

Sau đó câu giải thích: *"Client wrapper tập trung 3 concern — auth, retry, serialization — vào một surface duy nhất. Phần còn lại của codebase không biết transport layer có tồn tại, giúp sau này thay HTTPS bằng gRPC không cần đổi call site."*

## Diagrams

Xem `diagram-types.md` để biết khi nào dùng diagram loại nào.

**Quy tắc chung:**
- 2-4 diagrams / chapter (nhiều hơn cho chapter phức tạp như core loop, tools; ít hơn cho chapter focused)
- Mọi concept kiến trúc đều có diagram: data flow, state machines, decision trees, timelines, component relationships
- Mermaid format — render native trên GitHub và mọi web framework

## "Apply This" — Closing section của mỗi chapter

**Exactly 5 transferable patterns**, structured như sau:

```markdown
## Apply This

### 1. <Pattern Name>
**Problem it solves:** <1 câu>
**How to adapt:** <1-2 câu — cụ thể đủ để act on, abstract đủ để transfer>
**Pitfall to watch for:** <1 câu — cái mà team hay bị sai>

### 2. ...

### 3. ...

### 4. ...

### 5. ...
```

**Varying format:** Không phải chapter nào cũng dùng exact header này. Vary giữa các chapter:
- Chapter A dùng `### 1. <Name> — <problem>` (inline)
- Chapter B dùng `**Pattern:** ... / **When:** ... / **Trap:** ...`
- Chapter C dùng bullet list với bold keywords

Mục đích: 5 patterns standardized về CONTENT, varied về FORM để không monotonous.

## Cross-References

### Backward reference (mandatory)
Mỗi chapter MỞ ĐẦU với một câu/đoạn nối về chapter trước:

> "Chapter 4 showed how events enter the queue. This chapter follows what happens after the dispatcher picks one up."

### Forward reference (optional)
Khi giới thiệu concept sẽ expand sau:

> "Retries use exponential backoff with jitter — Chapter 9 covers the failure model in depth."

### Canonical home
Mỗi concept có MỘT chapter là "home" — các chapter khác reference, không re-explain.

## Consistency Anti-Patterns (cần tránh)

| Anti-pattern | Ví dụ | Fix |
|---|---|---|
| Repeated rhetorical phrases | "At its core, X is..." xuất hiện 5 chapter | Mỗi phrase dùng tối đa 2 lần toàn sách |
| Exact version/file counts | "There are 1,884 files in the src/ directory" | "The codebase is large — roughly 2000 files" |
| Marketing language | "Elegant", "powerful", "robust", "seamless" | Direct description thay thế |
| Apologetic hedging | "This is a bit tricky...", "You might be wondering..." | Cắt toàn bộ |
| Textbook transitions | "Now that we've covered X, let's move on to Y" | Header tự nhiên chuyển chủ đề |

## Chapter Length Checklist

- [ ] Chapter 300-800 lines?
- [ ] Opening 2-3 paragraphs với backward reference?
- [ ] 2-4 diagrams (Mermaid)?
- [ ] 3-5 pseudocode blocks, mỗi block 5-15 dòng?
- [ ] Apply This với exactly 5 patterns?
- [ ] Không có verbatim source code?
- [ ] Không có filler sentence nào?
- [ ] Mỗi concept có canonical home rõ ràng?
