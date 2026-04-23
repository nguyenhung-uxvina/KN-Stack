# Rules for 1_Projects/ folder

Khi làm việc trong 1_Projects/:

## Before any action
- Đọc `Status.md` của project trước khi làm bất kỳ điều gì
- Xác định Pahl-Beitz phase hiện tại và blocking constraint

## Project requirements
- Mỗi project PHẢI có: P-B phase, next physical gate date, blocking constraint
- Tier 1 (Prototype): physical gate ≤ 30 ngày. Ưu tiên cao nhất.
- Tier 2 (Product Dev): Pahl-Beitz phase tracking, dP/dt monitoring
- Tier 3 (Strategic): clear "done" criteria, lower priority than T1/T2

## Warnings
- Nếu project không có physical gate trong 30 ngày → cảnh báo: "Project này đang chuyển sang Area mode"
- Nếu Status.md chưa update > 7 ngày → nhắc CEO cập nhật

## Logging
- Design decisions → append vào `_meta/decisions.md` với context + rationale
- Session insights → append vào `_meta/learnings.md`
- Khi update Status.md → luôn cập nhật "updated" date trong frontmatter

## COD
- Task clarification, concept evaluation, gate decisions = Core (CEO)
- Drafting, formatting, analysis, search = Offload (AI)
- Notifications, cleanup = Default (skip/automate)
