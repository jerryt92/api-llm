$project_dir = Get-Location
$env:PYTHONPATH = "$project_dir;$env:PYTHONPATH"
Write-Host "project_dir: $project_dir"