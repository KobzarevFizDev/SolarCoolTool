using System;
using System.IO;

namespace Frost;

public static class Helpers
{
    public static long GetSizeOfDirectory(string path)
    {
        if (!Directory.Exists(path))
            throw new InvalidOperationException($"Path = {path} is not directory");

        long sizeInBytes = 0;

        foreach (string file in Directory.GetFiles(path))
        {
            FileInfo info = new FileInfo(file);
            sizeInBytes += info.Length;
        }

        foreach (string directory in Directory.GetDirectories(path))
        {
            sizeInBytes += GetSizeOfDirectory(directory);
        }

        return sizeInBytes;
    }

    public static long GetSizeOfFile(string path)
    {
        if (!File.Exists(path))
            throw new InvalidOperationException($"Path = {path} is not file");

        return new FileInfo(path).Length;
    }
}
