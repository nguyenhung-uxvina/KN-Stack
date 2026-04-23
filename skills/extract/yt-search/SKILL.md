Search YouTube for videos on a topic, extract metadata and transcripts, and optionally feed results to NotebookLM for analysis.

Usage: /yt-search <topic> [--count N] [--transcript]

PATH: yt-dlp is at C:/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts/yt-dlp.exe
Always prefix commands with: `export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"`

---

## WORKFLOW

### Step 1: Search YouTube

```bash
yt-dlp "ytsearch5:<topic>" --flat-playlist --print "%(id)s | %(title)s | %(duration_string)s | %(view_count)s views | %(upload_date)s" --no-download
```

Adjust count: `ytsearch10:` for 10 results, etc.

### Step 2: Present Results

Show results as a numbered table:

| # | Title | Duration | Views | Date | URL |
|---|-------|----------|-------|------|-----|

Ask user: which videos to process further?

### Step 3: Extract Details (if requested)

For selected videos, get transcript + description:

```bash
yt-dlp --write-auto-sub --sub-lang en,vi --skip-download --print-to-file "%(title)s\n%(description)s" - "https://youtube.com/watch?v=<ID>"
```

Or get transcript as text:
```bash
yt-dlp --write-auto-sub --sub-lang en --convert-subs srt --skip-download -o "%(title)s.%(ext)s" "https://youtube.com/watch?v=<ID>"
```

### Step 4: Route Output

Options (ask user):
a) **Add to NotebookLM notebook** → `nlm source add <notebook> --url "https://youtube.com/watch?v=<ID>"`
b) **Save transcript to vault** → Write to `0_Inbox/YT_<title>_<date>.md` with frontmatter
c) **Both** — add to NLM for analysis + save raw to vault
d) **Analyze inline** — use Claude Code to extract signals (run /signal logic)

---

## NLM INTEGRATION

If user wants NLM analysis after search:
1. Add selected videos as sources to a notebook
2. Run `/nlm generate report <notebook> --confirm` for analysis
3. Save output to vault

---

## RULES

- Default search count: 5 (override with --count)
- Always show results before processing — let CEO choose
- Never download full video files — transcripts and metadata only
- For Vietnamese content, try `--sub-lang vi` first, fallback to auto-generated
- COD: Search = Offload, video selection = Core, insight extraction = Core
