param(
    [string]$Command
)

$PythonStr = "python"
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonStr = "py"
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonStr = "python3"
}

if ($Command -eq "install") {
    & $PythonStr -m pip install -r requirements.txt
}
elseif ($Command -eq "sim") {
    & $PythonStr simulation/src/main.py
}
elseif ($Command -eq "sim-continuous") {
    & $PythonStr simulation/src/continuous_runner.py
}
elseif ($Command -eq "paper") {
    & $PythonStr utils/build_paper.py --paper manuscript/paper.json
}
elseif ($Command -eq "clean") {
    Remove-Item -Recurse -Force manuscript/build/*
}
else {
    Write-Host "Usage: ./manage.ps1 [install|sim|paper|clean]"
}
