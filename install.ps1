$FITS_ARCHIVE_NAME = "FitsFiles.rar"
$TDPB_ARCHIVE_NAME = "ReleaseTDPB.rar"

function PrintBanner() {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
    chcp 65001 > $null  # Change code page to UTF-8
    Clear-Host
    
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════════════╗" -ForegroundColor DarkYellow
    Write-Host "  ║                                                  ║" -ForegroundColor DarkYellow
    Write-Host "  ║     ████████╗██████╗ ██████╗ ██████╗             ║" -ForegroundColor DarkYellow
    Write-Host "  ║     ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗            ║" -ForegroundColor DarkYellow
    Write-Host "  ║        ██║   ██║  ██║██████╔╝██████╔╝            ║" -ForegroundColor DarkYellow
    Write-Host "  ║        ██║   ██║  ██║██╔═══╝ ██╔══██╗            ║" -ForegroundColor DarkYellow
    Write-Host "  ║        ██║   ██████╔╝██║     ██████╔╝            ║" -ForegroundColor DarkYellow
    Write-Host "  ║        ╚═╝   ╚═════╝ ╚═╝     ╚═════╝             ║" -ForegroundColor DarkYellow
    Write-Host "  ║                                                  ║" -ForegroundColor DarkYellow
    Write-Host "  ║            INSTALLER v0.9.0                      ║" -ForegroundColor DarkYellow
    Write-Host "  ║            prestable version                     ║" -ForegroundColor DarkYellow
    Write-Host "  ║                                                  ║" -ForegroundColor DarkYellow
    Write-Host "  ╚══════════════════════════════════════════════════╝" -ForegroundColor DarkYellow
    Write-Host ""
}

function DownloadFITS() {
    try {
        if ( -Not(Test-Path $FITS_ARCHIVE_NAME) ) {
            Write-Host "Downloading demo FITS files ..."
            $url = "https://github.com/KobzarevFizDev/SolarCoolTool/releases/download/v0.9.0alpha/FitsFiles.rar"
            curl -o $FITS_ARCHIVE_NAME $url
            Write-Host "Downloaded" -ForegroundColor Green
        }
        else {
            Write-Host "FITS files is already downloaded" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Failed to download archive with FITS files. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red 
        }
        exit
    }
}

function DownloadTDPB() {
    try {
        if ( -Not(Test-Path $TDPB_ARCHIVE_NAME) ) {
            $tag = "v0.9.0alpha"
            $version = "v0.9.0"
            Write-Host "Downloading TDPB ..."
            curl -o $TDPB_ARCHIVE_NAME "https://github.com/KobzarevFizDev/SolarCoolTool/releases/download/$tag/TDPB_$version.rar"
            Write-Host "Archive with TDPB downloaded. Tag = $tag, Version = $version" -ForegroundColor Green
        }
        else {
            Write-Host "TDPB is already downloaded" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Failed to download archive with TDPB files. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red 
        }
        exit
    }
}

function ExtractFITS {
    try {
        $workspaceFolder = Get-Location
        $pathToArchive = Join-Path $workspaceFolder $FITS_ARCHIVE_NAME
        $destinationFolder = $workspaceFolder

        Write-Host $pathToArchive
        Write-Host $destinationFolder

        $process = Start-Process -FilePath "C:\Program Files\WinRAR\WinRAR.exe" -ArgumentList "x", "-y", "`"$pathToArchive`"", "`"$destinationFolder`"" -Wait -PassThru -NoNewWindow
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Success extracted" -ForegroundColor Green
        }
        else {
            Write-Host "Failed extracted" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Failed to extract archive with FITS files. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red 
        }
        exit
    }
}

function  ExtractTDPB {
    try {
        $workspaceFolder = Get-Location
        $pathToArchive = Join-Path $workspaceFolder $TDPB_ARCHIVE_NAME
        $destinationFolder = $workspaceFolder

        Write-Host $pathToArchive
        Write-Host $destinationFolder

        if ( -Not(Test-Path "C:\Program Files\WinRAR\WinRAR.exe") ) {
            Write-Host "WinRar is not installed. Exit"
            exit
        }

        $process = Start-Process -FilePath "C:\Program Files\WinRAR\WinRAR.exe" -ArgumentList "x", "-y", "`"$pathToArchive`"", "`"$destinationFolder`"" -Wait -PassThru -NoNewWindow
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Success extracted" -ForegroundColor Green
        }
        else {
            Write-Host "Failed extracted" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Failed to extract archive with TDPB. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red 
        }
        exit
    }
}

