# Create enhancement workflow
# PowerShell version of create-enhance.sh

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments,
    [switch]$Json,
    [switch]$Help
)

function Show-Help {
    Write-Host "Usage: create-enhance.ps1 [-Json] <enhancement_description>"
    Write-Host ""
    Write-Host "Creates a new enhancement workflow with condensed single-document planning."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Json    Output results in JSON format"
    Write-Host "  -Help    Show this help message"
    exit 0
}

if ($Help) {
    Show-Help
}

# Join arguments into description
$EnhancementDescription = $Arguments -join " "

if ([string]::IsNullOrWhiteSpace($EnhancementDescription)) {
    Write-Error "Usage: create-enhance.ps1 [-Json] <enhancement_description>"
    exit 1
}

# Get repository root
function Get-RepoRoot {
    $currentDir = Get-Location
    while ($currentDir) {
        if (Test-Path (Join-Path $currentDir ".git")) {
            return $currentDir.Path
        }
        if (Test-Path (Join-Path $currentDir ".specify")) {
            return $currentDir.Path
        }
        $parent = Split-Path $currentDir -Parent
        if ($parent -eq $currentDir) {
            break
        }
        $currentDir = $parent
    }
    return (Get-Location).Path
}

# Check if git is available
function Test-Git {
    try {
        $null = git --version 2>&1
        return $true
    } catch {
        return $false
    }
}

# Generate branch name from description (simplified version)
function Get-BranchName {
    param([string]$Description)

    # Stop words to filter out
    $stopWords = @(
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'should', 'would', 'could', 'can',
        'this', 'but', 'not', 'or', 'so', 'than', 'then', 'there'
    )

    # Convert to lowercase and split into words
    $words = $Description.ToLower() -split '\s+' | Where-Object { $_ -match '^[a-z0-9]+$' }

    # Filter out stop words and keep first 5 meaningful words
    $filteredWords = $words | Where-Object { $stopWords -notcontains $_ } | Select-Object -First 5

    # Join with hyphens
    return ($filteredWords -join '-')
}

$RepoRoot = Get-RepoRoot
$HasGit = Test-Git

Set-Location $RepoRoot

$SpecsDir = Join-Path $RepoRoot "specs"
if (-not (Test-Path $SpecsDir)) {
    New-Item -ItemType Directory -Path $SpecsDir | Out-Null
}

# Find highest enhance number
$Highest = 0
$EnhanceDir = Join-Path $SpecsDir "enhance"
if (Test-Path $EnhanceDir) {
    Get-ChildItem $EnhanceDir -Directory | ForEach-Object {
        if ($_.Name -match '^(\d+)') {
            $num = [int]$matches[1]
            if ($num -gt $Highest) {
                $Highest = $num
            }
        }
    }
}

$Next = $Highest + 1
$EnhanceNum = "{0:D3}" -f $Next

# Create branch name from description
$Words = Get-BranchName $EnhancementDescription
$BranchName = "enhance/$EnhanceNum-$Words"
$EnhanceId = "enhance-$EnhanceNum"

# Create git branch if git available
if ($HasGit) {
    try {
        git checkout -b $BranchName 2>&1 | Out-Null
    } catch {
        Write-Warning "[enhance] Git repository detected but branch creation failed: $_"
    }
} else {
    Write-Warning "[enhance] Git repository not detected; skipped branch creation for $BranchName" -WarningAction Continue
}

# Create enhancement directory
if (-not (Test-Path $EnhanceDir)) {
    New-Item -ItemType Directory -Path $EnhanceDir | Out-Null
}

$EnhancementDir = Join-Path $EnhanceDir "$EnhanceNum-$Words"
New-Item -ItemType Directory -Path $EnhancementDir | Out-Null

# Copy template
$TemplateFile = Join-Path $RepoRoot ".specify\extensions\workflows\enhance\enhancement-template.md"
$EnhancementFile = Join-Path $EnhancementDir "enhancement.md"

if (Test-Path $TemplateFile) {
    Copy-Item $TemplateFile $EnhancementFile
} else {
    "# Enhancement" | Out-File -FilePath $EnhancementFile -Encoding utf8
}

# Create symlink from spec.md to enhancement.md
$SpecLink = Join-Path $EnhancementDir "spec.md"
# Windows symlinks require admin rights, so we'll create a copy or use mklink
if ($PSVersionTable.Platform -eq 'Win32NT' -or $PSVersionTable.PSVersion.Major -lt 6) {
    # On Windows, try to create symlink, fall back to copy
    try {
        $null = cmd /c mklink "$SpecLink" "enhancement.md" 2>&1
    } catch {
        Copy-Item $EnhancementFile $SpecLink
    }
} else {
    # On Unix-like systems (PowerShell Core on Linux/Mac)
    New-Item -ItemType SymbolicLink -Path $SpecLink -Target "enhancement.md" -Force | Out-Null
}

# Set environment variable for current session
$env:SPECIFY_ENHANCE = $EnhanceId

if ($Json) {
    $result = @{
        ENHANCE_ID = $EnhanceId
        BRANCH_NAME = $BranchName
        ENHANCEMENT_FILE = $EnhancementFile
        ENHANCE_NUM = $EnhanceNum
    } | ConvertTo-Json -Compress
    Write-Output $result
} else {
    Write-Output "ENHANCE_ID: $EnhanceId"
    Write-Output "BRANCH_NAME: $BranchName"
    Write-Output "ENHANCEMENT_FILE: $EnhancementFile"
    Write-Output "ENHANCE_NUM: $EnhanceNum"
    Write-Output "SPECIFY_ENHANCE environment variable set to: $EnhanceId"
}
