# QTCN — Bộ quy tắc công nghệ (Engineering Rules Reference)

Tri thức công nghệ để soạn từng nguyên công cho **đúng và an toàn**. Áp dụng theo loại mối ghép / thao tác. Mọi con số là **định hướng** — chốt theo bản vẽ & tiêu chuẩn áp dụng.

---

## 0. Nguyên tắc vàng của lắp ráp kết cấu

> **GÁ LỎNG → CĂN CHỈNH → SIẾT CHẶT.** Không bao giờ siết lực trước khi căn chỉnh xong cả cụm.

1. **Gá lỏng (vặn tay / siết nhẹ):** lắp toàn bộ bu lông của một cụm ở trạng thái còn độ rơ tự do, để có thể xê dịch căn chỉnh. In đậm quy tắc "**tuyệt đối chưa siết chặt ở nguyên công này**" trong các nguyên công gá lỏng.
2. **Căn chỉnh hình học** trước khi siết:
   - **Đồng tâm** lỗ bích: dùng **chốt côn rà lỗ** (mũi đột Ø10÷Ø12), **không dùng ngón tay**.
   - **Vuông góc** khung: đo **chéo hai góc đối diện**, hiệu hai đường chéo $\Delta \le 5\text{mm}$ (chống méo hình bình hành).
   - **Phẳng**: thước thủy (nivo).
   - **Thẳng đứng** cột/cánh: nivo có từ tính theo hai phương vuông góc, sai lệch $\le 5\text{mm}$ trên toàn chiều cao (hoặc góc lệch $\le 0.5^\circ$).
   - **Song song / khoảng cách tâm**: đo bằng thước cuộn tại **cả hai đầu** (vd tâm 2 phao $1530 \pm 10\text{mm}$).
3. **Siết chặt lực** sau cùng — xem §1.

---

## 1. Mối ghép bu lông

### 1.1 Bộ đệm chống tự nới lỏng (BẮT BUỘC ngoài trời / biển)
Mỗi bộ liên kết dùng đầy đủ: **01 đệm phẳng đầu bu lông + 01 đệm phẳng phía đai ốc + 01 đệm vênh sát đai ốc**. Lý do: rung động tuần hoàn của sóng/gió làm tự nới lỏng. ⇒ với 1 mối: 2 đệm phẳng + 1 đệm vênh. (Kiểm tra SL khi lập danh mục: N mối ⇒ 2N đệm phẳng + N đệm vênh.)

### 1.2 Mô-men siết (tham chiếu — CHỐT theo cấp bền & bản vẽ)
| Ren | Cấp bền | Mô-men siết tham chiếu | Ghi chú |
|-----|---------|------------------------|---------|
| M6  | 8.8 | ~9 ÷ 10 Nm | bích đèn, phụ kiện nhỏ |
| M10 | 5.6 | ~25 ÷ 30 Nm | bích chân cánh (giá trị thấp do cấp bền thấp) |
| M10 | 8.8 | ~43 ÷ 50 Nm | |
| M12 | 5.6 | ~30 ÷ 35 Nm | |
| M12 | 8.8 | ~45 ÷ 55 Nm | bích chân cột, dầm |
**Cảnh báo:** mô-men phụ thuộc **cấp bền, bôi trơn, loại mối ghép** — bảng chỉ để khởi điểm. Luôn ghi rõ cấp bền trong nguyên công và lấy số cuối từ thiết kế. Siết bằng **cờ lê lực (cờ lê cân lực)**, chọn dải đo bao trùm giá trị (vd 20÷100 Nm, 10÷60 Nm).

### 1.3 Trình tự & dấu kiểm
- Siết **đối xứng (chữ X), từ giữa ra hai đầu** để phân bố đều ứng suất.
- Siết theo **bước**: cụm gần trước (vd dầm ngang–tai phao 48 bộ) → cụm xa (dầm dọc–dầm ngang 12 bộ).
- Sau siết: **vạch sơn phấn màu** thẳng hàng từ đầu bu lông qua đai ốc → kiểm tra trực quan độ nới lỏng về sau.

