---
name: wx-krpano
description: "Offline-first 360° virtual-tour production layer for Workshop X — drives the krpano engine (krpanotools CLI + MAKE VTOUR droplets + XML/JS scaffolding) to turn a folder of panorama photos into a self-hosted or standalone-.exe interactive tour. Built for air-gapped defense use: product-showcase tours, offline BQP demo kiosks, facility as-built documentation, and WebVR training walkthroughs. Never uploads to cloud tour hosts. Complements wx-diagram (static diagrams) — wx-krpano = immersive walkable deliverables. Triggers on: 'wx-krpano', 'krpano', 'virtual tour', 'tour ảo 360', 'tour 360', '360 panorama tour', 'panorama viewer', 'MAKE VTOUR', 'multiresolution pano', 'hotspot scene', 'WebVR tour', 'offline tour kiosk', 'dựng tour ảo', 'tour trưng bày sản phẩm', 'tour tham quan xưởng', 'embedpano'."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "PowerShell"]
---

# wx-krpano — Tầng sản xuất tour ảo 360° (krpano engine)

> **Purpose:** Biến một thư mục ảnh panorama 360° thành tour ảo tương tác **self-hosted / chạy offline**, dùng cho deliverable "ra khỏi xưởng" và demo tại chỗ.
> **Engine:** krpano (krpanotools CLI + droplets + XML actions + JavaScript interface). Code-driven, không phụ thuộc GUI.
> **Định vị:** Bổ trợ `wx-diagram` (sơ đồ tĩnh draw.io) — `wx-krpano` = không gian đi lại được (immersive). KHÔNG thay `helix-draw` (phác thảo nội bộ Excalidraw).
> **Nguyên tắc số 1:** OFFLINE-FIRST. Không bao giờ đẩy panorama lên host tour đám mây (Matterport/Panoee/...). Xưởng sở hữu toàn bộ file đầu ra.

---

## When to Use / When NOT

**Dùng khi:**
- Cần tour 360° trưng bày sản phẩm defense cho khách/BQP (BB-01, VSN bridge, USV, target family...).
- Cần kiosk demo chạy offline (đóng gói `.exe`) khi đoàn tham quan, không có/không được nối mạng.
- Cần tài liệu hoá as-built phân xưởng/dây chuyền (bản ghi nội bộ).
- Cần walkthrough huấn luyện WebVR (Meta Quest) cho khí tài.

**KHÔNG dùng khi:**
- Chỉ cần sơ đồ/bản vẽ tĩnh → dùng `wx-diagram` (draw.io) hoặc `helix-draw`.
- Cảnh/sản phẩm là MẬT mà đích đến là host bên thứ ba → **STOP** (xem Security Gate).
- Chưa có ảnh panorama 360 (equirectangular hoặc cube) → chụp/ghép trước (Hugin, PTGui, hoặc camera 360 như Insta360/Ricoh Theta).

---

## Step 0 — Security & Classification Gate (Core — KHÔNG SKIP)

**Một ảnh 360° của xưởng hoặc sản phẩm quốc phòng TỰ NÓ là dữ liệu nhạy cảm.** Chạy gate này TRƯỚC khi chụp/ingest bất cứ gì.

```
PHÂN LOẠI nội dung tour:
  THƯỜNG / showcase công khai (sản phẩm đã lộ, marketing được duyệt)
      → OK mọi chế độ deploy (kể cả self-hosted web nội bộ có kiểm soát).
  HẠN CHẾ / nội bộ (layout dây chuyền, as-built)
      → CHỈ self-hosted trên hạ tầng Xưởng HOẶC đóng gói offline .exe. Không host công khai.
  MẬT (cơ sở/khí tài phân loại mật, khu vực cấm)
      → CHỈ đóng gói offline .exe trên máy air-gapped, bàn giao tay.
        KHÔNG localhost expose ra LAN chung, KHÔNG cloud, KHÔNG CDN.
        Cân nhắc protect/encrypt (krpanotools) cho file tour.
```

**Rule:** AI đề xuất phân loại, **CEO xác nhận**. Nếu MẬT → mọi bước sau mặc định về chế độ NW.js standalone offline. Không có ngoại lệ "để test nhanh trên cloud".

---

## Core Principles (phải NẮM để dùng đúng)

