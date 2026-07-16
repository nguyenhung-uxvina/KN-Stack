# krpano — Hệ thống học tập DMIR × Meta-Learning

> Đi kèm skill `wx-krpano`. KHÔNG phải danh sách bài đọc — là một **cỗ máy học** tự lặp.
> Hai khung áp dụng: **DMIR** (Diagnose→Model→Intervene→Reflect, mượn từ mentor-board) làm bộ khung; **Meta-learning** (deliberate practice, retrieval, spacing, interleaving, Feynman, 80/20, calibration) làm cách thực thi bên trong mỗi frame.
> Tra cứu tham số bất kỳ lúc nào: `nlm notebook query krpano "<câu hỏi>"`.

---

## PART A — DMIR MACRO: Chẩn đoán chiến lược học (đọc 1 lần trước khi bắt đầu)

### FRAME 1 — DIAGNOSE (vấn đề học THẬT sự là gì?)
- **CEO phát biểu:** "học krpano step by step".
- **Re-frame (vấn đề thật):** Bạn KHÔNG cần "biết krpano" — bạn cần **tin cậy SẢN XUẤT được 4 loại tour deliverable và tự debug khi hỏng**. Gap là *năng lực sản xuất + mô hình gỡ lỗi*, không phải kiến thức bách khoa.
- **Vì sao dễ mis-frame:** coi một *công cụ/nghề* như một *môn học* → đọc tuyến tính, xem hết video, ghi chép — rồi 20h sau không có tour nào chạy được. Đây chính là **Analyst Trap** ở dạng học tập.
- **Đối tượng chẩn đoán:** krpano là *craft* (tay nghề), học bằng tay + phản hồi, không bằng đọc.

### FRAME 2 — MODEL (mô hình tư duy áp cho việc học này)
- **Framework:** *DMIR micro-loop + Deliberate Practice + 80/20*. Mỗi đơn vị học = 1 vòng DMIR, luyện ở **rìa năng lực** với phản hồi tức thì.
- **Schema krpano cần nạp TRƯỚC (một câu):**
  > *ảnh 360 → cắt tile multires → scene → hotspot điều hướng → embed → deploy offline*.
  Mọi thứ khác (scripting, JS, plugin, VR) chỉ là **nhánh treo** vào xương sống này. Nắm xương sống = nắm 80%.
- **Vì sao áp được:** krpano rộng nhưng có 1 đường trục; học trục trước, chi tiết tra cứu sau (notebook `krpano` = bộ nhớ ngoài).

### FRAME 3 — REJECT (lớp phản biện — KHÔNG chiều theo default của CEO)
- **Default CEO dễ làm:** chạy tuyến tính Module 0→7, xem hết tutorial, "đọc xong manual rồi mới dựng".
- **REJECT thẳng:**
  1. ❌ Hoàn thành tuyến tính front-to-back → **thay bằng** dựng tour tối thiểu ở Module 2 NGAY, mọi thứ khác kéo vào khi cần.
  2. ❌ Xem video thụ động = ảo giác hiểu → **thay bằng** retrieval (tự làm lại không nhìn) + Feynman (giảng lại).
  3. ❌ Học scripting (M3/M4) trước khi *đau* → chỉ học script khi hotspot tĩnh không đủ. Học giải-pháp trước vấn-đề = quên ngay.
- **Failure mode nếu phớt lờ:** 20h, đầy note, **0 tour giao được**, chi tiết rơi rụng (spacing chưa có). Đúng Analyst Trap.

### FRAME 4 — ADAPT (bối cảnh Workshop X)
- **KEEP:** practice-first · dựng deliverable thật · vòng DMIR · 80/20.
- **ADAPT:**
  - CEO quỹ thời gian mỏng (COD < 60% Core) → **micro-session 45–90'**, interleave xen với việc sản phẩm thật, KHÔNG cày liền 8h.
  - Học trên **nhu cầu showcase THẬT** (1 sản phẩm đã-duyệt-lộ), không tour đồ chơi → transfer ngay ra giá trị.
  - Ràng buộc air-gap/MẬT → bỏ hẳn mọi lối tắt cloud (Security Gate luôn bật).
- **NOT-APPLICABLE:** kiểu "học trọn API cho đội lớn" · học để thi/chứng chỉ · hoàn hảo-chủ-nghĩa.

