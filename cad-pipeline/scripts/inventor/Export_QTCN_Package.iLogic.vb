' =====================================================================================
'  Export_QTCN_Package  —  iLogic rule cho Autodesk Inventor
'  "Export gói QTCN": chạy trên ASSEMBLY (.iam) đang mở → tự dump vào 1 thư mục:
'     • <asm>_BOM.csv   — bảng kê Parts-Only, cột chuẩn cho bom_xlsx_to_seed.py
'                         (Item · Part Number · Description · QTY · Material · Stock Number
'                          · Mass (kg) · BOM Structure)  — Mass do Inventor tính (nguồn VÀNG)
'     • <asm>.step      — STEP AP242 (hình học 3D trung lập, cho freecad_extract.py)
'     • dxf\<part>.dxf  — flat-pattern DXF từng chi tiết tôn (cho cắt laser/plasma + dung sai)
'     • pdf\<drawing>.pdf — PDF các bản vẽ .idw/.dwg trùng tên trong thư mục (title block/chữ ký)
'
'  Sau khi chạy → feed pipeline KN-Stack:
'     python cad-pipeline/scripts/extract/bom_xlsx_to_seed.py --bom <asm>_BOM.csv --assembly-code <mã> --product-name "<tên>"
'  (Không cần MCP: độ chính xác đến từ cột Mass+Material Inventor tự tính.)
'
'  CÁCH DÙNG:
'   1. Mở file lắp (.iam) trong Inventor.
'   2. Manage → iLogic → Add Rule (hoặc External Rule) → dán toàn bộ file này → Run.
'   3. Xem hộp thoại tổng kết; thư mục kết quả tự mở.
'
'  Mỗi khối export bọc Try/Catch riêng — 1 lỗi không chặn các phần còn lại.
'  Không sửa/không lưu đè mô hình gốc; flat-pattern tạo tạm rồi thoát edit.
' =====================================================================================

' LƯU Ý DÁN RULE: xóa SẠCH nội dung rule cũ (Ctrl+A → Delete) trước khi dán file này.
' Dán NỐI vào code cũ sẽ báo "All other Sub's or Function's must be after Sub Main()".
' Không dùng Imports: iLogic tự import namespace Inventor (có Inventor.Path/File trùng
' tên System.IO) — mọi lời gọi IO trong rule này đã viết tường minh System.IO.*

