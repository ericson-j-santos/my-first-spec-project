<#
.SYNOPSIS
    Cria um novo spec SDD a partir de um exemplo existente ou de templates.
.EXAMPLE
    .\new-spec.ps1
    .\new-spec.ps1 -SpecsPath "outra\pasta\specs"
#>
param(
    [string]$SpecsPath     = (Join-Path $PSScriptRoot ".sdd\specs"),
    [string]$TemplatesPath = (Join-Path $PSScriptRoot ".sdd\settings\templates\specs"),
    [string]$Lang          = "pt-br"
)

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Write-Banner {
    param([string]$Text, [string]$Color = "Cyan")
    $line = "=" * 54
    Write-Host ""
    Write-Host $line -ForegroundColor $Color
    Write-Host ("  " + $Text) -ForegroundColor $Color
    Write-Host $line -ForegroundColor $Color
    Write-Host ""
}

function Write-Step {
    param([int]$N, [string]$Text)
    Write-Host ""
    Write-Host "  [PASSO $N] $Text" -ForegroundColor Yellow
    Write-Host ""
}

function Read-ValidString {
    param([string]$Prompt, [string]$Default = "", [int]$MinLen = 1)
    while ($true) {
        if ($Default) {
            $raw = Read-Host "  $Prompt [$Default]"
        } else {
            $raw = Read-Host "  $Prompt"
        }
        if ([string]::IsNullOrWhiteSpace($raw) -and $Default -ne "") { return $Default }
        $raw = $raw.Trim()
        if ($raw.Length -ge $MinLen) { return $raw }
        Write-Host "  Valor muito curto (minimo $MinLen caractere(s))." -ForegroundColor Red
    }
}

function Read-ValidInt {
    param([string]$Prompt, [int]$Min, [int]$Max)
    while ($true) {
        $raw = Read-Host "  $Prompt (${Min}-${Max})"
        $n = 0
        if ([int]::TryParse($raw.Trim(), [ref]$n) -and $n -ge $Min -and $n -le $Max) {
            return $n
        }
        Write-Host "  Digite um numero entre $Min e $Max." -ForegroundColor Red
    }
}

function Slugify {
    param([string]$Text)
    # Decompoe acentos via normalizacao Unicode, remove nao-ASCII, limpa hifens
    $normalized = $Text.Normalize([System.Text.NormalizationForm]::FormD)
    $ascii = [System.Text.RegularExpressions.Regex]::Replace($normalized, '[^\x00-\x7F]', '')
    $s = $ascii.ToLower() -replace '[^a-z0-9-]', '-' -replace '-{2,}', '-'
    return $s.Trim('-')
}

function Get-MdFileNames {
    param([string]$DirPath)
    $files = Get-ChildItem $DirPath -Filter "*.md" -ErrorAction SilentlyContinue
    return ($files | Select-Object -ExpandProperty BaseName) -join ", "
}

function Show-FilePreview {
    param([string]$FilePath, [int]$MaxLines = 20)
    if (-not (Test-Path $FilePath)) { return }
    $name = Split-Path $FilePath -Leaf
    Write-Host "  +-- Preview: $name" -ForegroundColor DarkGray
    Get-Content $FilePath -Encoding UTF8 | Select-Object -First $MaxLines | ForEach-Object {
        Write-Host "  |  $_" -ForegroundColor DarkGray
    }
    Write-Host "  +--" -ForegroundColor DarkGray
    Write-Host ""
}

function Get-TemplateFile {
    param([string]$BaseName)
    $ptbr = Join-Path $TemplatesPath "$BaseName.$Lang.md"
    $en   = Join-Path $TemplatesPath "$BaseName.md"
    if (Test-Path $ptbr) { return $ptbr }
    if (Test-Path $en)   { return $en }
    return $null
}

function Build-MetaHeader {
    param([hashtable]$Info)
    $lines = @("<!--")
    $lines += "  Feature   : " + $Info.Title
    $lines += "  Slug      : " + $Info.Slug
    $lines += "  Criado em : " + $Info.Date
    $lines += "  Modo      : " + $Info.Mode
    if ($Info.Author) { $lines += "  Autor     : " + $Info.Author }
    if ($Info.Desc)   { $lines += "  Descricao : " + $Info.Desc }
    $lines += "--" + ">"
    $lines += ""
    return ($lines -join "`r`n")
}

# ---------------------------------------------------------------------------
# INICIO
# ---------------------------------------------------------------------------

Write-Banner "SDD -- Criar Novo Spec"