function DeleteGarbage {
    try {
        $userInput = Read-Host -Prompt "Do you want to delete downloaded archives? (Yes/No)"
        if ($userInput -eq "Yes") {
            $workspaceFolder = Get-Location
            $appArchive = Join-Path $workspaceFolder $TDPB_ARCHIVE_NAME
            $fitsArchive = Join-Path $workspaceFolder $FITS_ARCHIVE_NAME
            
            if (Test-Path $appArchive) {
                Remove-Item $appArchive
                Write-Host "Deleted: $appArchive" -ForegroundColor Green
            }
            else {
                Write-Host "Not found file: " $appArchive ".Skipped" -ForegroundColor Yellow
            }
            
            if (Test-Path $fitsArchive) {
                Remove-Item $fitsArchive
                Write-Host "Deleted: $fitsArchive" -ForegroundColor Green
            }
            else {
                Write-Host "Not found file: " $fitsArchive ". Skipped" -ForegroundColor Yellow
            }
            
            Write-Host "Cleanup complete" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Failed to delete garbage. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red 
        }
        exit
    }
}

function  CreateExportDirectory {
    try {
        $workspaceFolder = Get-Location
        $exportPath = Join-Path $workspaceFolder "ExportData"
        if ( -Not (Test-Path -Path $exportPath) ) {
            New-Item -Path $exportPath -ItemType Directory
            Write-Host "Created export directory. Path: " $exportPath
        }
        else {
            Write-Host "Directory for export is already exists. Path: " $exportPath
        }
    }
    catch {
        Write-Host "Failed to create export folder. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red
        }
        exit
    }
}

function CreateConfigFile {
    try {
        $workspaceFolder = Get-Location
        $pathToSolarImages = Join-Path $workspaceFolder "FitsFiles"
        $pathToExport = Join-Path $workspaceFolder "ExportData"
        $pathToConfigFile = Join-Path $workspaceFolder "app\configuration.txt"
        $settings = @"
STEP_FOR_A94 = [1]
STEP_FOR_A131 = [1]
STEP_FOR_A171 = [1]
STEP_FOR_A193 = [1]
STEP_FOR_A211 = [1]
STEP_FOR_A304 = [1]
STEP_FOR_A335 = [1]

MAX_NUMBER_OF_FRAMES_A94 = [10]
MAX_NUMBER_OF_FRAMES_A131 = [10]
MAX_NUMBER_OF_FRAMES_A171 = [10]
MAX_NUMBER_OF_FRAMES_A193 = [10]
MAX_NUMBER_OF_FRAMES_A211 = [10]
MAX_NUMBER_OF_FRAMES_A304 = [10]
MAX_NUMBER_OF_FRAMES_A335 = [10]

PATH_TO_SOLAR_IMAGES = [$pathToSolarImages]
PATH_TO_EXPORT = [$pathToExport]

INITIAL_CHANEL = [131]
"@

        $settings | Out-File -FilePath $pathToConfigFile -Encoding UTF8

        Write-Host "configuration.txt created. Path: $pathToConfigFile" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to create configuration.txt file. Exception: " $_.Exception.Message -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "Details: " $_.Exception.InnerException.Message -ForegroundColor Red
        }
        exit
    }
}

function CreateAppShortcut {
    param(
        [string]$AppName
    )
    
    try {
        $desktopPath = [System.Environment]::GetFolderPath("Desktop")
        $shortcutPath = Join-Path $desktopPath "$AppName.lnk" 
        $workspaceFolder = (Get-Location).Path
        $appExePath = Join-Path $workspaceFolder "app\app.exe"
        $pathToConfig = Join-Path $workspaceFolder "app\configuration.txt"
        
        if (-not (Test-Path $appExePath)) {
            throw "Application executable not found at: $appExePath"
        }
        
        if (-not (Test-Path $pathToConfig)) {
            Write-Host "Warning: Configuration file not found at: $pathToConfig" -ForegroundColor Yellow
        }
        
        Write-Host "Creating shortcut with:" -ForegroundColor Cyan
        Write-Host "  Target: $appExePath" -ForegroundColor Gray
        Write-Host "  Arguments: $pathToConfig" -ForegroundColor Gray
        Write-Host "  Working Directory: $workspaceFolder" -ForegroundColor Gray
        Write-Host "  Shortcut Path: $shortcutPath" -ForegroundColor Gray
        
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        
        $shortcut.TargetPath = $appExePath
        $shortcut.Arguments = $pathToConfig
        $shortcut.WorkingDirectory = $workspaceFolder
        $shortcut.Description = "Launch $AppName"
        
        $shortcut.Save()
        
        Write-Host "Successfully created shortcut: $shortcutPath" -ForegroundColor Green
        
        if (Test-Path $shortcutPath) {
            Write-Host "Shortcut verified!" -ForegroundColor Green
            return $true
        }
        else {
            throw "Shortcut file was not created"
        }
    }
    catch {
        Write-Host "Failed to create application shortcut: $_" -ForegroundColor Red
        Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
        
        if ($_.Exception.InnerException) {
            Write-Host "Inner exception: $($_.Exception.InnerException.Message)" -ForegroundColor Red
        }
        exit
    }
}

PrintBanner
DownloadTDPB
DownloadFITS
ExtractTDPB
ExtractFITS
DeleteGarbage
CreateExportDirectory
CreateConfigFile
CreateAppShortcut -AppName "TDPB"