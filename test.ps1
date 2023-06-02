function Get-FastestProxy {
    $url = 'https://proxy.ip3366.net/free/'
    $userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{0}.0.{1}.{2} Safari/537.36' -f (Get-Random -Minimum 60 -Maximum 91), (Get-Random -Minimum 0 -Maximum 9999), (Get-Random -Minimum 0 -Maximum 9999)

    $response = Invoke-WebRequest -Uri $url -Headers @{ 'User-Agent' = $userAgent }
    $htmlContent = $response.Content

    $tableRegex = '<table[^>]*class=["\']table table-bordered table-striped["\'][^>]*>.*?</table>'
    $tableHtml = $htmlContent | Select-String -Pattern $tableRegex -AllMatches | ForEach-Object { $_.Matches.Value }

    $headersRegex = '<th[^>]*>(.*?)</th>'
    $headers = ($tableHtml | Select-String -Pattern $headersRegex -AllMatches).Matches.Groups[1].Value.Trim() | ForEach-Object { $_ -replace '<.*?>', '' }

    $rowsRegex = '<tr[^>]*>.*?</tr>'
    $rows = ($tableHtml | Select-String -Pattern $rowsRegex -AllMatches).Matches.Value

    $fastestSpeed = [double]::PositiveInfinity
    $fastestAddress = ''
    $fastestArea = ''

    foreach ($row in $rows | Select-Object -Skip 1) {
        $dataRegex = '<td[^>]*>(.*?)</td>'
        $data = ($row | Select-String -Pattern $dataRegex -AllMatches).Matches.Groups[1].Value.Trim() | ForEach-Object { $_ -replace '<.*?>', '' }
        $proxy = @{}
        for ($i = 0; $i -lt $headers.Count; $i++) {
            $proxy[$headers[$i]] = $data[$i]
        }

        $responseSpeed = [double]($proxy['响应速度'] -replace '[^\d.]')
        if ($responseSpeed -lt $fastestSpeed) {
            $fastestSpeed = $responseSpeed
            $fastestAddress = "{0}:{1}" -f $proxy['IP'], $proxy['PORT']
            $fastestArea = $proxy['位置']
        }
    }

    [PSCustomObject]@{
        FastestAddress = $fastestAddress
        Area = $fastestArea
        Speed = $fastestSpeed
    }
}

function Set-SystemProxy($proxyAddress) {
    try {
        $regPath = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        Set-ItemProperty -Path $regPath -Name 'ProxyEnable' -Value 1
        Set-ItemProperty -Path $regPath -Name 'ProxyServer' -Value $proxyAddress
        Write-Host "System proxy set to: $proxyAddress"
    } catch {
        Write-Host "Failed to set system proxy: $_"
    }
}

$fastestProxyInfo = Get-FastestProxy
Write-Host "Fastest Proxy Address: $($fastestProxyInfo.FastestAddress)"
Write-Host "Area: $($fastestProxyInfo.Area)"
Write-Host "Response Speed: $($fastestProxyInfo.Speed) ms"

Set-SystemProxy $fastestProxyInfo.FastestAddress