### FRAME 5 — INTERVENE (kế hoạch cụ thể, đo được — xem Part D)
- **Tuần 1:** hoàn tất Module 0→2 → **success: 1 tour 3-scene đi lại mượt qua localhost** — check: hết tuần 1.
- **Tuần 2–4:** Module 3→6 xen kẽ, mỗi tuần 1 nhánh + ôn spaced → **success: tự viết 2 action + ra 1 `.exe` offline no-watermark** — check: hết tuần 4.
- **Quý:** Capstone Module 7 → **success: tour showcase đạt full Quality Checklist, dùng cho khách/BQP** — check: cuối quý.

### FRAME 6 — REFLECT (đóng vòng — xem Part E)
Sau mỗi cycle: error-log + teach-back + lịch spaced review. Chốt quý bằng một retro (kiểu `/mentor-board --retro`): dự đoán năng lực có đúng không? framework nào cần chỉnh?

---

## PART B — DMIR MICRO: Cỗ máy chạy cho MỖI module

Mỗi module dưới đây chạy qua đúng 4 nhịp. Đây là phần "how" — lặp lại 7 lần:

| Nhịp | Làm gì | Meta-learning tactic |
|------|--------|----------------------|
| **D — Diagnose** | Trả lời trước: "Module này giải quyết mình *chưa làm được* điều gì?" Viết 1 câu. | *Metacognition + calibration*: tự chấm 1–5 mình nghĩ mình biết bao nhiêu (đối chiếu ở R). |
| **M — Model** | Trước khi làm: vẽ/nói schema của module (vd "scene = 1 điểm chụp, hotspot = cửa sang scene khác"). | *Chunking + Feynman-lite*: giải thích bằng lời của mình cho tới khi gọn 1 câu. |
| **I — Intervene** | Làm **drill deliberate practice** (bảng Part C) ở rìa năng lực; hỏng thì tra NLM, KHÔNG xem lời giải trước. | *Deliberate practice + desirable difficulty + retrieval*: tự vật lộn trước, feedback tức thì qua testserver. |
| **R — Reflect** | Ghi **error-log** (lỗi gặp + nguyên nhân + cách sửa), teach-back 3 câu, hẹn ôn lại (spacing). | *Retrieval + spacing + teach-to-learn*. |

**Cổng chuyển module (desirable difficulty):** chỉ qua module sau khi *retrieval PASS* — làm lại được deliverable module này **không nhìn hướng dẫn**.

---

## PART C — Meta-Learning Toolkit (kỹ năng CHUYỂN GIAO được, không chỉ cho krpano)

| Nguyên lý | Nghĩa | Áp vào krpano |
|-----------|-------|---------------|
| **80/20 (vital few)** | 20% nội dung cho 80% giá trị | Module 2 (scene+hotspot) = trục; ưu tiên tuyệt đối |
| **Deliberate practice** | Luyện ở rìa năng lực, mục tiêu hẹp, feedback tức thì | Mỗi module 1 "drill" cụ thể, chạy testserver xem ngay |
| **Retrieval practice** | Tự tái tạo > đọc lại | Dựng lại tour **không nhìn** trước khi qua module |
| **Spaced repetition** | Ôn theo khoảng giãn dần | Lịch Part E (ngày 1 → 3 → 7 → 21) |
| **Interleaving** | Trộn chủ đề, không học khối liền | Xen scripting với deploy, không cày 1 topic 4h |
| **Feynman** | Giảng lại đơn giản để lộ lỗ hổng | Teach-back 3 câu cuối mỗi module |
| **Desirable difficulty** | Khó có kiểm soát → nhớ lâu | Vật lộn trước khi tra NLM; cổng retrieval |
| **Calibration** | Khớp "nghĩ mình biết" với "thực biết" | Chấm 1–5 ở D, đối chiếu ở R |
| **Transfer / project-based** | Học gắn sản phẩm thật | Học trên tour showcase thật của Xưởng |
| **External memory** | Đừng nhớ cái tra được | Notebook `krpano` = bộ nhớ ngoài; nhớ *đường trục*, tra *tham số* |

---

## PART D — Curriculum: 7 module chạy qua cỗ máy DMIR

> Mỗi module ghi sẵn: **D** (chưa làm được gì) · **M** (schema) · **I-drill** (luyện) · **R-gate** (retrieval để qua). Thời lượng = micro-session.
> Hai nhánh: **Fast Track** = 0·1·2·6·7 (~13h, đủ ra showcase). **Mastery** = 0→7 (~27h).

