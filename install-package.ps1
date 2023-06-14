param (
    [Parameter(Mandatory=$true)]
    [string]$Name
)

# Obtener la ruta completa del archivo .ps1
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Obtener el directorio actual antes de cambiarlo
$previousPath = Get-Location

# Construir la ruta de la carpeta
$folderPath = Join-Path -Path $scriptPath -ChildPath "packages\$Name"

# Cambiar al directorio de la carpeta
Set-Location -Path $folderPath

# Ejecutar el comando "pip install ."
pip install .

# Volver al directorio anterior
Set-Location -Path $previousPath