---

## 2. Cáp chằng + tăng đơ (rigging)

1. **Cáp:** thép bọc nhựa Ø6 (kiểm tra lớp bọc không rách/hở lõi). Cắt sẵn theo chiều dài thiết kế dưới mặt đất.
2. **Đầu cáp:** tạo **vòng khuyên (lá khế / thimble)** chống gãy gập tại điểm móc; liên kết bằng **ma ní D10** (vặn chặt chốt + siết thêm 1/4 vòng + **dây kẽm khóa chốt** chống tự xoay do gió).
3. **Cóc kẹp cáp:** **02 cóc M6** mỗi đầu dây, khoảng cách $50 \div 80\text{mm}$. **Quy tắc hướng:** thân chữ U ôm **đầu dây tự do (đuôi ngắn)**, đế yên ngựa ôm **nhánh dây chịu lực (chính)**. Siết đều, không làm dập lớp bọc nhựa. ("Never saddle a dead horse".)
4. **Tăng đơ M12:** xoay căng đều các dây đối xứng (độ võng giữa dây $\le 10\text{mm}$ dưới lực kéo tay). Sau khi đạt: siết đai ốc khóa (locknut) + **xỏ dây thép mạ kẽm Ø1.5÷2.0 xoắn khóa** chống tự xoay do rung động sóng/gió.
5. Trình tự: lắp sẵn cáp + cóc **dưới mặt đất** (NC chuẩn bị) → móc tăng đơ căng sơ bộ khi dựng → hiệu chỉnh lực căng & khóa ở nguyên công riêng cuối.

---

## 3. Nâng hạ & dựng cột / cụm lớn

- Móc cẩu vào **tai cẩu** thiết kế; hướng móc dọc theo hướng lắp (vd dọc dầm dọc).
- ≥ **02 dây mồi giữ hướng** (dây dù Ø10, dài ~10m) để công nhân dưới đất điều hướng, tránh va đập.
- Dùng **dây cáp cẩu vải (sling)** tải ≥ 1 tấn; cẩu tự hành hoặc pa lăng ba chân sức nâng ≥ 500kg.
- **Chỉ tháo móc cẩu sau khi** cụm đã tự đứng vững an toàn (đủ bu lông chân + căng sơ bộ dây chằng). **Cấm dựng cột bằng tay; không đứng dưới tầm treo.**

---

## 4. Hệ điện DC (đèn LED, ắc quy, đèn báo hiệu)

1. **Đi dây & bảo vệ:** luồn dây nguồn trong **ống ruột gà Ø16**, cố định thân cột bằng **lạt nhựa đen chịu thời tiết** (khoảng cách 200÷250mm); LED đi quanh viền cánh, kéo căng phẳng, lạt nhựa 200mm, cắt sát chân đuôi thừa.
2. **Ắc quy:** 12V–35Ah đặt khay chuyên dụng ở mũi phao; đai kẹp + bu lông giữ chống xê dịch/lật khi sóng.
3. **Đấu nối:** đầu **cosse ép chặt**; đúng cực tính (**+ đỏ trước, − xanh/đen sau**); đo VOM hở tải **12 ÷ 12.8 V**.
4. **Chống nước IP67 (BẮT BUỘC ngoài trời):** mọi mối nối & đầu cực bọc kín bằng **băng keo tự co chống nước** (hoặc ống co nhiệt có keo). Bôi **mỡ Vaseline kỹ thuật** đầu cực chống ăn mòn.
5. **Thử nghiệm:** bật liên tục ≥ 15 phút — LED & đèn báo hiệu ổn định, không chập chờn, không phát nhiệt bất thường tại đầu nối.

---

## 5. Định mức & phân công