### M0 — Môi trường (1h)
- **D:** chưa chạy được krpano cục bộ. **M:** "krpanotools = hộp lệnh; testserver = cửa xem." 
- **I-drill:** `register` bỏ watermark → `testserver` → mở 3 demo trong `examples/`.
- **R-gate:** mở lại 1 demo qua `http://localhost:8090` không cần trợ giúp. NLM: *"krpanotools functions and testserver usage"*.

### M1 — Panorama đầu tiên, 1 scene (2h)
- **D:** chưa biến ảnh → pano xem được. **M:** "ảnh equirect 2:1 (hoặc cube `_l/_f/_r/_b/_u/_d`) → makepano cắt tile → xem."
- **I-drill:** `krpanotools makepano <ảnh>.jpg` → mở → đổi `<view hlookat vlookat fov>` reload.
- **R-gate:** tự tạo lại pano + set view khởi tạo, không nhìn. NLM: *"panorama formats equirectangular vs cube and view hlookat vlookat fov"*.

### M2 — Tour đa cảnh + hotspot ⭐ (4h) — TRỤC 80%
- **D:** chưa nối được nhiều điểm chụp thành tour đi lại. **M:** "scene = điểm chụp; hotspot `onclick=loadscene()` = cửa; BLEND = chuyển mượt."
- **I-drill:** chụp 3–4 điểm → **MAKE VTOUR (MULTIRES) droplet** → thêm hotspot điều hướng:
  ```xml
  <hotspot name="to_side" style="skin_hotspotstyle" ath="45" atv="-5"
           distorted="true" onclick="loadscene(scene_side,null,MERGE,BLEND(1.0));" />
  ```
- **R-gate (CỔNG QUAN TRỌNG NHẤT):** dựng lại tour 3-scene đi lại mượt **không link chết, không nhìn hướng dẫn**. NLM: *"scene structure, navigation hotspots loadscene, hotspot ath atv distorted"*.

### M3 — XML Actions scripting (4h) *(chỉ học khi hotspot tĩnh không đủ)*
- **D:** chưa tự thêm tương tác động. **M:** "actions = list lệnh `;`; biến phải `get()/calc()/*`; scope local/global."
- **I-drill:** viết auto-rotate khi idle (`asyncloop`) + nút toggle layer info (`if`+`set`) + `scale.mobile`.
- **R-gate:** viết 2 action mới không copy nguyên. NLM: *"actions scripting syntax get calc, loops asyncloop renderloop, scope, device filtering"*.

### M4 — JavaScript Interface + embed (3h)
- **D:** chưa nhúng/điều khiển từ web app ngoài. **M:** "`embedpano({target,xml,onready})`; `krpano.get('global')` = Direct Access nhanh; đợi `onready`."
- **I-drill:** nhúng tour vào trang HTML tự viết + `addhotspot` từ JS + overlay theo `spheretoscreen`.
- **R-gate:** nhúng + thêm 1 hotspot bằng JS. NLM: *"embedpano parameters, Direct Access API krpano.get global, screentosphere spheretoscreen, onready onxmlcomplete"*.

### M5 — Plugins: WebVR / FloorPlan / Postproc (4h)
- **D:** chưa dùng được VR/minimap. **M:** "plugin dựng sẵn nạp qua XML; `registerplugin` là entry; VR scale 1 unit=1cm."
- **I-drill:** bật `webvr.xml` xem VR điện thoại; bật FloorPlan (map+radar cone, cần `key_flpl.xml`).
- **R-gate:** tour vào VR + có minimap hướng nhìn. NLM: *"plugin interface registerplugin, webvr, floorplan key file, postprocessing phases"*.

### M6 — Deploy OFFLINE + license (3h)
- **D:** chưa đóng gói chạy offline. **M:** "`file://` bị chặn → NW.js `.exe` / localhost / inline; license `register` per-domain."
- **I-drill:** gói NW.js `.exe` (`package.json` main=tour.html, fullscreen) → chạy trên máy **không mạng**.
- **R-gate:** ra 1 `.exe` double-click chạy offline, no watermark, đã xoá `tour_editor.html`. NLM: *"local offline usage file restrictions, NW.js package.json, license headless"*.

### M7 — Capstone: Tour trưng bày sản phẩm ⭐ (6h)
- **D:** chưa ghép mọi thứ thành deliverable giao được. **M:** áp trọn skill `wx-krpano` template #1.
- **I-drill:** Security Gate → chụp 4–6 góc sản phẩm đã-duyệt → MAKE VTOUR + Little Planet Intro + hotspot info + `.exe`.
- **R-gate:** đạt **toàn bộ Quality Checklist** trong SKILL.md → transfer thành công.

