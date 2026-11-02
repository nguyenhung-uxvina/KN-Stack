"""AutoCAD giả cho test — chỉ mô phỏng các thành viên COM mà bridge dùng (đã đối chiếu trên AutoCAD 2025 thật).

Bơm lỗi: `doc.fail_once("SetLayer")` ⇒ lần tới thao tác đó ném RPC_E_CALL_REJECTED đúng một lần.
Mọi lời gọi ghi lại vào `doc.calls` để test kiểm thứ tự (undo mark bao quanh thao tác ghi…).
"""
import math

import pythoncom

RPC_E_CALL_REJECTED = -2147418111


def busy_error():
    return pythoncom.com_error(RPC_E_CALL_REJECTED, "Call was rejected by callee.", None, None)


class FakeEntity:
    _seq = 0x200

    def __init__(self, doc, object_name, **props):
        FakeEntity._seq += 1
        object.__setattr__(self, "_doc", doc)
        object.__setattr__(self, "Handle", format(FakeEntity._seq, "X"))
        object.__setattr__(self, "ObjectName", object_name)
        object.__setattr__(self, "Layer", "0")
        for k, v in props.items():
            object.__setattr__(self, k, v)

    def __setattr__(self, name, value):
        if name == "Layer":
            self._doc._hit("SetLayer")
        object.__setattr__(self, name, value)

    def Delete(self):
        self._doc._hit("Delete")
        self._doc.ModelSpace._items.remove(self)


class FakeModelSpace:
    def __init__(self, doc):
        self._doc = doc
        self._items = []

    @property
    def Count(self):
        self._doc._hit("Count")
        return len(self._items)

    def Item(self, i):
        return self._items[i]

    def _add(self, op, obj_name, **props):
        self._doc._hit(op)
        e = FakeEntity(self._doc, obj_name, **props)
        self._items.append(e)
        return e

    def AddLine(self, p1, p2):
        p1, p2 = _point(p1), _point(p2)
        return self._add("AddLine", "AcDbLine", StartPoint=p1, EndPoint=p2,
                         Length=math.dist(p1[:2], p2[:2]))

    def AddCircle(self, c, r):
        return self._add("AddCircle", "AcDbCircle", Center=_point(c), Radius=r)


def _point(p):
    """COM thật nhận win32com VARIANT (có .value); test có thể truyền tuple."""
    return tuple(getattr(p, "value", p))


class FakeLayer:
    def __init__(self, name):
        self.Name, self.Color, self.LayerOn, self.Lock, self.Linetype = name, 7, True, False, "Continuous"


class FakeLayers:
    def __init__(self, doc):
        self._doc = doc
        self._layers = {"0": FakeLayer("0")}

    @property
    def Count(self):
        return len(self._layers)

    def Item(self, key):
        if isinstance(key, int):
            return list(self._layers.values())[key]
        if key not in self._layers:
            raise pythoncom.com_error(-2145386476, "Key not found", None, None)
        return self._layers[key]

    def Add(self, name):
        self._doc._hit("AddLayer")
        self._layers[name] = FakeLayer(name)
        return self._layers[name]


class FakeDocument:
    def __init__(self, app, name, full_name="", read_only=False):
        self._app = app
        self.Name, self.FullName, self.ReadOnly, self.Saved = name, full_name, read_only, True
        self.ModelSpace = FakeModelSpace(self)
        self.Layers = FakeLayers(self)
        self.calls, self.sent, self._fail = [], [], {}
        self.variables = {"INSUNITS": 4, "CMDACTIVE": 0}
        self.busy_reads_after_save = 0      # AutoCAD thật: vừa ghi xong, lời gọi đọc kế tiếp có thể bị từ chối
        self.command_runs_for = 0           # SendCommand bất đồng bộ: CMDACTIVE≠0 trong N lần đọc

    def __getattribute__(self, name):
        if name in ("Name", "FullName", "ReadOnly"):
            fail = object.__getattribute__(self, "_fail")
            if fail.get("Read", 0) > 0:
                fail["Read"] -= 1
                raise busy_error()
        return object.__getattribute__(self, name)

    # --- bơm lỗi ---
    def fail_once(self, op, times=1):
        self._fail[op] = self._fail.get(op, 0) + times

    def _hit(self, op):
        self.calls.append(op)
        if self._fail.get(op, 0) > 0:
            self._fail[op] -= 1
            raise busy_error()
        if op.startswith(("Add", "Set", "Delete")):
            self.Saved = False

    # --- API tài liệu ---
    def StartUndoMark(self):
        self._hit("StartUndoMark")

    def EndUndoMark(self):
        self._hit("EndUndoMark")

    def GetVariable(self, name):
        if name == "CMDACTIVE" and self.command_runs_for > 0:
            self.command_runs_for -= 1
            return 1
        return self.variables.get(name, 0)

    def Activate(self):
        self._app._active = self

    def Save(self):
        self._hit("Save")
        self.Saved = True

    def SaveAs(self, path, save_as_type=None):
        """Như AutoCAD 2025 thật (đo 2026-11-02): không truyền kiểu ⇒ lưu DWG và NỐI THÊM '.dwg' nếu đuôi khác;
        65 = ac2018_dxf giữ nguyên đuôi .dxf."""
        self._hit("SaveAs")
        if save_as_type is None and not path.lower().endswith(".dwg"):
            path += ".dwg"
        self.FullName, self.Name, self.Saved = path, path.replace("\\", "/").rsplit("/", 1)[-1], True
        self.saved_as_type = save_as_type
        self._fail["Read"] = self._fail.get("Read", 0) + self.busy_reads_after_save

    def Close(self, save=False):
        self._hit("Close")
        self._app._docs.remove(self)
        if self._app._active is self:
            self._app._active = self._app._docs[0] if self._app._docs else None

    def SendCommand(self, s):
        self._hit("SendCommand")
        self.sent.append(s)
        self.command_runs_for = self.variables.get("_command_duration", 0)


class FakeDocuments:
    def __init__(self, app):
        self._app = app

    @property
    def Count(self):
        # AutoCAD 2025 thật, ngay sau Close: win32com dynamic ném AttributeError('<unknown>.Count') một lúc
        if self._app.lost_typeinfo > 0:
            self._app.lost_typeinfo -= 1
            raise AttributeError("<unknown>.Count")
        return len(self._app._docs)

    def Item(self, i):
        return self._app._docs[i]

    def Add(self):
        d = FakeDocument(self._app, f"Drawing{len(self._app._docs) + 1}.dwg")
        self._app._docs.append(d)
        self._app._active = d
        return d

    def Open(self, path, read_only=True):
        d = FakeDocument(self._app, path.replace("\\", "/").rsplit("/", 1)[-1], path, read_only)
        self._app._docs.append(d)
        self._app._active = d
        return d


class FakeApp:
    Name, Version = "AutoCAD", "25.0s (fake)"

    def __init__(self):
        self._docs, self._active = [], None
        self.Documents = FakeDocuments(self)
        self.zoomed = 0
        self.lost_typeinfo = 0

    @property
    def ActiveDocument(self):
        return self._active

    def add_doc(self, name, full_name="", read_only=False, active=True):
        d = FakeDocument(self, name, full_name, read_only)
        self._docs.append(d)
        if active or self._active is None:
            self._active = d
        return d

    def ZoomExtents(self):
        self.zoomed += 1