- **Bậc thợ:** mặc định 4/7 cho lắp ráp kết cấu; nâng yêu cầu khi có kỹ thuật điện DC (vd 4/7 + hiểu biết điện một chiều). Việc hàn/NDT cần bậc + chứng chỉ cao hơn.
- **Định mức thời gian:** ước lượng theo độ phức tạp (kiểm tra ~30', kê/đặt ~20', gá lắp 1 cụm ~25÷45', dựng cột ~40', lắp 3 cánh ~90', đấu điện ~50'). Hiệu chỉnh theo thực tế xưởng.
- **Nơi thực hiện:** khu tập kết/chuẩn bị (kiểm tra, cắt cáp) vs bãi lắp dựng ngoài trời (lắp ráp chính).

---

## 6. Danh mục thiết bị, trang bị công nghệ (tooling catalog)

- **Đo & kiểm:** thước cặp 0÷300, thước cuộn thép 5m, **nivo (thước thủy) 300mm có từ tính**, dưỡng đo ren M10/M12, đồng hồ vạn năng (VOM), cờ lê lực (dải 10÷60 và 20÷100 Nm).
- **Siết / lắp:** cờ lê hai đầu vòng miệng (16/17/18/19mm tùy ren), mỏ lết 10", tua vít, **chốt côn rà lỗ** Ø10÷12, búa đồng / búa cao su.
- **Cáp & điện:** kìm cắt cáp chuyên dụng, kìm răng, kìm ép cosse, kìm cắt dây.
- **Nâng & cao:** cẩu tự hành / pa lăng ba chân, sling vải ≥1T, dây mồi Ø10, thang chữ A (≥2.0m / ≥3.0m), **dây đai an toàn**.
- **BHLĐ:** găng tay bảo hộ (loại chống cắt khi thao tác cáp), giày, mũ.
- **Tiêu hao:** phấn màu đánh dấu, dây kẽm khóa chốt, lạt nhựa chịu thời tiết, băng keo tự co, mỡ Vaseline, giẻ lau.

---

## 7. Flow Optimization — heuristics tối ưu dòng công nghệ

1. **Gá lỏng cả khung → căn chỉnh tổng thể → siết một lượt.** Tách "căn thẳng đứng & siết bích" thành nguyên công riêng để siết đúng lực sau khi hình học đã chuẩn.
2. **Chuẩn bị dưới mặt đất trước khi lên cao:** cắt/bấm cáp, lắp sẵn cóc cáp + dây chằng vào cột & cánh; **lắp đèn báo hiệu + luồn ống bảo vệ lên cụm trước khi dựng** → giảm thao tác trên cao, tối ưu tải & an toàn.
3. **Gộp nguyên công** trùng vị trí/đồ gá (vd gộp "lắp sẵn dây chằng cột" và "lắp sẵn dây chằng cánh" thành 1 NC chuẩn bị).
4. **Phân bố tải đối xứng:** lắp chi tiết quanh tâm theo trình tự đối xứng (cánh 1→2→3→4 theo chiều kim đồng hồ) tránh lệch tâm gây lật/nghiêng cụm trên phao.
5. **Bắt đầu bằng kiểm tra đầu vào**, kết thúc bằng **kiểm tra tổng thể + thử điện 15' + vệ sinh + nghiệm thu/bàn giao**.
6. Sau tối ưu, lập **Bảng tổng hợp tiến trình** để soát logic trước khi viết chi tiết.

---

## 8. Khung nguyên công cho QTCN GIA CÔNG cắt gọt (khi không phải lắp ráp)

Nếu sản phẩm là chi tiết gia công (không phải lắp ráp cụm), mỗi nguyên công đổi trục thông tin:
- **Yêu cầu kỹ thuật:** chuẩn định vị & kẹp chặt, máy/đồ gá, dao/mảnh dao, **chế độ cắt** (v, s, t), dung sai & độ nhám đạt (Ra/Rz), dung dịch trơn nguội.
- **Định mức:** bậc thợ, thời gian máy + thời gian phụ, máy thực hiện.
- **Vật tư + thiết bị:** phôi, dao cụ, dụng cụ đo (panme, calip, dưỡng).
- Trình tự chuẩn: phôi → gia công thô → gia công tinh → nhiệt luyện (nếu có) → mài/hoàn thiện → kiểm tra. Tham chiếu thêm `helix-detail-finalize` và `verify`.

