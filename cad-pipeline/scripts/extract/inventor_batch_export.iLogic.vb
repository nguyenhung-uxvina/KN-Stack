' ============================================================================
' inventor_batch_export.iLogic.vb  —  "3 file vàng" cho pipeline QTCN / qtcn-seed
' ----------------------------------------------------------------------------
' Xuất từ một ASSEMBLY (.iam) đang mở:
'   1) <asm>.step         — hình học 3D (feed freecad_extract.py: bbox/thể tích)
'   2) <asm>_BOM.csv      — Part Number, Description, Material, QTY, Mass_kg,
'                            Stock (feed seed: XƯƠNG SỐNG BOM — mass & vật liệu THẬT
'                            do Inventor tính, thay cho suy-theo-tên/parse binary)
'   3) <part>_flat.dxf    — flat pattern mọi part sheet-metal (feed bảng cắt CNC +
'                            parse_mech_drawing.py cho kích thước tấm/lỗ)
'   + <asm>_hygiene.txt   — cảnh báo 3 lỗi data: Material="Generic", thiếu Part
'                            Number / Description (những thứ làm BOM export thiếu cột).
'
' DÙNG:  Mở .iam trong Inventor → Manage > iLogic > Add Rule → dán → Run.
'        (hoặc lưu External Rule để chạy lại cho nhiều assembly).
' CHỈNH: chỉ cần sửa OUT_DIR bên dưới.
'
' LƯU Ý TRUNG THỰC: chưa chạy được trong môi trường này (không có Inventor). Viết
'   theo Inventor API chuẩn (2018+). Nếu version khác báo lỗi ở STEP options hay
'   flat-pattern, xem ghi chú [VER] tại chỗ đó. MassProperties.Mass trả về **kg**
'   (đơn vị DB của Inventor) — đối chiếu với khối lượng Inventor hiển thị 1 lần.
' ============================================================================

' ------------------------------- CONFIG -------------------------------------
Dim OUT_DIR As String = "D:\2025\XSX\Dau T\_inventor_export"
Dim STEP_PROTOCOL As Integer = 3      ' 2=AP203, 3=AP214, 4=AP242 ([VER] 242 cần Inv mới)
Dim DXF_ACADVER As String = "2018"
' ----------------------------------------------------------------------------

Dim oApp As Inventor.Application = ThisApplication
Dim oDoc As Document = ThisDoc.Document
If oDoc.DocumentType <> DocumentTypeEnum.kAssemblyDocumentObject Then
    MessageBox.Show("Hãy mở file ASSEMBLY (.iam) rồi chạy rule này.", "QTCN batch-export")
    Return
End If
If Not System.IO.Directory.Exists(OUT_DIR) Then System.IO.Directory.CreateDirectory(OUT_DIR)

Dim oAsm As AssemblyDocument = CType(oDoc, AssemblyDocument)
Dim asmName As String = System.IO.Path.GetFileNameWithoutExtension(oDoc.FullFileName)
Dim sbBom As New System.Text.StringBuilder()
Dim sbHyg As New System.Text.StringBuilder()
Dim seen As New System.Collections.Generic.HashSet(Of String)()

' --- 1) STEP của assembly ---
Try
    ExportSTEP(oApp, oDoc, System.IO.Path.Combine(OUT_DIR, asmName & ".step"), STEP_PROTOCOL)
Catch ex As Exception
    sbHyg.AppendLine("[STEP FAIL] " & ex.Message)
End Try

' --- 2)+3) BOM (structured) + flat DXF cho từng part ---
sbBom.AppendLine("Level,PartNumber,Description,Material,QTY,Mass_kg,StockNumber,FileName,Hygiene")
Dim oBOM As BOM = oAsm.ComponentDefinition.BOM
oBOM.StructuredViewEnabled = True
oBOM.StructuredViewFirstLevelOnly = False
Dim oView As BOMView = oBOM.BOMViews.Item("Structured")
WalkBOM(oView.BOMRows, 1, sbBom, sbHyg, seen, OUT_DIR, DXF_ACADVER)

System.IO.File.WriteAllText(System.IO.Path.Combine(OUT_DIR, asmName & "_BOM.csv"), _
    sbBom.ToString(), New System.Text.UTF8Encoding(True))   ' BOM: UTF-8 BOM để Excel đọc tiếng Việt
System.IO.File.WriteAllText(System.IO.Path.Combine(OUT_DIR, asmName & "_hygiene.txt"), _
    sbHyg.ToString(), System.Text.Encoding.UTF8)

MessageBox.Show("Xong. Xuất vào:" & vbCrLf & OUT_DIR & vbCrLf & _
    "- " & asmName & ".step" & vbCrLf & "- " & asmName & "_BOM.csv" & vbCrLf & _
    "- *_flat.dxf (part sheet-metal)" & vbCrLf & "- " & asmName & "_hygiene.txt (rà lỗi data)", _
    "QTCN batch-export")

