param (
    [Parameter(Mandatory=$true)][string]$sourceDir,
    [Parameter(Mandatory=$true)][string]$targetDir
 )

Get-ChildItem $sourceDir -filter "*.mid.txt" -recurse | `
    foreach{
        $targetFile = $targetDir + $_.FullName.SubString($sourceDir.Length);
        New-Item -ItemType File -Path $targetFile -Force;
        Copy-Item $_.FullName -destination $targetFile
    }
