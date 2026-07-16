' =====================================================================================
'  Drawing_Check_Live — iLogic rule: sensor tầng bản vẽ cần INVENTOR SỐNG
'  (bổ trợ cho drawing_check.py vốn chạy Apprentice không mở app — WX-QT-DRAWING-SENSOR-01)
'
'  Kiểm các rule mà Apprentice không với tới:
'   • D2-04  Interference assembly (AnalyzeInterference) — thể tích giao từng cặp
'   • D1-11  BOM view Parts Only đã Enabled chưa
'   • D3-03  Dimension "dangling" (mất tham chiếu) trên bản vẽ .idw/.dwg đang mở
'
'  DÙNG:
'   - Mở .iam → Run rule  → kiểm D2-04 + D1-11
'   - Mở .idw/.dwg → Run rule → kiểm D3-03
'   - Khuyến nghị add làm EXTERNAL RULE trỏ thẳng file này (luôn bản mới nhất):
'     Manage → iLogic → External Rules → Add → D:\KN-Stack\scripts\inventor\Drawing_Check_Live.iLogic.vb
'
'  Xuất <thư mục tài liệu>\drawing_live_report.json (cùng dạng rule-entry với
'  drawing_report.json của drawing_check.py). Read-only — không sửa/không lưu tài liệu.
'
'  LƯU Ý TRUNG THỰC: viết theo API chuẩn Inventor 2018+, CHƯA chạy thật trong môi
'  trường viết ra nó. Điểm cần xem khi chạy lần đầu: (1) AnalyzeInterference trên
'  assembly lớn có thể chậm; (2) thuộc tính Attached/HealthStatus của DrawingDimension
'  khác nhau theo version ([VER]); (3) InterferenceResult.Volume trả đơn vị DB (cm³).
'  Quy ước cứng: KHÔNG Imports System.IO (đụng Inventor.Path/File) — gọi tường minh;
'  KHÔNG Sub lồng trong Main (VB cấm) — helper đặt SAU Main.
' =====================================================================================

