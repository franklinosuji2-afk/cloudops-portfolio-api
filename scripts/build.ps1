# scripts/build.ps1 - Package lambdas for deployment
$ErrorActionPreference = 'Stop'
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path dist | Out-Null

$build = 'dist\build'
New-Item -ItemType Directory -Path $build | Out-Null

# Install runtime deps into build dir
pip install -r requirements.txt -t $build --quiet

# Copy source (handlers + utils)
Copy-Item -Recurse src\handlers $build\
Copy-Item -Recurse src\utils $build\

# Zip it
Compress-Archive -Path $build\* -DestinationPath dist\lambda.zip -Force
Remove-Item -Recurse -Force $build
Write-Host 'Built dist\lambda.zip'
