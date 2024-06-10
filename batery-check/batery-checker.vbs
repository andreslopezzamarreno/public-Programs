Do
    Set objShell = WScript.CreateObject("WScript.Shell")
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set colItems = objWMIService.ExecQuery("Select * from Win32_Battery")

    For Each objItem in colItems
        plugged = (objItem.BatteryStatus = 1)  ' True si está conectada, False si no lo está
        percent = objItem.EstimatedChargeRemaining

        If (Not plugged And percent > 85) Or (plugged And percent < 20) Then
            MsgBox "Battery Level: " & percent & "%", vbInformation, "Battery Checker"
        End If
    Next

    ' Espera 3 segundos antes de volver a verificar
    WScript.Sleep(3000)

Loop