Sub Main()
    Dim doc As Document = ThisApplication.ActiveDocument
    If doc Is Nothing Then
        MessageBox.Show("Mở file .iam (kiểm D2-04/D1-11) hoặc .idw/.dwg (kiểm D3-03) rồi chạy.",
                        "Drawing_Check_Live")
        Exit Sub
    End If

    Dim entries As New List(Of String)      ' từng dòng JSON rule-entry
    Dim human As New System.Text.StringBuilder()
    Dim nFail As Integer = 0, nWarn As Integer = 0

    If doc.DocumentType = DocumentTypeEnum.kAssemblyDocumentObject Then
        Dim oAsm As AssemblyDocument = doc

        ' ---------- D1-11: BOM view đã bật chưa ----------
        Try
            Dim oBOM As BOM = oAsm.ComponentDefinition.BOM
            If Not oBOM.PartsOnlyViewEnabled Then
                AddRule(entries, human, nFail, nWarn, "D1-11", "WARNING", oAsm.DisplayName,
                        "BOM view Parts Only chưa Enabled — bật trong Bill of Materials rồi Save")
            End If
        Catch ex As Exception
            AddRule(entries, human, nFail, nWarn, "D1-11", "WARNING", oAsm.DisplayName,
                    "không đọc được BOM: " & ex.Message)
        End Try

        ' ---------- D2-04: Interference ----------
        Try
            Dim oResults As InterferenceResults = oAsm.ComponentDefinition.AnalyzeInterference()
            If oResults.Count = 0 Then
                AddRule(entries, human, nFail, nWarn, "D2-04", "PASS", oAsm.DisplayName,
                        "không có interference")
            Else
                For k As Integer = 1 To oResults.Count
                    Dim r As InterferenceResult = oResults.Item(k)
                    Dim volMm3 As Double = r.Volume * 1000.0   ' [VER] Volume DB units cm³ → mm³
                    Dim names As String = ""
                    Try : names = r.OccurrenceOne.Name & " <-> " & r.OccurrenceTwo.Name : Catch : End Try
                    If volMm3 > 100.0 Then
                        AddRule(entries, human, nFail, nWarn, "D2-04", "FAIL", names,
                                "cài nhau " & Math.Round(volMm3, 1) & " mm3 (>100) — mối ghép chưa vát/lỗi model")
                    ElseIf volMm3 > 1.0 Then
                        AddRule(entries, human, nFail, nWarn, "D2-04", "WARNING", names,
                                "giao " & Math.Round(volMm3, 1) & " mm3 (1-100) — rà fit hàn/ren")
                    End If
                Next
            End If
        Catch ex As Exception
            AddRule(entries, human, nFail, nWarn, "D2-04", "WARNING", oAsm.DisplayName,
                    "AnalyzeInterference lỗi: " & ex.Message)
        End Try

        ' ---------- D2-05: occurrence "trôi" (không ground, không dính constraint nào) ----------
        Try
            Dim constrained As New HashSet(Of String)(StringComparer.OrdinalIgnoreCase)
            For Each c As AssemblyConstraint In oAsm.ComponentDefinition.Constraints
                Try : constrained.Add(c.OccurrenceOne.Name) : Catch : End Try
                Try : constrained.Add(c.OccurrenceTwo.Name) : Catch : End Try
            Next
            Dim nFloat As Integer = 0
            For Each occ As ComponentOccurrence In oAsm.ComponentDefinition.Occurrences
                Dim grounded As Boolean = True
                Try : grounded = occ.Grounded : Catch : End Try
                If (Not grounded) AndAlso (Not constrained.Contains(occ.Name)) Then
                    nFloat += 1
                    If nFloat <= 15 Then
                        AddRule(entries, human, nFail, nWarn, "D2-05", "WARNING", occ.Name,
                                "occurrence chưa ground và không có constraint — vị trí có thể trôi khi sửa")
                    End If
                End If
            Next
            If nFloat > 15 Then
                AddRule(entries, human, nFail, nWarn, "D2-05", "WARNING", oAsm.DisplayName,
                        "… và " & (nFloat - 15) & " occurrence trôi nữa")
            End If
            If nFloat = 0 Then
                AddRule(entries, human, nFail, nWarn, "D2-05", "PASS", oAsm.DisplayName,
                        "mọi occurrence đều ground hoặc có constraint")
            End If
        Catch ex As Exception
            AddRule(entries, human, nFail, nWarn, "D2-05", "WARNING", oAsm.DisplayName,
                    "kiểm ràng buộc lỗi: " & ex.Message)
        End Try

    ElseIf doc.DocumentType = DocumentTypeEnum.kDrawingDocumentObject Then
        Dim oDrw As DrawingDocument = doc

        ' ---------- D3-03: dimension dangling ----------
        Dim nDim As Integer = 0, nDangling As Integer = 0
        Try
            For Each oSheet As Sheet In oDrw.Sheets
                For Each oDim As DrawingDimension In oSheet.DrawingDimensions
                    nDim += 1
                    Dim attached As Boolean = True
                    Try
                        attached = oDim.Attached
                    Catch
                        Try
                            attached = (oDim.HealthStatus = HealthStatusEnum.kUpToDateHealth) ' [VER]
                        Catch : End Try
                    End Try
                    If Not attached Then
                        nDangling += 1
                        Dim txt As String = ""
                        Try : txt = oDim.Text.Text : Catch : End Try
                        AddRule(entries, human, nFail, nWarn, "D3-03", "FAIL",
                                oSheet.Name & "/" & txt,
                                "dimension mất tham chiếu (dangling) — bản vẽ chưa cập nhật theo model")
                    End If
                Next
            Next
            If nDangling = 0 Then
                AddRule(entries, human, nFail, nWarn, "D3-03", "PASS", oDrw.DisplayName,
                        nDim & " dimension đều còn tham chiếu")
            End If
        Catch ex As Exception
            AddRule(entries, human, nFail, nWarn, "D3-03", "WARNING", oDrw.DisplayName,
                    "duyệt dimension lỗi: " & ex.Message)
        End Try

        ' ---------- D3-07: ký hiệu hàn hiện diện (với bản vẽ kết cấu hàn) ----------
        Try
            Dim nWeld As Integer = 0
            For Each oSheet As Sheet In oDrw.Sheets
                Try
                    nWeld += oSheet.WeldSymbols.Count           ' [VER] tên collection theo version
                Catch
                    Try : nWeld += oSheet.WeldingSymbols.Count : Catch : End Try
                End Try
            Next
            If nWeld = 0 Then
                AddRule(entries, human, nFail, nWarn, "D3-07", "WARNING", oDrw.DisplayName,
                        "0 ký hiệu hàn trên bản vẽ — nếu đây là kết cấu hàn (WA/WS) thì theo D3-07 là FAIL")
            Else
                AddRule(entries, human, nFail, nWarn, "D3-07", "PASS", oDrw.DisplayName,
                        nWeld & " ký hiệu hàn")
            End If
        Catch ex As Exception
            AddRule(entries, human, nFail, nWarn, "D3-07", "WARNING", oDrw.DisplayName,
                    "đếm weld symbol lỗi: " & ex.Message)
        End Try
    Else
        MessageBox.Show("Rule này chạy trên .iam hoặc .idw/.dwg.", "Drawing_Check_Live")
        Exit Sub
    End If

    ' ---------- Ghi report + tổng kết ----------
    Dim verdict As String = If(nFail > 0, "FAIL", If(nWarn > 0, "WARNING", "PASS"))
    Dim json As New System.Text.StringBuilder()
    json.AppendLine("{")
    json.AppendLine("  ""form"": ""WX-QT-DRAWING-F01/live"",")
    json.AppendLine("  ""source"": """ & JEsc(doc.FullFileName) & """,")
    json.AppendLine("  ""verdict"": """ & verdict & """,")
    json.AppendLine("  ""counts"": {""FAIL"": " & nFail & ", ""WARNING"": " & nWarn & "},")
    json.AppendLine("  ""rules"": [")
    json.AppendLine(String.Join("," & vbLf, entries.ToArray()))
    json.AppendLine("  ]")
    json.AppendLine("}")

    Dim outPath As String = System.IO.Path.Combine(
        System.IO.Path.GetDirectoryName(doc.FullFileName), "drawing_live_report.json")
    Try
        System.IO.File.WriteAllText(outPath, json.ToString(), New System.Text.UTF8Encoding(True))
    Catch : End Try

    MessageBox.Show("KẾT QUẢ: " & verdict & "  (FAIL=" & nFail & ", WARNING=" & nWarn & ")" & vbCrLf &
                    "Report: " & outPath & vbCrLf & New String("-"c, 50) & vbCrLf & human.ToString(),
                    "Drawing_Check_Live — " & verdict)
End Sub

' ------------------------- Helpers (SAU Main — VB cấm Sub lồng) -------------------------

Private Sub AddRule(entries As List(Of String), human As System.Text.StringBuilder,
                    ByRef nFail As Integer, ByRef nWarn As Integer,
                    rule As String, level As String, where As String, msg As String)
    entries.Add("    {""rule"": """ & rule & """, ""level"": """ & level & """, ""where"": """ &
                JEsc(where) & """, ""msg"": """ & JEsc(msg) & """}")
    human.AppendLine("[" & level & "] " & rule & " @ " & where & " — " & msg)
    If level = "FAIL" Then nFail += 1
    If level = "WARNING" Then nWarn += 1
End Sub

Private Function JEsc(s As String) As String
    If s Is Nothing Then Return ""
    Return s.Replace("\", "\\").Replace("""", "'").Replace(vbCr, " ").Replace(vbLf, " ")
End Function
