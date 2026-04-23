---
name: chat-extract
description: Process messaging app exports (WhatsApp, Zalo, Viber) into structured business assets. Extract decisions, recurring patterns, SOPs, Galaxy candidates, and action items from exported conversations. Triggers on "whatsapp", "zalo", "viber", "extract chat", "process chat", "import chat", "tin nhắn", or when pointing at WhatsApp-Imports, Zalo-Imports, or Viber-Imports folders.
---

# Chat Extract — Turn Messaging History into Vault Assets

Convert exported WhatsApp/Zalo/Viber conversations into structured, routable knowledge following THỊNH pipeline.

## When to Use

- After dropping exports into `0_Inbox/WhatsApp-Imports/`, `0_Inbox/Zalo-Imports/`, or `0_Inbox/Viber-Imports/`
- When extracting business context from any messaging app export
- Priority channels: Zalo (VN partners, Viettel, HD128), WhatsApp (international), Viber (some VN contacts)

## Input

User provides path to exported chat folder or file. Default locations:
- `0_Inbox/WhatsApp-Imports/`
- `0_Inbox/Zalo-Imports/`
- `0_Inbox/Viber-Imports/`

If no path specified, scan all three folders for unprocessed items.

## Workflow

### Step 1: Detect Platform & Parse Chat Format

Auto-detect platform from folder location or file format:

**WhatsApp** export format:
```
[DD/MM/YYYY, HH:MM:SS] Contact Name: Message text
[DD/MM/YYYY, HH:MM:SS] Contact Name: <Media omitted>
```
- Media: IMG-*.jpg, VID-*.mp4, DOC-*.pdf, PTT-*.opus (voice notes)
- Export: **Mobile only** (Android: ⋮ → Thêm → Xuất cuộc trò chuyện; iOS: tap tên → Export Chat)
- Desktop workaround: Select messages → copy → paste vào _chat.txt

**Zalo** — KHÔNG có Export Chat (cả mobile lẫn PC). Capture thủ công:
- Copy-paste tin nhắn từ Zalo PC vào `_chat.txt`
- Download files qua tab "File" trong chat
- Format tự do (không chuẩn hóa như WhatsApp)
- Dùng "Đánh dấu tin quan trọng" để flag trước khi copy
- Media: lưu vào files/ subfolder

**Viber** export format:
```
Date: DD/MM/YYYY
HH:MM - Contact Name: Message text
HH:MM - Contact Name: [Photo] / [Video] / [File]
```
- Media: Viber Images/, Viber Videos/, Viber Files/ subfolders
- Export: Chat → ⋮ → Xuất cuộc trò chuyện (Export chat) → Email/Save
- Viber exports bao gồm cả media trong .zip

**Fallback:** Nếu format không khớp chính xác, đọc nội dung và infer structure từ patterns (timestamps, names, message boundaries).

Extract:
- **Platform** — WhatsApp / Zalo / Viber
- **Participants** — list all unique contacts
- **Date range** — first message to last message
- **Message count** — total messages per participant
- **Media inventory** — images, PDFs, voice notes, videos, files
- **Language** — Vietnamese/English/mixed

Present summary to CEO before proceeding.

### Step 2: Identify Chat Context

Ask CEO (if not obvious from content):
1. Chat type: **Client** / **Partner** / **Team** / **Supplier** / **Government**
2. Related project: link to `1_Projects/` if applicable
3. Priority: **HIGH** (active project, blocking) / **MEDIUM** (useful context) / **LOW** (archive)

### Step 3: Extract Signals

Scan entire conversation for these signal types:

**A. Decisions Made** (highest value)
- Statements like "OK let's go with...", "Đồng ý phương án...", "Approved", "Duyệt"
- Who decided, when, what context
- Extract rationale if available

**B. Recurring Patterns** (SOP candidates)
- Questions asked more than once → FAQ candidate
- Same explanation given to multiple people → Training doc candidate
- Same process described repeatedly → SOP candidate
- Flag: "This pattern appeared N times across M weeks"