---

## PART E — Lịch Spaced Repetition & Retro (đóng vòng R)

**Spacing mỗi kỹ năng cốt lõi (M2, M6):** ôn bằng *retrieval* (làm lại, không đọc) vào **ngày 1 → 3 → 7 → 21**. Mỗi lần ≤ 15'. Nếu quên > 30% → rút ngắn khoảng.

**Interleaving tuần:** đừng học 1 topic liền mạch. Mẫu tuần 2–4:
```
Thứ 2: M3 script (drill)     Thứ 3: ôn-retrieval M2     Thứ 5: M6 deploy (drill)
Thứ 6: ôn-retrieval M3       CN: teach-back tổng
```

**Error-log (bảng sống, mỗi module ghi):**
| Ngày | Lỗi gặp | Nguyên nhân gốc | Cách sửa | Ôn lại lúc |
|------|---------|-----------------|----------|-----------|

**Retro cuối quý (R-closure, kiểu mentor-board --retro):**
- Dự đoán "sẽ dựng được showcase" — HIT / MISS / PARTIAL?
- Framework nào (80/20? script-khi-đau?) đúng/sai với thực tế Xưởng?
- Cập nhật lại plan này (đây là tài liệu sống).

---

## PART F — Metacognition Dashboard (tự soi, chống ảo giác hiểu)

Tự chấm sau mỗi module (1–5), đối chiếu D vs R để hiệu chỉnh calibration:

| Module | Nghĩ mình biết (D) | Thực làm được (R-gate PASS?) | Lệch? → hành động |
|--------|:---:|:---:|---|
| M0 |  |  |  |
| M2 ⭐ |  |  |  |
| M6 |  |  |  |
| M7 ⭐ |  |  |  |

**3 câu test "đã thực hiểu" (Feynman):** giải thích cho 1 NV chưa biết, trong 1 câu mỗi ý:
1. Multires tiling giải quyết gì? 2. Vì sao không mở `file://`? 3. Khi nào dùng actions vs JavaScript?
Nói lắp/phải mở doc = chưa qua → quay lại I-drill module đó.

---

## Bản đồ tra cứu (topic → nguồn notebook `krpano`)
| Chủ đề | Nguồn |
|--------|-------|
| XML/scene/tag | docu/xml · JS: docu/js · Actions: docu/actions · Embed: docu/embedpano · Plugin: docu/plugininterface |
| CLI/config/droplets | docu/tools · docu/tools/config · tools/droplets · vtour-multires.config |
| Pano formats / offline / license / VR | docu/panoformats · docu/localusage · download · plugins/webvr |
| Tổng hợp kiến trúc | "Architectural Reference & Engineering Manual" (deep report) |

## Công cụ Retrieval/Spacing sẵn có — NLM Studio (notebook `krpano`)
Đã sinh 2026-07-16, tiếng Việt (giữ thuật ngữ API tiếng Anh). Mở tại: https://notebooklm.google.com/notebook/e041cc65-742c-4734-a346-4b0171187754

| Artifact | Dùng cho nhịp DMIR | Cách dùng trong plan |
|----------|---------------|----------------------|
| **Quiz** (hard — tình huống sản xuất + troubleshooting) | **R-gate / retrieval** | Làm để mở cổng qua module; sai câu nào → quay lại I-drill module đó |
| **Flashcards** (Dễ/TB/Khó) | **R — Spacing** | Ôn theo lịch ngày 1→3→7→21 (Part E); nhắm số/rule dễ quên |
| **Study Guide report** ("Hệ thống Scripting và Phân phối Tour Ảo") | **M — Model** | Đọc để nạp schema có thứ tự (7 bước) trước khi vào I-drill |
| **Audio Deep-Dive VN** | **Interleaving** | Nghe khi di chuyển; củng cố đường trục 80/20 + 3 quyết định + cạm bẫy |
| **Audio Critique VN** (phản biện) | **R — Reflect / phán đoán** | Nghe trước khi cam kết dựng tour cho khách; rèn hỏi "có thật sự cần tour không?" |

> Artifact IDs: quiz `7dbedd74` · flashcards `4297514c` · study-guide `91c393ca` · audio-deepdive `1e82cdf3` · audio-critique `de35e672`. (Audio VN render async — xem panel Studio.) Regenerate/thêm: skill `research` RKB-3 hoặc `studio_create`.

## Bổ trợ khác
- `/learning --mode practice` bám M1–M2 để khởi động; `/mentor-board --retro` để đóng R-frame cuối quý.