1. **Dual runtime — hai ngôn ngữ điều khiển.** krpano có (a) **XML actions scripting** (ngôn ngữ riêng, chạy trong viewer, dấu `;` kết thúc lệnh) và (b) **JavaScript Interface** (điều khiển từ web app ngoài). Dùng actions cho logic trong tour; dùng JS khi nhúng vào ứng dụng web/HTML lớn hơn. [NLM: docu/actions, docu/js]

2. **Pipeline tools/droplets, KHÔNG dựng tay từ đầu.** `krpanotools` là CLI với các hàm: `makepano` (tạo pano/tour theo template), `maketiles`, `convert`, `makepreview`, `spheretocube`, `cubetosphere`, `protect`, `encrypt`, `testserver`, `register`. Droplet **MAKE VTOUR (MULTIRES)** = kéo-thả ảnh lên → sinh tour multires hoàn chỉnh + skin điều hướng. [NLM: docu/tools, tools/droplets]

3. **Multiresolution tiling = xem gigapixel không giới hạn.** Ảnh được cắt thành tile theo nhiều mức phân giải; viewer chỉ tải tile cần thiết cho khung nhìn hiện tại → không giới hạn kích thước, tải nhanh. Config điển hình: `tilesize=512`, `customimage[vr].size=1536`, `jpegquality=82`. [NLM: vtour-multires.config, docu/tools/config]

4. **`tour.xml` + scene = xương sống tour.** Mỗi điểm chụp = một `<scene>`; điều hướng giữa scene = **hotspot** có `onclick="loadscene(...)"`. Tour đa cảnh nằm trong một `tour.xml`. [NLM: deep report §XML]

5. **Nhúng bằng `embedpano()`, host bằng file tĩnh.** Trang HTML nạp `krpano.js` (hoặc `tour.js`) rồi gọi `embedpano({target, xml, onready})`. Đầu ra là **file tĩnh** — deploy trên server nội bộ, localhost, hoặc gói vào `.exe`. [NLM: docu/embedpano]

6. **WebGL là chính, CSS3D là fallback.** Render trên GPU (mục tiêu 60fps). WebGL2 mở khoá 3D model / Gaussian Splatting / NPOT texture; CSS3D chỉ hỗ trợ cube/flat, không post-processing/VR. Giới hạn ~8 WebGL context/trang → giải phóng bằng `removepano()`/`.unload()`. [NLM: deep report §WebGL]

---

## Prerequisites

- **krpano license + krpanotools** cài trên máy build (bản Xưởng). Bản chưa đăng ký chạy được nhưng chèn watermark → phải `register` trước khi giao.
- Thư mục ảnh panorama 360°: **equirectangular** (tỉ lệ 2:1) hoặc **cube** (6 mặt, hậu tố `_l _f _r _b _u _d` hoặc `left front right back up down` để tự nhận diện). [NLM query2 cite 1]
- Cân nhắc phân loại (Step 0) đã xong.

---

## Workflow — từ ảnh 360 tới tour deploy (5 stage)

### Stage 1 — Chuẩn bị ảnh
- Gom ảnh mỗi điểm chụp; đặt tên rõ theo scene (vd `lobby.jpg`, `assembly_line.jpg`).
- Cube thì giữ hậu tố mặt. Equirect thì đảm bảo 2:1, đủ phân giải (≥ 8000×4000 cho zoom nét).

### Stage 2 — Sinh multires vtour (droplet hoặc CLI)
- **Cách nhanh (droplet):** kéo-thả cả thư mục ảnh lên **`MAKE VTOUR (MULTIRES) droplet.bat`**. Sinh tiles + `tour.xml` + skin điều hướng (`vtourskin-thumbnails-bingmaps-gyro.skin`). Config: `vtour-multires.config`. [NLM: tools/droplets]
- **Cách CLI (scriptable, ưu tiên trong pipeline agentic):**
  ```bash
  krpanotools makepano -config=vtour-multires.config *.jpg
  ```
- Tile config chủ chốt (chỉnh trong `.config`): `tilesize=512`, `maxsize=auto`, `maxcubesize=auto`, VR-optimized `customimage[vr].size=1536` `jpegquality=82 jpegsubsamp=444 jpegoptimize=true`. Placeholder tilepath: `%l`=mức, `%h`/`%v`=chỉ số tile ngang/dọc, `[c]`=ký tự mặt cube, `%f`=frame. [NLM query1 cites]