**C. Technical Specifications** (design context)
- Numbers, dimensions, materials, part numbers
- Requirement changes or clarifications
- Test results shared informally

**D. Action Items** (operational)
- Statements like "Anh gửi cho em...", "Please send...", "Deadline is..."
- Check: was the action completed later in the chat?

**E. Relationship Signals** (BRIDGE)
- Tone shifts, frustrations, praise
- Commitments made by either party
- Trust-building or trust-eroding moments

**F. Galaxy Candidates** (atomic insights)
- Statements that reveal a principle, law, or hard-won lesson
- "Lần trước mình làm X thì bị Y" → potential Galaxy note
- Must pass 3-question gate: changes design? changes strategy? warns about trap?

### Step 4: Generate Signal Report

```markdown
## Chat Signal Report
**Platform:** [WhatsApp / Zalo / Viber]
**Chat:** [folder name]
**Participants:** [names]
**Date range:** YYYY-MM-DD → YYYY-MM-DD
**Messages:** [count] | **Media:** [count images, PDFs, voice notes]
**Related project:** [if any]

### Decisions (N items)
| # | Decision | Who | When | Rationale |
|---|----------|-----|------|-----------|

### Recurring Patterns → SOP/FAQ Candidates (N items)
| # | Pattern | Occurrences | Suggested Asset Type |
|---|---------|-------------|---------------------|

### Technical Specs (N items)
| # | Spec/Requirement | Context | Route To |
|---|------------------|---------|----------|

### Action Items (N items — M completed, K pending)
| # | Action | Owner | Status | Deadline |
|---|--------|-------|--------|----------|

### Relationship Signals (N items)
| # | Signal | Type | Severity |
|---|--------|------|----------|

### Galaxy Candidates (N items)
| # | Insight | Why Galaxy-worthy | Suggested Title |
|---|---------|-------------------|-----------------|
```

### Step 5: CEO Validation (MANDATORY)

Present Signal Report. CEO reviews and decides:
- Which decisions to log → `_meta/decisions.md`
- Which patterns to formalize → `3_Resources/SOPs/` or project docs
- Which specs to update → project Requirements List
- Which action items to track → project `Status.md`
- Which insights to promote → Galaxy (via `/galaxy-gate`)
- What to discard

NEVER auto-route without CEO validation.

### Step 6: Route and Archive

After CEO approval:
1. Create approved assets in their destinations
2. Move processed chat folder → `4_Archives/Chat-Processed/[platform]-[folder-name]/`
3. Keep original export intact in archive (never delete raw data)
4. Log extraction in `_meta/learnings.md`:
   ```
   [DATE] WhatsApp extract [chat-name]: N decisions, M SOP candidates, K Galaxy candidates
   ```

## Voice Notes & Media

Voice notes per platform:
- **WhatsApp:** `.opus` files (PTT-*.opus)
- **Zalo:** `.m4a` files trong subfolder riêng
- **Viber:** `.m4a` hoặc `.ogg` trong Viber Audio/

If voice/audio files exist:
- Flag to CEO: "N voice notes found — transcribe?"
- If yes: use available transcription (Tana/StenoAI/manual)
- Voice notes often contain richest context — prioritize these

Images/PDFs per platform:
- **WhatsApp:** IMG-*, DOC-*, VID-* prefixed files
- **Zalo:** photos/, files/ subfolders
- **Viber:** Viber Images/, Viber Files/ subfolders
- Flag technical drawings, contracts, specs for routing to project docs

## Integration Points

- Feeds into: `bridge-signal-extract` (same output format)
- Feeds into: `bridge-knowledge-base` (KB Layer 2 product knowledge)
- Feeds into: `bridge-risk-radar` (relationship risk flags)
- Feeds into: Galaxy (via `/galaxy-gate` for qualifying insights)
- Feeds into: Project `Status.md` (action items, decisions)

## COD Classification

- Parsing and extraction: **Offload** (AI)
- Validation and routing decisions: **Core** (CEO judgment)
- Archiving processed chats: **Default** (automate)