Sub Main()

    ' --- 0. Bắt buộc là assembly ---
    If ThisApplication.ActiveDocumentType <> DocumentTypeEnum.kAssemblyDocumentObject Then
        MessageBox.Show("Hãy mở FILE LẮP (.iam) rồi chạy rule này.", "Export gói QTCN",
                        MessageBoxButtons.OK, MessageBoxIcon.Warning)
        Exit Sub
    End If

    Dim oAsm As AssemblyDocument = ThisApplication.ActiveDocument
    Dim asmPath As String = oAsm.FullFileName
    Dim asmName As String = System.IO.Path.GetFileNameWithoutExtension(asmPath)
    Dim asmDir As String = System.IO.Path.GetDirectoryName(asmPath)

    ' --- Thư mục xuất: <asmDir>\_QTCN_export\<asmName>\ ---
    Dim outDir As String = System.IO.Path.Combine(asmDir, "_QTCN_export", asmName)
    Dim dxfDir As String = System.IO.Path.Combine(outDir, "dxf")
    Dim pdfDir As String = System.IO.Path.Combine(outDir, "pdf")
    System.IO.Directory.CreateDirectory(outDir)
    System.IO.Directory.CreateDirectory(dxfDir)
    System.IO.Directory.CreateDirectory(pdfDir)

    Dim Log As New System.Text.StringBuilder
    Log.AppendLine("GÓI QTCN — " & asmName)
    Log.AppendLine("Nguồn : " & asmPath)
    Log.AppendLine("Xuất  : " & outDir)
    Log.AppendLine(New String("-"c, 60))

    Dim nBom As Integer = 0, nDxf As Integer = 0, nPdf As Integer = 0
    Dim stepOK As Boolean = False

    ' ================================================================
    ' 1. BOM.csv  (Parts Only — cột chuẩn cho bom_xlsx_to_seed.py)
    ' ================================================================
    Dim bomStage As String = "khởi tạo"
    Try
        Dim oBOM As BOM = oAsm.ComponentDefinition.BOM
        ' Lấy BOM view theo VIEWTYPE (enum), KHÔNG theo tên — BOMViews.Item("Parts Only")
        ' ném E_INVALIDARG khi tên view khác đi (ngôn ngữ UI / weldment assembly).
        Dim oView As BOMView = Nothing
        Dim viewLabel As String = ""
        bomStage = "bật Parts Only"
        Try
            oBOM.PartsOnlyViewEnabled = True
            For Each v As BOMView In oBOM.BOMViews
                If v.ViewType = BOMViewTypeEnum.kPartsOnlyBOMViewType Then
                    oView = v : viewLabel = "Parts Only" : Exit For
                End If
            Next
        Catch
        End Try
        If oView Is Nothing Then
            ' Fallback: view Structured mọi cấp, duyệt đệ quy; dòng cụm lắp được đánh
            ' dấu "Assembly" ở cột BOM Structure để bom_xlsx_to_seed.py tự bỏ.
            bomStage = "bật Structured"
            Try
                oBOM.StructuredViewEnabled = True
                oBOM.StructuredViewFirstLevelOnly = False
            Catch
            End Try
            For Each v As BOMView In oBOM.BOMViews
                If v.ViewType = BOMViewTypeEnum.kStructuredBOMViewType Then
                    oView = v : viewLabel = "Structured/đệ quy" : Exit For
                End If
            Next
        End If
        If oView Is Nothing Then
            ' Fallback CUỐI: Model Data view (luôn tồn tại, thường tên "Unnamed") —
            ' gặp khi bật Parts Only/Structured bị chặn: file mở chế độ EXPRESS,
            ' Model State/LOD active không phải Primary, hoặc view chưa từng bật
            ' trong tài liệu. Đệ quy + dedupe + TotalQuantity vẫn cho BOM đủ dùng.
            bomStage = "fallback Model Data"
            For Each v As BOMView In oBOM.BOMViews
                If v.ViewType = BOMViewTypeEnum.kModelDataBOMViewType Then
                    oView = v : viewLabel = "Model Data — nên bật Parts Only trong hộp thoại Bill of Materials rồi Save" : Exit For
                End If
            Next
        End If
        If oView Is Nothing Then
            ' Liệt kê view đang có để chẩn đoán lần sau
            Dim names As String = ""
            Try
                For Each v As BOMView In oBOM.BOMViews : names &= v.Name & " · " : Next
            Catch : End Try
            Throw New Exception("Không lấy được BOM view nào. View hiện có: " & names)
        End If

        bomStage = "ghi CSV (" & viewLabel & ")"
        Dim csvPath As String = System.IO.Path.Combine(outDir, asmName & "_BOM.csv")
        ' UTF-8 BOM để Excel mở đúng tiếng Việt
        Using sw As New System.IO.StreamWriter(csvPath, False, New System.Text.UTF8Encoding(True))
            sw.WriteLine("Item,Part Number,Description,QTY,Material,Stock Number,Mass (kg),BOM Structure")
            Dim seen As New HashSet(Of String)(StringComparer.OrdinalIgnoreCase)
            nBom = WriteBomRows(oView.BOMRows, sw, seen)
        End Using
        Log.AppendLine("[OK] BOM.csv (" & viewLabel & "): " & nBom & " dòng → " & System.IO.Path.GetFileName(csvPath))
    Catch ex As Exception
        Log.AppendLine("[X ] BOM.csv (lỗi ở bước: " & bomStage & "): " & ex.Message)
    End Try

    ' ================================================================
    ' 2. STEP AP242
    ' ================================================================
    Try
        Dim stepPath As String = System.IO.Path.Combine(outDir, asmName & ".step")
        Dim oSTEP As TranslatorAddIn =
            ThisApplication.ApplicationAddIns.ItemById("{90AF7F40-0C01-11D5-8E83-0010B541CD80}")
        Dim oCtx As TranslationContext = ThisApplication.TransientObjects.CreateTranslationContext
        oCtx.Type = IOMechanismEnum.kFileBrowseIOMechanism
        Dim oOpts As NameValueMap = ThisApplication.TransientObjects.CreateNameValueMap
        Dim oData As DataMedium = ThisApplication.TransientObjects.CreateDataMedium
        If oSTEP.HasSaveCopyAsOptions(oAsm, oCtx, oOpts) Then
            ' 2=AP203, 3=AP214, 4=AP242 (dùng AP242, fallback im lặng nếu bản Inventor không hỗ trợ)
            Try : oOpts.Value("ApplicationProtocolType") = 4 : Catch : End Try
            Try : oOpts.Value("Author") = "Workshop X" : Catch : End Try
        End If
        oData.FileName = stepPath
        oSTEP.SaveCopyAs(oAsm, oCtx, oOpts, oData)
        stepOK = System.IO.File.Exists(stepPath)
        Log.AppendLine("[OK] STEP           : " & System.IO.Path.GetFileName(stepPath))
    Catch ex As Exception
        Log.AppendLine("[X ] STEP           : " & ex.Message)
    End Try

    ' ================================================================
    ' 3. Flat-pattern DXF cho từng chi tiết TÔN (sheet metal), dedupe theo file
    ' ================================================================
    Try
        Dim seen As New HashSet(Of String)(StringComparer.OrdinalIgnoreCase)
        Dim oOcc As ComponentOccurrence
        For Each oOcc In oAsm.ComponentDefinition.Occurrences.AllLeafOccurrences
            Dim oDef As ComponentDefinition = Nothing
            Try : oDef = oOcc.Definition : Catch : Continue For : End Try
            If Not (TypeOf oDef Is SheetMetalComponentDefinition) Then Continue For
            Dim oPartDoc As PartDocument = Nothing
            Try : oPartDoc = oDef.Document : Catch : Continue For : End Try
            Dim ff As String = oPartDoc.FullFileName
            If seen.Contains(ff) Then Continue For
            seen.Add(ff)

            Try
                Dim oSM As SheetMetalComponentDefinition = oDef
                Dim created As Boolean = False
                If Not oSM.HasFlatPattern Then
                    oSM.Unfold() : oSM.FlatPattern.ExitEdit() : created = True
                End If
                Dim baseNm As String = SafeName(System.IO.Path.GetFileNameWithoutExtension(ff))
                Dim dxfPath As String = System.IO.Path.Combine(dxfDir, baseNm & ".dxf")
                Dim sOut As String =
                    "FLAT PATTERN DXF?AcadVersion=2018" &
                    "&OuterProfileLayer=IV_OUTER_PROFILE" &
                    "&InteriorProfilesLayer=IV_INTERIOR_PROFILES" &
                    "&BendUpLayer=IV_BEND&BendDownLayer=IV_BEND_DOWN"
                oSM.FlatPattern.DataIO.WriteDataToFile(sOut, dxfPath)
                nDxf += 1
            Catch exi As Exception
                Log.AppendLine("      · DXF lỗi (" & System.IO.Path.GetFileName(ff) & "): " & exi.Message)
            End Try
        Next
        Log.AppendLine("[OK] Flat DXF (tôn) : " & nDxf & " chi tiết → dxf\")
    Catch ex As Exception
        Log.AppendLine("[X ] Flat DXF       : " & ex.Message)
    End Try

    ' ================================================================
    ' 4. PDF các bản vẽ .idw/.dwg trùng tên gốc trong cùng thư mục
    ' ================================================================
    Try
        Dim oPDF As TranslatorAddIn =
            ThisApplication.ApplicationAddIns.ItemById("{0AC6FD96-2F4D-42CE-8BE0-8AEA580399E4}")
        Dim cands As New List(Of String)
        For Each pat As String In {"*.idw", "*.dwg"}
            Try : cands.AddRange(System.IO.Directory.GetFiles(asmDir, pat)) : Catch : End Try
        Next
        For Each dwgPath As String In cands
            Try
                Dim oDrw As DrawingDocument = ThisApplication.Documents.Open(dwgPath, False) ' không hiện
                Dim oCtx As TranslationContext = ThisApplication.TransientObjects.CreateTranslationContext
                oCtx.Type = IOMechanismEnum.kFileBrowseIOMechanism
                Dim oOpts As NameValueMap = ThisApplication.TransientObjects.CreateNameValueMap
                Dim oData As DataMedium = ThisApplication.TransientObjects.CreateDataMedium
                If oPDF.HasSaveCopyAsOptions(oDrw, oCtx, oOpts) Then
                    Try : oOpts.Value("All_Color_AS_Black") = 0 : Catch : End Try
                    Try : oOpts.Value("Sheet_Range") = PrintRangeEnum.kPrintAllSheets : Catch : End Try
                End If
                Dim pdfName As String = SafeName(System.IO.Path.GetFileNameWithoutExtension(dwgPath)) & ".pdf"
                oData.FileName = System.IO.Path.Combine(pdfDir, pdfName)
                oPDF.SaveCopyAs(oDrw, oCtx, oOpts, oData)
                oDrw.Close(True)
                nPdf += 1
            Catch exd As Exception
                Log.AppendLine("      · PDF lỗi (" & System.IO.Path.GetFileName(dwgPath) & "): " & exd.Message)
            End Try
        Next
        Log.AppendLine("[OK] PDF bản vẽ     : " & nPdf & " file → pdf\")
    Catch ex As Exception
        Log.AppendLine("[X ] PDF            : " & ex.Message)
    End Try

    ' ================================================================
    ' 5. Ghi tóm tắt + mở thư mục
    ' ================================================================
    Log.AppendLine(New String("-"c, 60))
    Log.AppendLine("Bước tiếp (pipeline KN-Stack):")
    Log.AppendLine("  python cad-pipeline/scripts/extract/bom_xlsx_to_seed.py --bom """ & asmName & "_BOM.csv""")
    Dim sumPath As String = System.IO.Path.Combine(outDir, "_export_summary.txt")
    Try : System.IO.File.WriteAllText(sumPath, Log.ToString(), New System.Text.UTF8Encoding(True)) : Catch : End Try

    Try : Process.Start("explorer.exe", """" & outDir & """") : Catch : End Try

    MessageBox.Show(Log.ToString(), "Export gói QTCN — xong",
                    MessageBoxButtons.OK, MessageBoxIcon.Information)

End Sub

' ------------------------- Helpers -------------------------

' Ghi các dòng BOM ra CSV. Đệ quy ChildRows (view Structured); Parts Only phẳng thì
' vòng ngoài chạy 1 lượt. Dedupe part theo file (Structured lặp part ở nhiều nhánh —
' TotalQuantity đã là tổng toàn sản phẩm nên chỉ ghi 1 lần).
Private Function WriteBomRows(rows As BOMRowsEnumerator, sw As System.IO.StreamWriter,
                              seen As HashSet(Of String)) As Integer
    Dim n As Integer = 0
    For Each oRow As BOMRow In rows
        Try
            Dim oCompDef As ComponentDefinition = Nothing
            Try : oCompDef = oRow.ComponentDefinitions.Item(1) : Catch : End Try
            If oCompDef IsNot Nothing Then
                Dim oDoc As Document = Nothing
                Try : oDoc = oCompDef.Document : Catch : End Try

                Dim isAsm As Boolean = False
                Try : isAsm = (oDoc IsNot Nothing AndAlso
                               oDoc.DocumentType = DocumentTypeEnum.kAssemblyDocumentObject) : Catch : End Try

                Dim key As String = ""
                Try : key = oDoc.FullFileName : Catch : End Try
                If key = "" OrElse Not seen.Contains(key) Then
                    If key <> "" Then seen.Add(key)

                    Dim item As String = TryStr(Function() oRow.ItemNumber.ToString())
                    Dim pno As String = IProp(oDoc, "Design Tracking Properties", "Part Number")
                    Dim desc As String = IProp(oDoc, "Design Tracking Properties", "Description")
                    ' TotalQuantity = tổng toàn sản phẩm (đúng cho định mức); fallback ItemQuantity
                    Dim qty As String = TryStr(Function() oRow.TotalQuantity.ToString())
                    If qty = "" Then qty = TryStr(Function() oRow.ItemQuantity.ToString())
                    Dim mat As String = MaterialName(oCompDef, oDoc)
                    Dim stock As String = IProp(oDoc, "Design Tracking Properties", "Stock Number")
                    Dim massKg As String = UnitMassKg(oCompDef)
                    Dim struct As String = StructName(oRow)
                    If isAsm Then struct = "Assembly"   ' để bom_xlsx_to_seed.py bỏ dòng cụm lắp

                    sw.WriteLine(String.Join(",", {
                        Csv(item), Csv(pno), Csv(desc), Csv(qty),
                        Csv(mat), Csv(stock), Csv(massKg), Csv(struct)}))
                    n += 1
                End If
            End If
        Catch
        End Try
        Try
            If oRow.ChildRows IsNot Nothing AndAlso oRow.ChildRows.Count > 0 Then
                n += WriteBomRows(oRow.ChildRows, sw, seen)
            End If
        Catch : End Try
    Next
    Return n
End Function

' Đọc iProperty an toàn (rỗng nếu không có)
Private Function IProp(oDoc As Document, setName As String, propName As String) As String
    If oDoc Is Nothing Then Return ""
    Try
        Dim v As Object = oDoc.PropertySets.Item(setName).Item(propName).Value
        If v Is Nothing Then Return ""
        Return v.ToString().Trim()
    Catch
        Return ""
    End Try
End Function

' Tên vật liệu: ưu tiên iProperty "Material", fallback ComponentDefinition.Material.Name
Private Function MaterialName(oCompDef As ComponentDefinition, oDoc As Document) As String
    Dim m As String = IProp(oDoc, "Design Tracking Properties", "Material")
    If m <> "" Then Return m
    Try : Return oCompDef.Material.Name : Catch : Return "" : End Try
End Function

' Khối lượng ĐƠN VỊ 1 chiếc, quy về kg (database mass units → kg)
Private Function UnitMassKg(oCompDef As ComponentDefinition) As String
    Try
        Dim raw As Double = oCompDef.MassProperties.Mass ' database mass units
        Dim oUOM As UnitsOfMeasure = oCompDef.Document.UnitsOfMeasure
        Dim kg As Double = oUOM.ConvertUnits(raw, UnitsTypeEnum.kDatabaseMassUnits, UnitsTypeEnum.kKilogramMassUnits)
        Return Math.Round(kg, 4).ToString(System.Globalization.CultureInfo.InvariantCulture)
    Catch
        Return ""
    End Try
End Function

' Loại kết cấu BOM (Normal/Purchased/Phantom/Assembly…)
Private Function StructName(oRow As BOMRow) As String
    Try
        Select Case oRow.BOMStructure
            Case BOMStructureEnum.kNormalBOMStructure : Return "Normal"
            Case BOMStructureEnum.kPurchasedBOMStructure : Return "Purchased"
            Case BOMStructureEnum.kPhantomBOMStructure : Return "Phantom"
            Case BOMStructureEnum.kReferenceBOMStructure : Return "Reference"
            Case BOMStructureEnum.kInseparableBOMStructure : Return "Inseparable"
            Case Else : Return ""
        End Select
    Catch
        Return ""
    End Try
End Function

' Bọc lambda trả string an toàn
Private Function TryStr(f As Func(Of String)) As String
    Try : Return f().Trim() : Catch : Return "" : End Try
End Function

' Escape 1 ô CSV
Private Function Csv(s As String) As String
    If s Is Nothing Then s = ""
    If s.Contains(",") OrElse s.Contains("""") OrElse s.Contains(vbLf) OrElse s.Contains(vbCr) Then
        Return """" & s.Replace("""", """""") & """"
    End If
    Return s
End Function

' Tên file an toàn (bỏ ký tự cấm)
Private Function SafeName(s As String) As String
    For Each c As Char In System.IO.Path.GetInvalidFileNameChars()
        s = s.Replace(c, "_"c)
    Next
    Return s
End Function
