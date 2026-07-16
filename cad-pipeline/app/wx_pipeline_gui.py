#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wx_pipeline_gui.py — Phần mềm điều khiển tổng thể CAD Pipeline Workshop X

LỚP VỎ (không phải lõi): mỗi nút chỉ gọi lại đúng script trong
cad-pipeline/scripts/extract/ qua subprocess — toàn bộ adapter/sensor/gate đã
field-test giữ nguyên. GUI chỉ: dựng lệnh, chạy nền, in output, tô màu exit code.

Chạy:  python cad-pipeline/app/wx_pipeline_gui.py   (hoặc bấm đúp WX_Pipeline.bat)
Yêu cầu: chỉ cần Python có Tkinter (bản chuẩn Windows đã có sẵn). FreeCAD/Inventor
chỉ cần cho các nút tương ứng — thiếu thì nút đó báo lỗi rõ, không làm sập app.

An ninh: chạy hoàn toàn local, không mở cổng mạng, read-only với file CAD gốc.
File MẬT xử lý trên máy nội bộ như mọi khi — GUI không đổi vùng lưu trữ.
"""
import os
import sys
import queue
import threading
import subprocess

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# ── Đường dẫn (tính từ vị trí file này: cad-pipeline/app/…) ───────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.normpath(os.path.join(HERE, ".."))                 # cad-pipeline/
EXTRACT = os.path.join(CAD, "scripts", "extract")
INVENTOR = os.path.join(CAD, "scripts", "inventor")
GOLDEN_STEP = os.path.join(CAD, "golden", "step")
PY = sys.executable or "python"
FREECADCMD = os.environ.get(
    "FREECADCMD", r"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe")

EXT_RULE = os.path.join(INVENTOR, "Export_QTCN_Package.iLogic.vb")


def sx(name):
    return os.path.join(EXTRACT, name)


# Ý nghĩa exit code (đồng bộ HD-00 §3) → (nhãn, màu)
EXIT_MEANING = {
    0: ("ĐẠT", "#1a7f37"),
    1: ("ĐẠT — có WARNING (đọc danh sách)", "#b26a00"),
    2: ("FAIL — gate chặn, KHÔNG đi tiếp", "#b3261e"),
    3: ("Lỗi môi trường / thiếu đầu vào", "#b3261e"),
    4: ("Merge từ chối seed (chưa validate/cũ/FAIL)", "#b3261e"),
    127: ("Không tìm thấy chương trình (kiểm đường dẫn)", "#b3261e"),
}


class Runner:
    """Chạy 1 lệnh nền, đẩy output + kết quả qua queue về GUI (thread-safe)."""

    def __init__(self, q):
        self.q = q
        self.proc = None

    def busy(self):
        return self.proc is not None and self.proc.poll() is None

    def run(self, cmd, env_extra=None, cwd=None, on_done=None):
        if self.busy():
            messagebox.showwarning("Đang chạy",
                                   "Một tác vụ đang chạy — chờ xong rồi thử lại.")
            return
        self.q.put(("clear", None))
        shown = " ".join(('"%s"' % c if " " in c else c) for c in cmd)
        self.q.put(("log", "$ " + shown + "\n"))
        t = threading.Thread(target=self._worker,
                             args=(cmd, env_extra, cwd, on_done), daemon=True)
        t.start()

    def _worker(self, cmd, env_extra, cwd, on_done):
        env = dict(os.environ)
        if env_extra:
            env.update(env_extra)
        try:
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                env=env, cwd=cwd, bufsize=1)
            for line in self.proc.stdout:
                self.q.put(("log", line))
            rc = self.proc.wait()
        except FileNotFoundError as e:
            self.q.put(("log", "\n[LỖI] Không tìm thấy chương trình:\n  %s\n" % e))
            rc = 127
        except Exception as e:  # noqa: BLE001 — báo mọi lỗi ra console, không sập app
            self.q.put(("log", "\n[LỖI] %s: %s\n" % (type(e).__name__, e)))
            rc = 3
        finally:
            self.proc = None
        self.q.put(("status", rc))
        if on_done:
            self.q.put(("done", (rc, on_done)))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WX CAD PIPELINE — điều khiển tổng thể")
        self.geometry("980x720")
        self.minsize(820, 600)
        self.q = queue.Queue()
        self.runner = Runner(self.q)
        self.vars = {}                         # StringVar/BooleanVar theo key
        self._build()
        self.after(80, self._pump)

    # ── tiện ích dựng UI ─────────────────────────────────────────────────────
    def var(self, key, default="", boolean=False):
        if key not in self.vars:
            self.vars[key] = tk.BooleanVar(value=bool(default)) if boolean \
                else tk.StringVar(value=default)
        return self.vars[key]

    def path_row(self, parent, label, key, kind="file", filetypes=None):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=3)
        ttk.Label(row, text=label, width=18).pack(side="left")
        ttk.Entry(row, textvariable=self.var(key)).pack(
            side="left", fill="x", expand=True)

        def browse():
            if kind == "dir":
                p = filedialog.askdirectory()
            else:
                p = filedialog.askopenfilename(
                    filetypes=filetypes or [("Tất cả", "*.*")])
            if p:
                self.var(key).set(p)
        ttk.Button(row, text="Chọn…", width=7, command=browse).pack(
            side="left", padx=3)
        return row

    def action(self, parent, text, fn):
        ttk.Button(parent, text=text, command=fn).pack(
            fill="x", pady=4, ipady=3)

    def section(self, parent, title):
        lf = ttk.LabelFrame(parent, text=title, padding=10)
        lf.pack(fill="x", padx=10, pady=8)
        return lf

    # ── chạy lệnh, có kiểm đầu vào ───────────────────────────────────────────
    def need(self, *keys):
        for k in keys:
            if not self.var(k).get().strip():
                messagebox.showwarning("Thiếu đầu vào",
                                       "Hãy chọn đầy đủ đường dẫn trước khi chạy.")
                return False
        return True

    def go(self, cmd, **kw):
        self.runner.run(cmd, **kw)

    # ── các tab ──────────────────────────────────────────────────────────────
    def _build(self):
        top = ttk.Frame(self, padding=(10, 8, 10, 0))
        top.pack(fill="x")
        ttk.Label(top, text="1 nguồn CAD → 5 đầu ra · harness 3 tầng · "
                  "chạy local, read-only",
                  font=("Segoe UI", 9, "italic")).pack(side="left")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        for name, builder in [
            ("Thiết kế", self._tab_design),
            ("KS công nghệ", self._tab_ks),
            ("QC / Gate", self._tab_qc),
            ("Đầu ra AI", self._tab_ai),
            ("Xưởng", self._tab_shop),
            ("CEO", self._tab_ceo),
        ]:
            f = ttk.Frame(nb)
            nb.add(f, text=name)
            builder(f)

        # ── console + status (luôn hiện) ──
        bottom = ttk.Frame(self, padding=(8, 0, 8, 8))
        bottom.pack(fill="both", expand=False)
        bar = ttk.Frame(bottom)
        bar.pack(fill="x")
        self.status = tk.Label(bar, text="Sẵn sàng", anchor="w",
                               font=("Segoe UI", 10, "bold"), fg="#444")
        self.status.pack(side="left", fill="x", expand=True)
        ttk.Button(bar, text="Xóa màn hình",
                   command=lambda: self._set_console("")).pack(side="right")
        self.console = scrolledtext.ScrolledText(
            bottom, height=15, font=("Consolas", 9), wrap="word",
            bg="#0f1115", fg="#d6d6d6", insertbackground="#d6d6d6")
        self.console.pack(fill="both", expand=True, pady=(4, 0))
        self.console.configure(state="disabled")

    def _tab_design(self, f):
        s = self.section(f, "Kiểm model / bản vẽ (HD-01, HD-03)")
        self.path_row(s, "File .ipt/.iam", "d_file",
                      filetypes=[("Inventor", "*.ipt *.iam"), ("Tất cả", "*.*")])
        ttk.Checkbutton(s, text="Kèm xuất giao-viec.csv (gửi bên thiết kế)",
                        variable=self.var("d_ticket", boolean=True)).pack(
            anchor="w", pady=2)
        self.action(s, "▶ Kiểm bản vẽ (drawing_check)", self._run_drawing)

        s2 = self.section(f, "Model Rhino vỏ nhôm (HU)")
        self.path_row(s2, "File .3dm", "rh_file",
                      filetypes=[("Rhino", "*.3dm"), ("Tất cả", "*.*")])
        self.action(s2, "▶ Kiểm Rhino (rhino_check)", self._run_rhino)

        s3 = self.section(f, "Export gói QTCN — chạy TRONG Inventor")
        ttk.Label(s3, wraplength=880, justify="left", text=(
            "Bước này là External Rule chạy trong Inventor (không gọi từ đây được).\n"
            "Manage → iLogic → External Rules → Add → trỏ file dưới, rồi Run trên .iam:")
        ).pack(anchor="w")
        row = ttk.Frame(s3)
        row.pack(fill="x", pady=4)
        ttk.Entry(row, textvariable=self.var("ext_rule", EXT_RULE)).pack(
            side="left", fill="x", expand=True)
        ttk.Button(row, text="Chép đường dẫn", command=self._copy_rule).pack(
            side="left", padx=3)

    def _tab_ks(self, f):
        s = self.section(f, "Trích xuất MỘT LỆNH (HD-02)")
        self.path_row(s, "Thư mục _QTCN_export", "k_dir", kind="dir")
        opt = ttk.Frame(s)
        opt.pack(fill="x", pady=2)
        ttk.Checkbutton(opt, text="--release (phát hành: bắt buộc kiểm chéo 2 nguồn)",
                        variable=self.var("k_release", boolean=True)).pack(anchor="w")
        ttk.Checkbutton(opt, text="--force (đi tiếp qua FAIL — chỉ để chẩn đoán)",
                        variable=self.var("k_force", boolean=True)).pack(anchor="w")
        self.action(s, "▶ Chạy trích xuất (run_pipeline)", self._run_pipeline)

        s2 = self.section(f, "Kiểm lẻ khi cần chẩn đoán")
        self.path_row(s2, "Seed cần kiểm", "v_seed",
                      filetypes=[("JSON", "*.json")])
        self.action(s2, "▶ Kiểm 1 seed (validate S1–S4)", self._run_validate)
        self.path_row(s2, "Seed nguồn A", "c_a", filetypes=[("JSON", "*.json")])
        self.path_row(s2, "Seed nguồn B", "c_b", filetypes=[("JSON", "*.json")])
        self.action(s2, "▶ Kiểm chéo 2 nguồn (S2)", self._run_cross)

        s3 = self.section(f, "Chiều dài hàn (cần FreeCAD)")
        self.path_row(s3, "File .step", "w_step",
                      filetypes=[("STEP", "*.step *.stp"), ("Tất cả", "*.*")])
        self.action(s3, "▶ Ước lượng chiều dài hàn (weld_length)", self._run_weld)

    def _tab_qc(self, f):
        s = self.section(f, "Golden set G3 — hồi quy (HD-04)")
        ttk.Label(s, text="Chạy lại bộ đáp án chuẩn (golden/step) — phải khớp 100%."
                  ).pack(anchor="w")
        self.action(s, "▶ Kiểm golden G3", self._run_golden)

        s2 = self.section(f, "Tự kiểm toàn bộ harness (battery)")
        ttk.Checkbutton(s2, text="--regen (trích lại golden STEP — cần FreeCAD)",
                        variable=self.var("b_regen", boolean=True)).pack(anchor="w")
        self.action(s2, "▶ Chạy battery (phải ĐẠT 8/8)", self._run_battery)

        s3 = self.section(f, "Kiểm môi trường")
        ttk.Label(s3, text="Kiểm Python, thư viện, FreeCAD, đường dẫn script."
                  ).pack(anchor="w")
        self.action(s3, "▶ Kiểm môi trường", self._run_envcheck)

    def _tab_ai(self, f):
        s = self.section(f, "Kiểm số tài liệu AI sinh (HD-05, tầng 3)")
        ttk.Label(s, wraplength=880, justify="left", text=(
            "Mọi số CÓ ĐƠN VỊ trong tài liệu AI phải truy được về seed. "
            "Exit 2 = có số mồ côi → KHÔNG trình duyệt.")).pack(anchor="w", pady=2)
        self.path_row(s, "Tài liệu .md/.txt", "t_doc",
                      filetypes=[("Văn bản", "*.md *.txt"), ("Tất cả", "*.*")])
        self.path_row(s, "Seed nguồn 1", "t_seed1", filetypes=[("JSON", "*.json")])
        self.path_row(s, "Seed nguồn 2 (tùy chọn)", "t_seed2",
                      filetypes=[("JSON", "*.json")])
        self.action(s, "▶ Kiểm số (trace_numbers)", self._run_trace)

    def _tab_shop(self, f):
        s = self.section(f, "Ghi số liệu thật từ xưởng (HD-06)")
        self.path_row(s, "Sổ actuals .jsonl", "a_file",
                      filetypes=[("JSONL", "*.jsonl"), ("Tất cả", "*.*")])
        self.path_row(s, "File record .json", "a_rec",
                      filetypes=[("JSON", "*.json")])
        self.action(s, "▶ Ghi 1 record (--add-file)", self._run_actual_add)

        s2 = self.section(f, "Báo cáo hệ số hiệu chỉnh")
        ttk.Label(s2, text="Đọc cả sổ → calibration.json (đầu vào cho định mức sau)."
                  ).pack(anchor="w")
        self.action(s2, "▶ Báo cáo hiệu chỉnh (--report)", self._run_actual_report)

    def _tab_ceo(self, f):
        s = self.section(f, "Dashboard toàn cục (HD-02 §5)")
        self.path_row(s, "Thư mục gốc _QTCN_export", "ceo_root", kind="dir")
        self.action(s, "▶ Sinh dashboard", self._run_dashboard)
        ttk.Button(s, text="Mở dashboard.md", command=self._open_dashboard).pack(
            fill="x", pady=4, ipady=3)

    # ── handlers: mỗi cái dựng cmd rồi self.go(...) ─────────────────────────
    def _run_drawing(self):
        if not self.need("d_file"):
            return
        cmd = [PY, sx("drawing_check.py"), "--file", self.var("d_file").get()]
        if self.var("d_ticket", boolean=True).get():
            cmd.append("--ticket")
        self.go(cmd)

    def _run_rhino(self):
        if not self.need("rh_file"):
            return
        self.go([PY, sx("rhino_check.py"), "--file", self.var("rh_file").get()])

    def _copy_rule(self):
        self.clipboard_clear()
        self.clipboard_append(self.var("ext_rule", EXT_RULE).get())
        messagebox.showinfo("Đã chép", "Đã chép đường dẫn External Rule.")

    def _run_pipeline(self):
        if not self.need("k_dir"):
            return
        cmd = [PY, sx("run_pipeline.py"), "--dir", self.var("k_dir").get()]
        if self.var("k_release", boolean=True).get():
            cmd.append("--release")
        if self.var("k_force", boolean=True).get():
            cmd.append("--force")
        self.go(cmd)

    def _run_validate(self):
        if not self.need("v_seed"):
            return
        self.go([PY, sx("validate_qtcn_seed.py"), "--seed", self.var("v_seed").get()])

    def _run_cross(self):
        if not self.need("c_a", "c_b"):
            return
        self.go([PY, sx("validate_qtcn_seed.py"), "--cross",
                 self.var("c_a").get(), self.var("c_b").get()])

    def _run_weld(self):
        if not self.need("w_step"):
            return
        step = self.var("w_step").get()
        self.go([FREECADCMD, sx("weld_length.py")],
                env_extra={"FC_FILE": step, "FC_OUT": os.path.dirname(step)})

    def _run_golden(self):
        self.go([PY, sx("validate_qtcn_seed.py"), "--golden", GOLDEN_STEP])

    def _run_battery(self):
        cmd = [PY, sx("run_battery.py")]
        if self.var("b_regen", boolean=True).get():
            cmd.append("--regen")
        self.go(cmd)

    def _run_envcheck(self):
        code = (
            "import sys;print('Python',sys.version.split()[0],sys.executable)\n"
            "import importlib\n"
            "for m in ['tkinter','jsonschema','openpyxl','rhino3dm','win32com']:\n"
            "    try: importlib.import_module(m);print('  [OK]',m)\n"
            "    except Exception as e: print('  [THIẾU]',m,'-',e)\n"
            "import os;fc=r'%s'\n"
            "print('FreeCAD:', '[OK] '+fc if os.path.exists(fc) else '[THIẾU] '+fc)\n"
            "print('Script extract:', '[OK]' if os.path.isdir(r'%s') else '[THIẾU]', r'%s')\n"
            % (FREECADCMD, EXTRACT, EXTRACT))
        self.go([PY, "-c", code])

    def _run_trace(self):
        if not self.need("t_doc", "t_seed1"):
            return
        cmd = [PY, sx("trace_numbers.py"), "--doc", self.var("t_doc").get(),
               "--seed", self.var("t_seed1").get()]
        if self.var("t_seed2").get().strip():
            cmd += ["--seed", self.var("t_seed2").get()]
        self.go(cmd)

    def _run_actual_add(self):
        if not self.need("a_file", "a_rec"):
            return
        self.go([PY, sx("record_actuals.py"), "--file", self.var("a_file").get(),
                 "--add-file", self.var("a_rec").get()])

    def _run_actual_report(self):
        if not self.need("a_file"):
            return
        out = os.path.join(os.path.dirname(self.var("a_file").get()),
                           "calibration.json")
        self.go([PY, sx("record_actuals.py"), "--file", self.var("a_file").get(),
                 "--report", "--out", out])

    def _run_dashboard(self):
        if not self.need("ceo_root"):
            return
        self.go([PY, sx("pipeline_dashboard.py"), "--root",
                 self.var("ceo_root").get()])

    def _open_dashboard(self):
        root = self.var("ceo_root").get().strip()
        if not root:
            messagebox.showwarning("Thiếu", "Chọn thư mục gốc trước.")
            return
        p = os.path.join(root, "dashboard.md")
        if not os.path.exists(p):
            messagebox.showinfo("Chưa có", "Chưa có dashboard.md — bấm 'Sinh dashboard' trước.")
            return
        try:
            os.startfile(p)  # noqa: S606 — mở bằng app mặc định Windows
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Lỗi mở file", str(e))

    # ── console pump (thread-safe qua queue) ─────────────────────────────────
    def _set_console(self, text):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        if text:
            self.console.insert("end", text)
        self.console.configure(state="disabled")

    def _append(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def _pump(self):
        try:
            while True:
                kind, payload = self.q.get_nowait()
                if kind == "clear":
                    self._set_console("")
                    self.status.config(text="Đang chạy…", fg="#b26a00")
                elif kind == "log":
                    self._append(payload)
                elif kind == "status":
                    label, color = EXIT_MEANING.get(
                        payload, ("Kết thúc (exit %s)" % payload, "#b3261e"))
                    self.status.config(text="exit %d · %s" % (payload, label),
                                       fg=color)
                elif kind == "done":
                    rc, cb = payload
                    try:
                        cb(rc)
                    except Exception:  # noqa: BLE001
                        pass
        except queue.Empty:
            pass
        self.after(80, self._pump)


def main():
    try:
        app = App()
    except tk.TclError as e:
        sys.stderr.write("Không khởi động được giao diện (Tkinter): %s\n" % e)
        sys.exit(3)
    app.mainloop()


if __name__ == "__main__":
    main()
