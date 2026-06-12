---
name: convert_md_to_docx
description: >-
  Convert a Markdown file to DOCX format using python-docx. Handles headings,
  tables, bullet and numbered lists, bold/italic, checkboxes, YAML frontmatter
  stripping, and horizontal rules. Use when a Vietnamese defense document or
  project report needs to be delivered as a Word file. Triggers on: "convert to
  docx", "markdown to word", "xuất file Word", "chuyển sang docx", "tạo file
  docx".
---

Convert a Markdown file to DOCX format.

Usage: /splash <file_path>

1. If no file path is provided in "$ARGUMENTS", ask the user which .md file to convert.
2. Read the markdown file using the Read tool.
3. Determine the output path: same directory, same name but `.docx` extension.
4. Run the following Python script via Bash to convert:

```bash
python -c "
import sys, re, os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0] + '.docx'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip YAML frontmatter
content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

lines = content.split('\n')
i = 0
in_table = False
table_rows = []

while i < len(lines):
    line = lines[i]

    # Headings
    if line.startswith('######'):
        doc.add_heading(line[6:].strip(), level=6)
    elif line.startswith('#####'):
        doc.add_heading(line[5:].strip(), level=5)
    elif line.startswith('####'):
        doc.add_heading(line[4:].strip(), level=4)
    elif line.startswith('###'):
        doc.add_heading(line[3:].strip(), level=3)
    elif line.startswith('##'):
        doc.add_heading(line[2:].strip(), level=2)
    elif line.startswith('#'):
        doc.add_heading(line[1:].strip(), level=1)
    # Horizontal rule
    elif line.strip() in ('---', '***', '___'):
        doc.add_paragraph('_' * 50)
    # Table rows
    elif '|' in line and line.strip().startswith('|'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if all(set(c) <= set('-: ') for c in cells):
            i += 1
            continue
        table_rows.append(cells)
        # Check if next line is still table
        if i + 1 < len(lines) and '|' in lines[i+1] and lines[i+1].strip().startswith('|'):
            i += 1
            continue
        # End of table — render it
        if table_rows:
            cols = max(len(r) for r in table_rows)
            table = doc.add_table(rows=len(table_rows), cols=cols, style='Table Grid')
            for ri, row in enumerate(table_rows):
                for ci, cell in enumerate(row):
                    if ci < cols:
                        table.rows[ri].cells[ci].text = cell
                        for p in table.rows[ri].cells[ci].paragraphs:
                            for run in p.runs:
                                run.font.size = Pt(9)
            # Bold header row
            for ci in range(cols):
                for run in table.rows[0].cells[ci].paragraphs[0].runs:
                    run.bold = True
            table_rows = []
    # Bullet list
    elif line.strip().startswith('- ') or line.strip().startswith('* '):
        indent = len(line) - len(line.lstrip())
        level = indent // 2
        text = line.strip()[2:]
        # Handle checkbox
        if text.startswith('[x] '):
            text = '[DONE] ' + text[4:]
        elif text.startswith('[ ] '):
            text = '[TODO] ' + text[4:]
        p = doc.add_paragraph(text, style='List Bullet')
        if level > 0:
            p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    # Numbered list
    elif re.match(r'^\s*\d+\.\s', line):
        text = re.sub(r'^\s*\d+\.\s', '', line)
        doc.add_paragraph(text, style='List Number')
    # Empty line
    elif line.strip() == '':
        pass
    # Normal paragraph
    else:
        p = doc.add_paragraph()
        # Simple bold/italic parsing
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                run = p.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*'):
                run = p.add_run(part[1:-1])
                run.italic = True
            else:
                p.add_run(part)
    i += 1

doc.save(output_file)
print(f'Saved: {output_file}')
" "$INPUT_FILE"
```

Replace `$INPUT_FILE` with the actual absolute path (quoted for spaces).

5. Confirm to the user: output file path and size.
6. If conversion fails, check that `python-docx` is installed (`pip install python-docx`) and retry.

Notes:
- Handles: headings, tables, bullet/numbered lists, bold/italic, checkboxes, YAML frontmatter stripping, horizontal rules
- Does NOT handle: images, complex nested markdown, code blocks with syntax highlighting
- For full-featured conversion, install pandoc: `winget install JohnMacFarlane.Pandoc`