' ============================== SUBROUTINES =================================
Sub WalkBOM(rows As BOMRowsEnumerator, level As Integer, sbBom As System.Text.StringBuilder, _
            sbHyg As System.Text.StringBuilder, seen As System.Collections.Generic.HashSet(Of String), _
            outDir As String, dxfVer As String)
    For Each row As BOMRow In rows
        If row.ComponentDefinitions.Count = 0 Then Continue For
        Dim cd As ComponentDefinition = row.ComponentDefinitions.Item(1)
        Dim d As Document = CType(cd.Document, Document)
        Dim pn As String = GetProp(d, "Design Tracking Properties", "Part Number")
        Dim de As String = GetProp(d, "Design Tracking Properties", "Description")
        Dim mat As String = GetProp(d, "Design Tracking Properties", "Material")
        Dim st As String = GetProp(d, "Design Tracking Properties", "Stock Number")
        Dim qty As Integer = row.TotalQuantity
        Dim mass As Double = 0
        Try : mass = Math.Round(cd.MassProperties.Mass, 3) : Catch : End Try   ' kg
        Dim fn As String = System.IO.Path.GetFileName(d.FullFileName)

        ' --- hygiene (3 lỗi data hygiene) ---
        Dim flags As New System.Collections.Generic.List(Of String)()
        If mat = "" OrElse mat.ToLower().Contains("generic") Then flags.Add("MAT?")
        If pn = "" Then flags.Add("noPN")
        If de = "" Then flags.Add("noDesc")
        Dim fstr As String = String.Join("|", flags.ToArray())
        If flags.Count > 0 Then sbHyg.AppendLine(fn & "  ->  " & fstr)

        sbBom.AppendLine(String.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8}", _
            level, Csv(pn), Csv(de), Csv(mat), qty, mass, Csv(st), Csv(fn), fstr))

        ' --- flat DXF nếu là part tấm (sheet-metal) ---
        If TypeOf cd Is SheetMetalComponentDefinition Then
            Dim base As String = System.IO.Path.GetFileNameWithoutExtension(d.FullFileName)
            If seen.Add(base) Then ExportFlatDXF(CType(cd, SheetMetalComponentDefinition), _
                System.IO.Path.Combine(outDir, base & "_flat.dxf"), dxfVer, sbHyg)
        End If

        ' --- đệ quy sub-assembly ---
        If row.ChildRows IsNot Nothing AndAlso row.ChildRows.Count > 0 Then
            WalkBOM(row.ChildRows, level + 1, sbBom, sbHyg, seen, outDir, dxfVer)
        End If
    Next
End Sub

Function GetProp(d As Document, setName As String, propName As String) As String
    Try
        Return CStr(d.PropertySets.Item(setName).Item(propName).Value)
    Catch
        Return ""
    End Try
End Function

Function Csv(s As String) As String
    If s Is Nothing Then Return ""
    If s.Contains(",") OrElse s.Contains("""") OrElse s.Contains(vbLf) Then _
        Return """" & s.Replace("""", """""") & """"
    Return s
End Function

Sub ExportFlatDXF(smcd As SheetMetalComponentDefinition, outFile As String, _
                  dxfVer As String, sbHyg As System.Text.StringBuilder)
    Try
        If Not smcd.HasFlatPattern Then smcd.Unfold()   ' [VER] tạo flat pattern nếu chưa có
        ' Chuỗi tuỳ chọn chuẩn của Inventor cho flat-pattern DXF:
        Dim opt As String = "FLAT PATTERN DXF?AcadVersion=" & dxfVer & _
            "&OuterProfileLayer=IV_OUTER_PROFILE&InteriorProfilesLayer=IV_INTERIOR_PROFILES"
        smcd.DataIO.WriteDataToFile(opt, outFile)
    Catch ex As Exception
        sbHyg.AppendLine(System.IO.Path.GetFileName(outFile) & "  ->  FLAT DXF FAIL: " & ex.Message)
    End Try
End Sub

Sub ExportSTEP(oApp As Inventor.Application, oDoc As Document, outFile As String, protocol As Integer)
    Dim addin As TranslatorAddIn = CType( _
        oApp.ApplicationAddIns.ItemById("{90AF7F40-0C01-11D5-8E83-0010B541CD80}"), TranslatorAddIn)
    Dim ctx As TranslationContext = oApp.TransientObjects.CreateTranslationContext()
    ctx.Type = IOMechanismEnum.kFileBrowseIOMechanism
    Dim opts As NameValueMap = oApp.TransientObjects.CreateNameValueMap()
    Dim med As DataMedium = oApp.TransientObjects.CreateDataMedium()
    If addin.HasSaveCopyAsOptions(oDoc, ctx, opts) Then
        Try : opts.Value("ApplicationProtocolType") = protocol : Catch : End Try
    End If
    med.FileName = outFile
    addin.SaveCopyAs(oDoc, ctx, opts, med)
End Sub
