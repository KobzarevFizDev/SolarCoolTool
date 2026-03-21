function GetSizeOfDirectoryInMb {
    param (
        $fullPathToDir
    )

    $workspaceFolder = Get-Location
    $internalFolder = Join-Path $workspaceFolder "dist\app\_internal"
    $directoriesToDelete = @(
        "astropy_iers_data",
        "sunpy",
        "pandas",
        "pandas.libs",
        "certifi",
        "charset_normalizer",
        "drms",
        "erfa",
        "tcl8",
        "yaml")

    $totalSizeDir = 0
    foreach ($i in Get-ChildItem $fullPathToDir -Recurse) {
        $totalSizeDir += (Get-Item $i.FullName).Length
    }

    return [math]::Round($totalSizeDir / 1024 / 1024, 3)
}

function RemoveGarbage {
    foreach ($item in Get-ChildItem $internalFolder) {

        if ($item -in $directoriesToDelete) {
            if(Test-Path -Path $item.FullName) {
                $sizeOfDirectory = GetSizeOfDirectoryInMb $item.FullName
                
                Remove-Item $item.FullName -Recurse -Force
                Write-Host "Deleted directory: " $item.FullName $sizeOfDirectory " Mb"
            }
        }
    }
    Write-Host "Garbage was deleted" -ForegroundColor Green
}

function Archive {
    $archiveName = "TDPB_" + (Get-Date -Format "yyyyMMddHHmmss") + ".rar"
    Write-Host $archiveName

    $workspaceFolder = Get-Location
    $inputFolder = Join-Path $workspaceFolder "dist\app"
    $outputArchive = Join-Path $workspaceFolder "dist\$archiveName"

    Write-Host "Creating archive ..."

    $process = Start-Process -FilePath "C:\Program Files\WinRAR\WinRAR.exe" -ArgumentList "a", "-r", "`"$outputArchive`"", "`"$inputFolder`"" -Wait -PassThru -NoNewWindow
    if ($process.ExitCode -eq 0){
        $archiveSize = [math]::Round((Get-Item $outputArchive).Length / 1MB, 2)
        Write-Host "Success created" -ForegroundColor Green
    } else {
        Write-Host "Failed created" -ForegroundColor Red
    }

}

RemoveGarbage
Archive

