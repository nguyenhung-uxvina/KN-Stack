# NLM Notebook Registry — Research Pipeline

## Active Notebooks

| Alias | Topic | Notes |
|-------|-------|-------|
| `kpipe` | Siêu quy trình nghiên cứu | GOD MODE setup |
| `ast` | AST-MSL-001 Design Questions | Towed target |
| `rcs` | Trihedral Corner Reflector RCS | Radar cross-section |
| `lomah` | Piezo LOMAH Signal Conditioning | BB-01 |
| `127sim` | 12.7mm Simulator Recoil Fidelity | VN-12.7MM-SIM |
| `ach` | ACH Defense Training Cases | 34 sources |
| `mcp-agent` | MCP Agent Development | Claude Code skills |
| `ssusv` | Semi-Sub USV Design | VN-USV-SS-001 |
| `hdpe-hull` | HDPE Torpedo Hull | 19 sources |
| `stability` | Stability analysis | Marine engineering |
| `hdpe-mooring` | HDPE mooring systems | VN-AST-MSL-001 |
| `multi-agent-design` | Multi-Agent Collaborative Conceptual Design | 30 sources, deep research 2026-04-22 |

## Notebook Management Commands

```bash
# Create new notebook
nlm notebook create "{{Research Topic}}"
nlm alias set {{short-name}} {{new-notebook-id}}

# Check source count (limit ~50)
nlm source list {{notebook}} 2>&1 | wc -l

# Prune low-relevance sources
# See: 1_Projects/VN-XUONG-UUV/References/prune_nlm.py
```

## Source Limits
- NLM hard limit: ~50 sources per notebook
- Warn at 45+ sources
- If approaching limit: create sub-notebook or prune low-relevance web_page sources
- Prune script uses `nlm source delete` with `--confirm` flag + 1.5s rate limit