### Stage 3 — Cấu trúc file đầu ra
```
/vtour/
├── tour.html            # trang xem (dùng testserver hoặc deploy)
├── tour.xml             # scene + hotspot + view khởi tạo
├── tour.js              # viewer + license nhúng
├── tour_editor.html     # (tuỳ chọn) editor — XOÁ trước khi giao
├── skin/                # UI: nút, thumbnail, gyro...
└── panos/
    └── <scene>.tiles/   # tiles đa mức + preview.jpg + vr/
```

### Stage 4 — Scene, hotspot, điều hướng (sửa `tour.xml`)
- **View khởi tạo** mỗi scene: `<view hlookat="0" vlookat="0" fov="90" />` (giới hạn pano từng phần bằng `limitview`). [NLM cite 60]
- **Hotspot điều hướng** (đứng trong 3D, `distorted="true"`):
  ```xml
  <hotspot name="to_hallway" style="skin_hotspotstyle"
           ath="45.0" atv="-10.0" distorted="true"
           onclick="loadscene(scene_hallway, null, MERGE, BLEND(1.0));" />
  ```
- **Chuyển cảnh mượt:** `loadscene(name, null, MERGE, BLEND(1.0))` hoặc zoom-blend. Tham số blend `time`, `zoom`, `tweentype` (mặc định `easeInOutSine`). [NLM cite 69]
- **Actions scripting nhớ:** biến truyền vào là *tên* trừ khi dùng `get(var)` / `*var`; tính toán bọc trong `calc(...)`; lệnh kết bằng `;`. Lọc thiết bị: `devices="mobile|tablet"`, `scale.mobile="0.5"`. [NLM: deep report §Actions]
- **Bổ sung bằng JS (khi cần):** `krpano.get("global")` → Direct Access API nhanh (bypass parser); `addhotspot()`, `screentosphere()/spheretoscreen()` để gắn overlay HTML, `addChangeListener()` theo dõi camera. [NLM: deep report §JS]

### Stage 5 — Nhúng & deploy
- **Nhúng:**
  ```html
  <div id="pano" style="width:100%;height:100vh;"></div>
  <script src="tour.js"></script>
  <script>
    embedpano({ xml:"tour.xml", target:"pano",
                html5:"only+webgl", onready:function(k){ /* ready */ } });
  </script>
  ```
- Chọn chế độ deploy theo Step 0 (xem "Deployment Modes"). Xem thử tại chỗ bằng **krpano Testing Server** (`krpanotools testserver`) — KHÔNG mở trực tiếp `file://` (bị chặn, xem Gotchas).

---

## Decision Rules (IF → THEN)

- **IF** ảnh > ~4000px hoặc cần zoom nét **THEN** multiresolution (droplet MULTIRES). **ELSE** single-resolution cho pano nhỏ/preview nhanh.
- **IF** nguồn là ảnh equirectangular 2:1 **THEN** để nguyên (WebGL render sphere trực tiếp). **IF** cần CSS3D fallback/thiết bị cũ **THEN** `spheretocube` (CSS3D chỉ hỗ trợ cube/flat).
- **IF** logic nằm trong tour (điều hướng, animation, tooltip) **THEN** XML actions. **IF** điều khiển từ app web ngoài / tích hợp React-HTML **THEN** JavaScript Interface (`krpano.get("global")`).
- **IF** tour giao khách/BQP **THEN** `krpanotools register <key>` để bỏ watermark trước. **IF** chỉ test nội bộ **THEN** chấp nhận bản chưa đăng ký.
- **IF** MẬT hoặc không có mạng ở nơi demo **THEN** đóng gói NW.js standalone `.exe` (offline hoàn toàn). **IF** nội bộ có server **THEN** self-hosted static. **IF** dự án cực nhỏ **THEN** inline base64 vào 1 file HTML.
- **IF** cần xem VR (Meta Quest) **THEN** bật plugin `webvr.xml`/`webvr2.xml` + đảm bảo `customimage[vr].size` đã sinh; tắt post-processing nặng trong VR (`webvr="2"`).

---

## WX Use-Case Templates (viết cả 4; ⭐ = worked example)

### ⭐ 1. Product Showcase Tour (mặc định)
Trưng bày sản phẩm defense cho khách/BQP.
- Skin: `vtourskin` + thumbnails; bật **Little Planet Intro** (`littleplanetintro=true` trong `tour.xml`) cho mở màn ấn tượng. [NLM query2 cite 2]
- Hotspot info (`type=image` + tooltip) chú thích tính năng; hotspot điều hướng giữa các góc sản phẩm.
- Deploy: self-hosted nội bộ (nếu showcase đã duyệt công khai) HOẶC `.exe` mang đi hội chợ.
- **Phân loại:** chỉ dùng ảnh sản phẩm đã được duyệt lộ.

