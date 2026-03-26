function GetSizeOfDirectoryInMb {
    param (
        $fullPathToDir
    )

    $totalSizeDir = 0
    foreach ($i in Get-ChildItem $fullPathToDir -Recurse) {
        $totalSizeDir += (Get-Item $i.FullName).Length
    }

    return [math]::Round($totalSizeDir / 1024 / 1024, 3)
}

function RemoveGarbage {
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

    foreach ($item in Get-ChildItem $internalFolder) {

        if ($item -in $directoriesToDelete) {
            if (Test-Path -Path $item.FullName) {
                $sizeOfDirectory = GetSizeOfDirectoryInMb $item.FullName
                
                Remove-Item $item.FullName -Recurse -Force
                Write-Host "Deleted directory: " $item.FullName $sizeOfDirectory " Mb"
            }
        }
    }
    Write-Host "Garbage was deleted" -ForegroundColor Green
}

function ArchiveApp {
    $archiveName = "TDPB_" + (Get-Date -Format "yyyyMMddHHmmss") + ".zip"
    Write-Host $archiveName

    $workspaceFolder = Get-Location
    $inputFolder = Join-Path $workspaceFolder "dist\app"
    $outputArchive = Join-Path $workspaceFolder "dist\$archiveName"
    $distFolder = Join-Path $workspaceFolder "dist"

    if (-not (Test-Path $distFolder)) {
        New-Item -ItemType Directory -Path $distFolder -Force | Out-Null
    }

    Write-Host "Creating archive ..."

    try {
        # Check if input folder exists
        if (-not (Test-Path $inputFolder)) {
            throw "Input folder 'app' not found at $inputFolder"
        }

        Compress-Archive -Path "$inputFolder\*" -DestinationPath $outputArchive -Force
        
        $archiveSize = [math]::Round((Get-Item $outputArchive).Length / 1MB, 2)
        Write-Host "Success created" -ForegroundColor Green
        Write-Host "Result saved to $outputArchive. Size: $archiveSize Mb"
    }
    catch {
        Write-Host "Failed created: $_" -ForegroundColor Red
    }
}

function PackApp {
    param (
        [string]$Archivator
    )

    if ($archivator -eq "WinRar") {
        ArchiveAppWithRAR
    }
    else {
        ArchiveApp
    }
    
}

pyinstaller --clean --noconfirm .\app.spec
RemoveGarbage
PackApp -Archivator "ZIP"

