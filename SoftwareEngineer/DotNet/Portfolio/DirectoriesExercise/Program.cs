using System.Collections.Generic;
using System.IO;

var salesFiles = FindFiles("stores");

foreach (var file in salesFiles)
{
    Console.WriteLine(file);
}

IEnumerable<string> FindFiles(string folderName)
{
    List<string> salesFiles = new List<string>();

    var foundFiles = Directory.EnumerateFiles(
        folderName, "*", SearchOption.AllDirectories);

    foreach (var file in foundFiles)
    {
        if (file.EndsWith("sales.json"))
        {
            salesFiles.Add(file);
        }
        Console.WriteLine(file);
    }

    return salesFiles;
}