### 2. Offline BQP Demo Kiosk
- Đóng gói **NW.js `.exe`** — double-click chạy, không cần mạng/trình duyệt.
- Fullscreen, ẩn toolbar (`package.json` → `"toolbar": false`).
- Chạy trên máy kiosk air-gapped tại phòng demo.

### 3. Facility As-Built Documentation
- Chụp toàn bộ phân xưởng/dây chuyền theo lưới điểm; mỗi trạm = 1 scene + hotspot điều hướng theo sơ đồ mặt bằng.
- Bật plugin **FloorPlan** (bản đồ 2D + radar-cone chỉ hướng nhìn) — cần key `key_flpl.xml` gắn theo email đăng ký krpano. [NLM query2 cite 22]
- **Phân loại:** thường HẠN CHẾ → self-hosted nội bộ / offline. Bản ghi as-built, không lộ ra ngoài.

### 4. VR Training Walkthrough
- Bật `webvr.xml` (head tracking, gaze cursor, controller). Scale đúng: trong 3D-model 1 unit = 1cm (quan trọng cho cảm giác VR). [NLM query2 cite 19]
- Hotspot gaze-activated dẫn học viên qua quy trình vận hành khí tài.
- Tối ưu mobile VR: `display.framebufferscale`, tắt shader nặng khi phát hiện HMD.

---

## Deployment Modes (OFFLINE-FIRST)

| Mode | Khi dùng | Cách làm | Air-gap? |
|------|----------|----------|:---:|
| **NW.js standalone `.exe`** ⭐ | Kiosk / bàn giao khách / MẬT | Cấu trúc: `package.json` (`"main":"vtour/tour.html"`, `window`) + `nw.exe` + thư mục `vtour/`. Mac: đặt vào `app.nw/` trong `/Contents/Resources/`. Đổi tên `nw.exe` tuỳ ý. | ✅ Hoàn toàn |
| **Self-hosted static** | Server/LAN nội bộ Xưởng | Copy `vtour/` lên web server nội bộ; truy cập qua `http://`. | ✅ Nếu LAN kín |
| **Localhost testing server** | Xem thử khi phát triển | `krpanotools testserver` → `http://localhost:8090`. | ✅ |
| **Inline base64 1-file HTML** | Dự án cực nhỏ | Nhúng XML/JS/ảnh dạng data-URL vào 1 file HTML → bypass chặn `file://`. | ✅ |
| ~~Cloud tour host~~ | ❌ CẤM cho nội dung defense | — | — |

---

## Licensing (thực thi trên máy Xưởng)

- **Đăng ký:** `krpanotools register "<LICENSE_KEY>"` (bind theo domain khi host web). `register show` / `register remove` để xem/gỡ. [NLM cite 66/67]
- **Headless / CI Linux:** compiler tìm license theo thứ tự: `~/.krpanolicense` (home) → cùng thư mục executable → thư mục làm việc. **KHÔNG copy tay file license binary** (làm hỏng xác thực mật mã → build fail). [NLM: deep report §License]
- **Dùng license một lần cho 1 call** (không đăng ký lên máy): tham số `-license=<key>`; ép buộc phải có license: `-needlicense`. [NLM query2 cite 6]
- Bản **chưa đăng ký** = có watermark + giới hạn → chỉ để dev, không giao khách.

---

## Quality Criteria — checklist "production-ready"

- [ ] Multires đúng: `tilesize` hợp lý (512), có bản VR (`customimage[vr].size=1536`), preview sinh đủ.
- [ ] Mọi scene liên kết được — không hotspot điều hướng nào chết (`loadscene` đúng tên scene).
- [ ] Không watermark (đã `register`).
- [ ] Chạy tốt trên desktop + mobile (WebGL); có fallback nếu cần thiết bị cũ.
- [ ] View khởi tạo (`hlookat/vlookat/fov`) mỗi scene hợp lý, không nhìn vào nadir/zenith.
- [ ] Hiệu năng: chỉ tile cần thiết được tải; không lỗi context WebGL trên iOS (chú ý ceiling ~40MB tile).
- [ ] `tour_editor.html` + file backup đã XOÁ trước khi giao.
- [ ] Đúng chế độ deploy theo phân loại Step 0 (MẬT → `.exe` offline).
- [ ] VR (nếu có): scale đúng (1 unit = 1cm), shader nặng tắt trong HMD.

