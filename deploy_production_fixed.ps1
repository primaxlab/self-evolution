# 完整生产级部署脚本 - PowerShell

Write-Host "🚀 开始完整生产级自我进化系统部署..." -ForegroundColor Green
Write-Host "=================================================="

# 1. 创建生产目录结构
Write-Host "📁 创建生产目录结构..." -ForegroundColor Yellow
$directories = @(
    "D:\OpenClaw_Main\workspace\evolution_production",
    "D:\OpenClaw_Main\workspace\evolution_data",
    "D:\OpenClaw_Main\workspace\evolution_backups",
    "D:\OpenClaw_Main\workspace\evolution_logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✅ 创建目录: $dir" -ForegroundColor Green
    } else {
        Write-Host "   ℹ️  目录已存在: $dir" -ForegroundColor Blue
    }
}

# 2. 设置生产环境变量
Write-Host "🔧 设置生产环境变量..." -ForegroundColor Yellow
$env:A2A_NODE_ID = "openclaw-prod-main-node-$(Get-Date -Format 'yyyyMMddHHmmss')"
$env:NODE_ENV = "production"
$env:EVOLUTION_MODE = "full_production"
$env:EVOLUTION_DATA_PATH = "D:\OpenClaw_Main\workspace\evolution_data"
$env:EVOLUTION_LOG_PATH = "D:\OpenClaw_Main\workspace\evolution_logs"

Write-Host "   ✅ A2A_NODE_ID: $env:A2A_NODE_ID" -ForegroundColor Green
Write-Host "   ✅ NODE_ENV: $env:NODE_ENV" -ForegroundColor Green
Write-Host "   ✅ EVOLUTION_MODE: $env:EVOLUTION_MODE" -ForegroundColor Green

# 3. 创建生产配置文件
Write-Host "📝 创建生产配置文件..." -ForegroundColor Yellow
$productionConfig = @{
    evolution = @{
        a2aNodeId = $env:A2A_NODE_ID
        strategy = "aggressive"
        riskAssessment = $true
        autoReflection = $true
        concurrency = 12
        validationStrictness = "very_high"
        timeHorizon = @("1h", "6h", "1d", "1w", "1m")
        rollbackMode = "soft"
        priorityStrategy = "impact_urgency_feasibility"
        workspacePath = "D:\OpenClaw_Main\workspace\evolution_production"
        dataPath = "D:\OpenClaw_Main\workspace\evolution_data"
        backupPath = "D:\OpenClaw_Main\workspace\evolution_backups"
        logLevel = "debug"
        maxEvolutionHistory = 5000
        autoBackupEnabled = $true
        realTimeMonitoring = $true
        performanceMetrics = $true
    }
    modules = @{
        evolution = @{
            enabled = $true
            maxConcurrentEvolutions = 8
            timeoutMs = 600000
            retryAttempts = 5
        }
        prediction = @{
            enabled = $true
            predictionHorizon = @("1h", "6h", "24h", "7d")
            confidenceThreshold = 0.85
        }
        improvement = @{
            enabled = $true
            maxImprovementsPerCycle = 50
            autoImplement = $true
            reviewRequired = $false
        }
        reflection = @{
            enabled = $true
            depth = "deep"
            autoCorrect = $true
            validationStrictness = "strict"
        }
    }
    security = @{
        encryptionEnabled = $true
        accessControl = "strict"
        auditLogging = $true
        dataRetentionDays = 180
        autoPurge = $true
    }
    performance = @{
        maxMemoryMb = 8192
        maxCpuPercent = 90
        monitoringIntervalMs = 2000
        autoScale = $true
    }
    network = @{
        evolveMapEnabled = $true
        nodeDiscovery = $true
        knowledgeSharing = $true
        updateFrequency = "30m"
    }
    metadata = @{
        version = "4.0.0-production"
        deploymentId = "openclaw-prod-$(Get-Date -Format 'yyyyMMddHHmmss')"
        owner = "杨元强"
        created = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        lastUpdated = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        environment = "production"
    }
}

$configJson = $productionConfig | ConvertTo-Json -Depth 10
$configJson | Out-File -FilePath "D:\OpenClaw_Main\workspace\skills\complete-self-evolution\production_config.json" -Encoding UTF8
Write-Host "   ✅ 生产配置文件创建完成" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 生产级部署准备完成！" -ForegroundColor Green
Write-Host "=================================================="
Write-Host "✅ 生产目录结构"
Write-Host "✅ 环境变量配置"
Write-Host "✅ 生产配置文件"
Write-Host ""
Write-Host "🚀 下一步: 启动生产环境..." -ForegroundColor Yellow
Write-Host ""
Write-Host "💪 准备好进行真正的进化工作了！" -ForegroundColor Green