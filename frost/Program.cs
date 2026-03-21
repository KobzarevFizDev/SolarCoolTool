using System.Text;
using System.Threading.Tasks;
using Cake.Core;
using Cake.Core.Diagnostics;
using Cake.Frosting;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using Frost;
using System;
using System.Diagnostics;

public static class Program
{
    public static int Main(string[] args)
    {
        return new CakeHost()
            .UseContext<BuildContext>()
            .Run(args);
    }
}


public class BuildContext : FrostingContext
{

    public string PathToDist { get; set; }
    public string WinRarPath { get; set; }
    public string RarFilePath { get; set; }
    public BuildContext(ICakeContext context)
        : base(context)
    {
        PathToDist = context.Arguments.GetArgument("dist");
        WinRarPath = context.Arguments.GetArgument("winrar");
        RarFilePath = context.Arguments.GetArgument("rarpath");
    }
}

[TaskName("Build")]
public sealed class BuildTask : FrostingTask<BuildContext>
{
    public override void Run(BuildContext context)
    {
        base.Run(context);
    }
}

[TaskName("DeleteUnnecessaryFiles")]
public sealed class DeleteUnnecessaryFilesTask : FrostingTask<BuildContext>
{
    public override void Run(BuildContext context)
    {
        List<string> directoriesToDelete = new()
        {
            "astropy_iers_data",
            "sunpy",
            "pandas",
            "pandas.libs",
            "certifi",
            "charset_normalizer",
            "drms",
            "erfa",
            "tcl8",
            "yaml"
        };

        float totalSize = 0;
        foreach (var dir in directoriesToDelete)
        {
            string path = Path.Combine(context.PathToDist, "app", "_internal", dir);
            if (Path.Exists(path))
            {
                long sizeInBytes = Helpers.GetSizeOfDirectory(path);
                float mb = sizeInBytes / (float)1024 / (float)1024;
                totalSize += mb;
                Console.WriteLine($"Path = {path}. Size = {mb} Mb");
            }
            else
            {
                Console.WriteLine($"Path = {path} is not exists");
            }
        }

        Console.WriteLine($"Deleted = {totalSize} Mb");
    }
}

[TaskName("CleanPyQt")]
public sealed class CleanPyQtTask : FrostingTask<BuildContext>
{
    public override void Run(BuildContext context)
    {
        List<string> needToDelete = new()
        {
            "Qt5Qml.dll",
            "Qt5Network.dll",
            "Qt5QmlModels.dll",
            "Qt5DBus.dll",
            "Qt5Svg.dll",
            "Qt5WebSockets.dll",
            "Qt5Quick.dll"
        };

        float totalSize = 0;
        foreach (var dll in needToDelete)
        {
            string path = Path.Combine(context.PathToDist, "app", "_internal", "PyQt5", "Qt5", "bin", dll);
            if (Path.Exists(path))
            {
                long sizeInBytes = Helpers.GetSizeOfFile(path);
                float mb = sizeInBytes / (float)1024 / (float)1024;
                totalSize += mb;
                Console.WriteLine($"Path = {path}. Size = {mb} Mb");
            }
            else
            {
                Console.WriteLine($"Path = {path} is not exists");
            }
        }

        Console.WriteLine($"Deleted = {totalSize} Mb");
    }
}

[TaskName("Archive")]
public sealed class ArchiveTask : FrostingTask<BuildContext>
{
    public override void Run(BuildContext context)
    {
        Console.WriteLine($"WinRAR path: {context.WinRarPath}");
        Console.WriteLine($"Source path: {context.RarFilePath}");
        Console.WriteLine($"Destination path: {context.PathToDist}");

        if (!System.IO.File.Exists(context.WinRarPath))
        {
            Console.WriteLine($"ERROR: WinRAR not found at {context.WinRarPath}");
            return;
        }

        if (!System.IO.Directory.Exists(context.PathToDist))
        {
            Console.WriteLine($"ERROR: Source directory not found at {context.PathToDist}");
            return;
        }


        string archivePath = context.RarFilePath;
        string sourcePath = context.PathToDist;

        if (!archivePath.EndsWith(".rar", StringComparison.OrdinalIgnoreCase))
        {
            archivePath += ".rar";
        }

        string arguments = $"a -r \"{archivePath}\" \"{sourcePath}\"";

        Console.WriteLine($"Arguments: {arguments}");

        ProcessStartInfo startInfo = new ProcessStartInfo();
        startInfo.FileName = context.WinRarPath;
        startInfo.Arguments = arguments;
        startInfo.WindowStyle = ProcessWindowStyle.Normal;
        startInfo.UseShellExecute = true;
        startInfo.CreateNoWindow = false;

        try
        {
            using (Process process = Process.Start(startInfo))
            {
                if (process != null)
                {
                    process.WaitForExit();
                    Console.WriteLine($"WinRAR exited with code: {process.ExitCode}");

                    // Коды выхода WinRAR:
                    // 0 = успешно
                    // 1 = предупреждение (некоторые файлы не добавлены)
                    // 2 = фатальная ошибка
                    // 3 = ошибка CRC
                    // 4 = архив заблокирован
                    // 5 = недостаточно памяти
                    // 6 = ошибка доступа
                    // 7 = недостаточно дискового пространства

                    if (process.ExitCode != 0)
                    {
                        Console.WriteLine($"ERROR: WinRAR failed with exit code {process.ExitCode}");
                    }
                }
                else
                {
                    Console.WriteLine("ERROR: Failed to start WinRAR process");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Exception: {ex.Message}");
        }
    }
}

//"C:\Program Files\WinRAR\WinRAR.exe" a -r "D:\Python\SolarCoolTool\dist\app.rar" "D:\Python\SolarCoolTool\dist\app"

[TaskName("Default")]
public class DefaultTask : FrostingTask
{
    public override void Run(ICakeContext context)
    {
        base.Run(context);
    }
}