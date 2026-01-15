$source = "C:\Users\gerar\.gemini\antigravity\scratch\research_project_template"
$dest = "C:\Users\gerar\VScodeProjects\research_project_template"

Write-Host "Copying project from $source to $dest..."
Copy-Item -Path $source -Destination $dest -Recurse -Force
Write-Host "Done! You can now open the project in VS Code at: $dest"
