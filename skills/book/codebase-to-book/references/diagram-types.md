# Mermaid Diagram Types — Reference

> Hướng dẫn khi nào dùng loại diagram nào trong sách kỹ thuật. Mọi diagram dùng Mermaid format (```mermaid fenced code blocks) — render native trên GitHub và hầu hết web framework.

## Decision: Khi nào dùng loại nào?

| Concept to show | Diagram type | Example use |
|---|---|---|
| Component / module relationships | `graph TD` or `graph LR` | "System architecture overview" |
| Data flow through pipeline | `graph LR` with labels on edges | "How a request moves through layers" |
| State transitions over time | `stateDiagram-v2` | "Connection state machine" |
| Request/response + actors | `sequenceDiagram` | "Auth handshake lifecycle" |
| Decision tree / pipeline with branches | `flowchart TD` | "Retry decision logic" |
| Timeline / parallel execution | `gantt` | "Build phases over time" |
| Nested hierarchy / call tree | `graph TD` + subgraphs | "Handler invocation tree" |
| Entity relationships (DB schema) | `erDiagram` | "Persistence model" (rare in code books) |

## 1. `graph TD` / `graph LR` — Architecture + Data Flow

**TD** (top-down) — dùng cho hierarchy, layered architecture.
**LR** (left-to-right) — dùng cho pipeline, data flow.

### Example: System architecture

```mermaid
graph TD
    Client[Client] --> Gateway[API Gateway]
    Gateway --> Auth[Auth Service]
    Gateway --> Router[Request Router]
    Router --> ServiceA[Service A]
    Router --> ServiceB[Service B]
    ServiceA --> DB[(Postgres)]
    ServiceB --> Queue[(Redis Queue)]
    Queue --> Worker[Background Worker]
    Worker --> DB
```

### Example: Data flow pipeline

```mermaid
graph LR
    Input[Raw events] --> Parse[Parser]
    Parse --> Validate[Validator]
    Validate -->|valid| Enrich[Enricher]
    Validate -->|invalid| DLQ[(Dead Letter)]
    Enrich --> Sink[Output]
```

### Style tips
- Dùng `(shape)` để phân loại: `[]` = service, `()` = storage, `{}` = decision, `([])` = terminal
- Labels trên edges khi có nhiều đường đi: `-->|condition| Target`
- Subgraphs để group:

```mermaid
graph TD
    subgraph Frontend
        UI[React App]
        Router[Router]
    end
    subgraph Backend
        API[API Server]
        DB[(Database)]
    end
    UI --> API
    API --> DB
```

## 2. `sequenceDiagram` — Interactions Over Time

Dùng khi có NHIỀU ACTORS (≥2) và thứ tự message matter. Không dùng cho internal data flow (dùng graph LR thay).

### Example: Auth handshake

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant A as Auth
    participant S as Session Store
    
    C->>G: POST /login (credentials)
    G->>A: validate(credentials)
    A->>S: lookup(user_id)
    S-->>A: user record
    A-->>G: session_token
    G-->>C: 200 OK + cookie
    
    Note over C,G: Token valid for 24h
    
    C->>G: GET /api/resource
    G->>S: validate(token)
    S-->>G: user_id
    G-->>C: resource
```

### Style tips
- `->>` = sync call, `-->>` = response, `-)` = async
- `Note over A,B: text` cho context chú thích
- `alt / else / end` cho branching logic
- `loop` cho retry/polling patterns

## 3. `stateDiagram-v2` — State Machines

Dùng khi object có finite states và transitions theo events.

### Example: Connection lifecycle

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connecting: connect()
    Connecting --> Connected: handshake_ok
    Connecting --> Failed: timeout
    Connecting --> Failed: rejected
    Connected --> Streaming: subscribe()
    Streaming --> Connected: unsubscribe()
    Streaming --> Disconnected: disconnect()
    Connected --> Disconnected: disconnect()
    Failed --> Disconnected: reset()
    Disconnected --> [*]
```

### Style tips
- `[*]` = initial/final pseudo-state
- `State: condition` cho transition condition
- `State --> State: event` cho triggered transition
- `state "Custom Label" as S1` để rename

## 4. `flowchart TD` — Decision Trees

Dùng khi có branching logic, không phải architecture. Similar to graph TD but optimized cho rhombus decisions.

### Example: Retry decision

```mermaid
flowchart TD
    Start([Request failed]) --> Transient{Transient error?}
    Transient -->|No| Dead[Send to DLQ]
    Transient -->|Yes| Attempts{Attempts < 3?}
    Attempts -->|No| Dead
    Attempts -->|Yes| Backoff[Wait 2^n + jitter]
    Backoff --> Retry([Retry])
    Retry --> Transient
    Dead --> End([Alert ops])
```

### Style tips
- `([])` = start/end terminals
- `{}` = decision diamond
- `[]` = process step
- Label edges với condition

## 5. `gantt` — Timeline / Parallel Execution

Dùng khi show phase overlap, parallel stages, deadlines.

### Example: Build pipeline

```mermaid
gantt
    title CI Pipeline Stages
    dateFormat s
    axisFormat %S
    
    section Test
    Lint           :0, 30
    Unit tests     :0, 90
    Integration    :30, 180
    
    section Build
    Compile        :90, 120
    Package        :120, 30
    
    section Deploy
    Staging        :150, 60
    Smoke tests    :210, 30
    Production     :240, 60
```

### Style tips
- `section` để group parallel tracks
- `Task :start, duration` hoặc `Task :start, end`
- Dùng cho architecture sequencing, ít khi dùng trong code books

## Diagram Count Per Chapter

| Chapter type | Diagram count | Typical mix |
|---|---|---|
| Foundation (startup, state) | 2 | 1 architecture + 1 state machine |
| Core loop | 3-4 | 1 architecture + 1 sequence + 1-2 data flow |
| Capability (tools) | 2-3 | 1 architecture + 1 data flow + 1 decision tree |
| Advanced (multi-agent) | 3-4 | 1 architecture + 2 sequence + 1 state machine |
| Infrastructure (UI, network) | 2 | 1 architecture + 1 sequence |
| Performance chapter | 2-3 | 1 data flow + 1 gantt/sequence |
| Epilogue / synthesis | 1 | 1 overview diagram tying everything |

**Target:** 2-4 diagrams per chapter. Tổng toàn sách khoảng 25-50 Mermaid diagrams.

## Anti-patterns

### ❌ Diagram thay prose
Không dùng diagram nếu prose ngắn hơn diagram. "A depends on B" không cần diagram.

### ❌ Mega-diagram
Diagram có >15 nodes là dấu hiệu chapter cần split hoặc cần break diagram thành 2-3 subgraphs.

### ❌ Labels dài
Node labels >3 từ làm diagram khó đọc. Dùng symbol + giải thích dưới.

### ❌ Repeat trong nhiều chapter
Mỗi diagram có canonical home (một chapter). Chapter khác reference: "see Figure 5-2" — không redraw.

## Mermaid rendering fallback

Nếu Mermaid không render (rare), block vẫn readable as ASCII-ish text. Không dùng Mermaid features mới (Mermaid 10+) — stick with stable subset: `graph`, `sequenceDiagram`, `stateDiagram-v2`, `flowchart`, `gantt`.

**Avoid:** `timeline`, `mindmap`, `quadrantChart`, `C4`, `sankey` — rendering không consistent cross-platform.
