Do
    On Error Resume Next ' Ignora los errores
    Set objShell = WScript.CreateObject("WScript.Shell")
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set colItems = objWMIService.ExecQuery("Select * from Win32_Battery")

    If Err.Number <> 0 Then
        MsgBox "Error al acceder a la información de la batería: " & Err.Description, vbCritical, "Error"
        Err.Clear ' Limpia el error para continuar
    Else
        For Each objItem in colItems
            unplugged = (objItem.BatteryStatus = 1)
            percent = objItem.EstimatedChargeRemaining

            If (Not unplugged And percent > 85) Or (unplugged And percent < 20) Then
                MsgBox "Battery Level: " & percent & "%", vbInformation, "Battery Checker"
            End If
        Next
    End If

    ' Espera 3 segundos antes de volver a verificar
    WScript.Sleep(3000)
Loop