---

## 9. Minh họa CAD cho từng nguyên công (khi chạy `--cad`)

Mục tiêu: mỗi nguyên công có **một hình minh họa** giúp thợ hiểu ngay thao tác. Skill **KHÔNG vẽ hình** — skill **đặc tả hình cần vẽ** (figure spec) để họa viên dựng trong CAD (AutoCAD/Inventor/SolidWorks) rồi chèn ảnh vào tài liệu. Một hình đúng thay được nhiều dòng chữ và giảm sai thao tác.

### 9.1 Chọn loại hình theo bản chất nguyên công
| Bản chất nguyên công | Loại hình đề xuất | Nội dung bắt buộc thể hiện |
|----------------------|-------------------|----------------------------|
| Kiểm tra chi tiết | Ảnh/hình chi tiết + vùng đo đánh dấu | vị trí đo, dụng cụ, ngưỡng dung sai (vd ±1 mm), điểm đo điện áp |
| Kê / định vị cụm (kê phao) | Hình chiếu bằng + chiếu đứng | khoảng cách tâm (vd 1530), vị trí đế kê cách đầu (vd 800), quy ước mũi/đuôi, trái/phải |
| Gá lắp mối bu lông | Hình cắt trích (detail bubble) phóng to + exploded | thứ tự xếp: đầu bu lông–đệm phẳng–chi tiết–đệm phẳng–**đệm vênh**–đai ốc; callout ren×dài (M12×40); hướng xỏ bu lông |
| Căn chỉnh & siết lực | Sơ đồ trình tự siết đánh số (chữ X) | số thứ tự siết, chiều đối xứng từ giữa ra hai đầu, giá trị mô-men, vị trí vạch sơn kiểm |
| Cáp chằng + tăng đơ | Detail cóc cáp + ma ní + vòng khuyên | **hướng yên ngựa** (đế ôm nhánh chịu lực, chữ U ôm đuôi tự do), khoảng cách 2 cóc 50–80, lá khế, dây kẽm khóa chốt |
| Nâng dựng cột / cụm lớn | Sơ đồ nâng (rigging diagram) | điểm móc tai cẩu, hướng/góc sling, ≥2 dây mồi, **vùng cấm đứng dưới tầm treo** |
| Lắp chi tiết đối xứng (cánh) | Hình chiếu bằng đánh số 1→2→3→4 | trình tự chiều kim đồng hồ, khe hở giữa cánh, tâm đối xứng |
| Hệ điện DC | Sơ đồ đấu nối + đường đi dây | cực +/− (đỏ/đen), đường LED quanh viền cánh, ống ruột gà, điểm bọc kín IP67 |
| Thử nổi (hạ thủy) | Hình chiếu đứng có đường nước | đường mớn nước, Tp (vd ≈0,25 m), Hp dự trữ, tư thế cân bằng |

### 9.2 Quy ước trình bày
- **Ballooned assembly:** đánh số bóng (balloon) **trùng mã VT/pos** trong BOM để tra chéo.
- **Exploded view** cho mối ghép nhiều lớp đệm; **detail bubble (I, II…)** phóng to chi tiết nhỏ (cóc cáp, bộ đệm).
- **Callout** ghi đúng thông số nguyên công (lực siết, dung sai, quy cách, bước) — **con số phải khớp mục I. YCKT**; lệch số = lỗi.
- **Nguồn:** ưu tiên **trích từ bản vẽ chế tạo có sẵn** (vd 19.BM-01.xx.xx) — ghi mã bản vẽ; nếu phải dựng mới ghi rõ "dựng mới".
- **Mã hình:** `H-<mã nguyên công>` (vd `H-B3`), đánh số figure liên tục; MD chèn tại chỗ `[ẢNH: chèn hình H-B3]`, file hình để trong `figures/`.
- Một nguyên công phức tạp có thể cần >1 hình (vd B7 dựng cột: 1 sơ đồ nâng + 1 detail chân bích) — đánh `H-B7a`, `H-B7b`.