---

## Failure Modes / Gotchas

1. **Mở `file://` trực tiếp = màn đen.** Trình duyệt chặn nạp XML/JS/ảnh cục bộ (cross-origin). **Giải:** localhost server (`testserver`), hoặc NW.js `.exe`, hoặc inline base64. KHÔNG hướng dẫn khách "mở tour.html". [NLM: docu/localusage]
2. **Watermark khi giao khách.** Quên `register` → tour dính chữ krpano. Luôn đăng ký trước bàn giao.
3. **Tên scene/element bắt đầu bằng SỐ = hỏng.** Parser hiểu số là array-index. Tên phải bắt đầu bằng chữ cái; tên tự chuẩn hoá về chữ thường. [NLM: deep report §XML Array Rule]
4. **Truy cập krpano từ JS quá sớm = race condition.** `DOMContentLoaded` không đảm bảo viewer đã sẵn sàng. Dùng callback `onready` (hoặc sự kiện `onxmlcomplete`). [NLM: deep report §Scoping]
5. **Cube nhận diện sai mặt.** Thiếu hậu tố `_l/_f/_r/_b/_u/_d` → ghép cube sai. Đặt tên đúng trước khi makepano.
6. **iOS reload/crash tour lớn.** Vượt ceiling bộ nhớ texture WebGL (mặc định ~40MB tile trên iOS). Chỉnh `maxmem`, `multiresthreshold`; đừng nhồi pano quá lớn cho mobile. [NLM: forum iphone offline]
7. **Rò WebGL context.** Nhiều viewer/điều hướng SPA không `removepano()`/`.unload()` → hết context (~8/trang). Luôn giải phóng viewer cũ.
8. **vtoureditor.swf là Flash — đã chết.** Đừng phụ thuộc GUI editor Flash cũ; sửa `tour.xml` bằng text/скрипт trực tiếp (đúng tinh thần agentic).

---

## NLM Reference

- **Notebook:** `krpano` (`e041cc65-742c-4734-a346-4b0171187754`) — 24 nguồn: krpano.com official docs (XML, actions, JS interface, plugin interface, embedpano, tools/config, droplets, panoformats, localusage, download, releasenotes, examples), plugin WebVR/vtoureditor/floorplan/autotour, vrtourviewer, config template thật, 2 tutorial video, positioning intel.
- **Deep-research synthesis:** `RESEARCH` output — "Architectural Reference & Engineering Manual for the krpano Immersive Engine" (48.9K, 40 cited sources).
- Hỏi notebook khi cần tra cứu tham số chính xác: `nlm notebook query krpano "<câu hỏi>"`.

---

## COD Classification

| Task | COD | Ghi chú |
|------|-----|---------|
| Phân loại nội dung (Step 0) | **C** | CEO xác nhận MẬT/HẠN-CHẾ/THƯỜNG |
| Chụp/chuẩn bị ảnh 360 | C/O | Người chụp; AI hướng dẫn |
| Sinh multires vtour (makepano/droplet) | O | Cơ học, scriptable |
| Viết scene/hotspot/điều hướng XML | O | AI scaffold, người duyệt bố cục |
| Chọn chế độ deploy | **C** | Ràng buộc bởi phân loại |
| Đăng ký license | O | `register` trên máy Xưởng |
| Nghiệm thu chất lượng | **C** | CEO/quản đốc duyệt trước giao |

---

## Rules

- **OFFLINE-FIRST tuyệt đối** — nội dung defense không bao giờ lên host tour đám mây. MẬT → chỉ `.exe` air-gapped.
- **Security Gate (Step 0) KHÔNG skip** — phân loại trước khi chụp.
- **Đăng ký license trước khi giao** — không giao bản watermark.
- **Không mở `file://`** — luôn testserver / `.exe` / inline.
- **Sửa XML bằng code, không phụ thuộc Flash GUI đã chết.**
- **Xoá `tour_editor.html` + backup trước khi bàn giao.**
- **Bổ trợ, không trùng:** `wx-krpano` (tour immersive) ⟂ `wx-diagram` (sơ đồ tĩnh) ⟂ `helix-draw` (phác thảo nội bộ).