if (-not (Test-Path $SpecsPath)) {
    Write-Host "  Pasta de specs nao encontrada: $SpecsPath" -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------------------
# PASSO 1 -- Modo de criacao
# ---------------------------------------------------------------------------

Write-Step 1 "Modo de criacao"
Write-Host "  [1] Baseado em exemplo existente  (copia e adapta um spec pronto)" -ForegroundColor White
Write-Host "  [2] A partir de templates em branco (preenche placeholders)"       -ForegroundColor White
Write-Host ""

$mode = Read-ValidInt -Prompt "Modo" -Min 1 -Max 2

# ---------------------------------------------------------------------------
# PASSO 2 -- Selecionar fonte
# ---------------------------------------------------------------------------

$sourceFiles = @{}
$sourceLabel = ""

if ($mode -eq 1) {

    Write-Step 2 "Selecionar exemplo base"

    $examples = @(Get-ChildItem -Path $SpecsPath -Directory |
        Where-Object { (Get-ChildItem $_.FullName -Filter "*.md" -ErrorAction SilentlyContinue).Count -gt 0 })

    if ($examples.Count -eq 0) {
        Write-Host "  Nenhum exemplo encontrado em $SpecsPath" -ForegroundColor Red
        Write-Host "  Crie um spec manualmente ou use o modo 2." -ForegroundColor DarkGray
        exit 1
    }

    Write-Host "  Exemplos disponiveis:" -ForegroundColor White
    Write-Host ""
    for ($i = 0; $i -lt $examples.Count; $i++) {
        $fileList = Get-MdFileNames $examples[$i].FullName
        Write-Host ("  [{0}] {1}" -f ($i + 1), $examples[$i].Name) -ForegroundColor Yellow
        Write-Host "       Arquivos: $fileList" -ForegroundColor DarkGray
    }
    Write-Host ""

    $sel    = Read-ValidInt -Prompt "Numero do exemplo" -Min 1 -Max $examples.Count
    $picked = $examples[$sel - 1]
    $sourceLabel = "exemplo: " + $picked.Name

    Get-ChildItem $picked.FullName -Filter "*.md" | ForEach-Object {
        $sourceFiles[$_.BaseName] = $_.FullName
    }

    Write-Host ""
    Write-Host "  Selecionado: " -NoNewline; Write-Host $picked.Name -ForegroundColor Green
    Write-Host ""
    Show-FilePreview (Join-Path $picked.FullName "requirements.md")

} else {

    Write-Step 2 "Selecionar templates"

    $templateNames = @("requirements", "design", "tasks", "research")
    $available     = @()
    foreach ($base in $templateNames) {
        $f = Get-TemplateFile $base
        if ($f) { $available += [pscustomobject]@{ Base = $base; Path = $f } }
    }

    if ($available.Count -eq 0) {
        Write-Host "  Nenhum template encontrado em $TemplatesPath" -ForegroundColor Red
        exit 1
    }

    Write-Host "  Templates disponiveis ($Lang):" -ForegroundColor White
    Write-Host ""
    for ($i = 0; $i -lt $available.Count; $i++) {
        Write-Host ("  [{0}] {1}" -f ($i + 1), $available[$i].Base) -ForegroundColor Yellow
    }
    Write-Host ""

    $rawSel = Read-Host "  Numeros dos templates (ex: 1 2  ou  1,2,3)"
    $chosen = ($rawSel -split '[, ]+') | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }

    foreach ($n in $chosen) {
        if ($n -ge 1 -and $n -le $available.Count) {
            $entry = $available[$n - 1]
            $sourceFiles[$entry.Base] = $entry.Path
        }
    }

    if ($sourceFiles.Count -eq 0) {
        Write-Host "  Nenhum template valido selecionado. Saindo." -ForegroundColor Red
        exit 1
    }

    $sourceLabel = "templates em branco ($Lang)"
    Write-Host ""
    Write-Host "  Templates selecionados: " -NoNewline
    Write-Host ($sourceFiles.Keys -join ", ") -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# PASSO 3 -- Dados da nova feature
# ---------------------------------------------------------------------------

Write-Step 3 "Dados da nova feature"

$featureTitle = Read-ValidString -Prompt "Titulo da feature (ex: Autenticacao de Usuarios)" -MinLen 3
$autoSlug     = Slugify $featureTitle
$featureSlug  = Read-ValidString -Prompt "Slug/pasta" -Default $autoSlug -MinLen 2
$featureSlug  = Slugify $featureSlug

$featureDesc   = (Read-Host "  Descricao curta (opcional, Enter para pular)").Trim()
$featureAuthor = (Read-Host "  Autor (opcional, Enter para pular)").Trim()

# ---------------------------------------------------------------------------
# PASSO 4 -- Preenchimento interativo de placeholders (modo 2 apenas)
# ---------------------------------------------------------------------------

$tplVars = @{
    INTRODUCAO              = "Este documento define os requisitos para a feature `"$featureTitle`"."
    "AREA_DO_REQUISITO_1"   = "Requisito principal"
    "AREA_DO_REQUISITO_2"   = "Requisito secundario"
    PAPEL                   = "usuario"
    CAPACIDADE              = "[descreva a capacidade desejada]"
    BENEFICIO               = "[descreva o beneficio esperado]"
}

if ($mode -eq 2) {
    Write-Host ""
    Write-Host "  --- Preenchimento do requirements.md ---" -ForegroundColor White

    $intro = (Read-Host "  Introducao do documento (Enter para usar o padrao)").Trim()
    if ($intro) { $tplVars["INTRODUCAO"] = $intro }

    $r1 = (Read-Host "  Nome do Requisito 1 (Enter: 'Requisito principal')").Trim()
    if ($r1) { $tplVars["AREA_DO_REQUISITO_1"] = $r1 }

    $r2 = (Read-Host "  Nome do Requisito 2 (Enter: 'Requisito secundario')").Trim()
    if ($r2) { $tplVars["AREA_DO_REQUISITO_2"] = $r2 }

    $papel = (Read-Host "  Papel do usuario (ex: analista, admin - Enter: 'usuario')").Trim()
    if ($papel) { $tplVars["PAPEL"] = $papel }
}

# ---------------------------------------------------------------------------
# PASSO 5 -- Criar arquivos
# ---------------------------------------------------------------------------

Write-Step 4 "Criando arquivos"

$destPath = Join-Path $SpecsPath $featureSlug

if (Test-Path $destPath) {
    Write-Host "  Aviso: a pasta '$featureSlug' ja existe." -ForegroundColor Yellow
    $ow = (Read-Host "  Sobrescrever arquivos existentes? (s/N)").Trim()
    if ($ow.ToLower() -ne 's') {
        Write-Host "  Operacao cancelada." -ForegroundColor DarkGray
        exit 0
    }
}

New-Item -ItemType Directory -Force -Path $destPath | Out-Null

$metaHeader = Build-MetaHeader @{
    Title  = $featureTitle
    Slug   = $featureSlug
    Date   = (Get-Date -Format "yyyy-MM-dd")
    Mode   = $sourceLabel
    Author = $featureAuthor
    Desc   = $featureDesc
}

$utf8 = [System.Text.Encoding]::UTF8
$createdFiles = @()

foreach ($base in $sourceFiles.Keys) {
    $srcPath = $sourceFiles[$base]
    $content = [System.IO.File]::ReadAllText($srcPath, $utf8)

    if ($mode -eq 1) {
        # Troca referências ao slug antigo pelo novo
        $content = $content -replace [regex]::Escape($picked.Name), $featureSlug

        # Atualiza titulo H1 do design.md  (linha: # Documento de Design - Titulo)
        $content = $content -replace '(?m)^(# Documento de Design\s*[-]+\s*)(.+)$', ('${1}' + $featureTitle)

        # Atualiza paragrafo de introducao no requirements.md
        $introNew = $tplVars["INTRODUCAO"]
        $content  = $content -replace '(?s)(## Introdu[^#\r\n]+\r?\n\r?\n)([^\r\n]+)', ('${1}' + $introNew)

    } else {
        # Substitui placeholders {{VAR}} com valores fornecidos
        foreach ($key in $tplVars.Keys) {
            $content = $content -replace ([regex]::Escape("{{$key}}")), $tplVars[$key]
        }
    }

    $finalContent = $metaHeader + $content
    $destFile = Join-Path $destPath "$base.md"
    [System.IO.File]::WriteAllText($destFile, $finalContent, $utf8)
    $createdFiles += $destFile

    Write-Host "  [OK] $base.md" -ForegroundColor Green
    Write-Host "       -> $destFile" -ForegroundColor DarkGray
}

# ---------------------------------------------------------------------------
# RESUMO FINAL
# ---------------------------------------------------------------------------

Write-Banner "Spec criado com sucesso!" "Green"

Write-Host "  Feature   : " -NoNewline; Write-Host $featureTitle -ForegroundColor Yellow
Write-Host "  Slug      : " -NoNewline; Write-Host $featureSlug  -ForegroundColor Cyan
Write-Host "  Pasta     : " -NoNewline; Write-Host $destPath     -ForegroundColor Cyan
Write-Host "  Arquivos  : " -NoNewline; Write-Host "$($createdFiles.Count) criado(s)" -ForegroundColor White
Write-Host "  Baseado em: " -NoNewline; Write-Host $sourceLabel  -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Proximos passos:" -ForegroundColor Yellow
Write-Host "    1. Abra os arquivos em: $destPath"
Write-Host "    2. Substitua o conteudo pelo da sua feature real"
Write-Host "    3. Remova o bloco de metadados quando nao precisar mais"
Write-Host ""

Show-FilePreview (Join-Path $destPath "requirements.md")

Write-Host "  Pronto! Execute novamente para criar outra feature." -ForegroundColor Cyan
Write-Host ""

# Retorna lista de arquivos criados (util em automacao/pipeline)
return $createdFiles
