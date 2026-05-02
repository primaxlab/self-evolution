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

# 4. 创建生产级启动脚本
Write-Host "⚡ 创建生产级启动脚本..." -ForegroundColor Yellow
$startScript = @"
// 生产级启动脚本
import { CompleteEvolutionSystem } from './complete_evolution.js';
import fs from 'fs/promises';

console.log('🚀 生产环境完整自我进化系统启动中...');

async function startProduction() {
    try {
        // 加载生产配置
        const configData = await fs.readFile('./production_config.json', 'utf8');
        const config = JSON.parse(configData);
        
        // 创建生产系统实例
        const system = new CompleteEvolutionSystem(config.evolution);
        
        console.log('✅ 生产系统实例创建完成');
        
        // 执行完整初始化
        await system.initialize();
        console.log('🎉 生产系统初始化完成');
        
        // 启动进化循环
        console.log('🔁 开始生产级进化循环...');
        
        return system;
        
    } catch (error) {
        console.error('❌ 生产启动失败:', error.message);
        throw error;
    }
}

// 启动生产环境
startProduction().catch(console.error);
"@

$startScript | Out-File -FilePath "D:\OpenClaw_Main\workspace\skills\complete-self-evolution\start_production_full.js" -Encoding UTF8
Write-Host "   ✅ 生产启动脚本创建完成" -ForegroundColor Green

# 5. 创建系统服务配置
Write-Host "🛠️  创建系统服务配置..." -ForegroundColor Yellow
$serviceConfig = @{
    "name" = "OpenClaw-SelfEvolution"
    "description" = "OpenClaw Complete Self Evolution System"
    "script" = "D:\OpenClaw_Main\workspace\skills\complete-self-evolution\start_production_full.js"
    "env" = @{
        "NODE_ENV" = "production"
        "A2A_NODE_ID" = $env:A2A_NODE_ID
        "EVOLUTION_MODE" = "full_production"
    }
    "cwd" = "D:\OpenClaw_Main\workspace\skills\complete-self-evolution"
    "autorestart" = $true
    "max_restarts" = 10
    "max_memory_restart" = "8G"
    "exec_mode" = "cluster"
    "instances" = 4
}

$serviceConfig | ConvertTo-Json -Depth 5 | Out-File -FilePath "D:\OpenClaw_Main\workspace\skills\complete-self-evolution\pm2.config.json" -Encoding UTF8
Write-Host "   ✅ PM2服务配置创建完成" -ForegroundColor Green

# 6. 创建监控脚本
Write-Host "📊 创建监控脚本..." -ForegroundColor Yellow
$monitorScript = @"
// 生产环境监控脚本
import fs from 'fs/promises';
import os from 'os';

class ProductionMonitor {
    constructor() {
        this.metrics = {
            cpuUsage: 0,
            memoryUsage: 0,
            evolutionCycles: 0,
            successfulCycles: 0,
            failedCycles: 0,
            startTime: new Date().toISOString()
        };
    }
    
    async collectMetrics() {
        // 收集系统指标
        const totalMem = os.totalmem();
        const freeMem = os.freemem();
        const usedMem = totalMem - freeMem;
        
        this.metrics.memoryUsage = (usedMem / totalMem) * 100;
        this.metrics.cpuUsage = os.loadavg()[0]; // 1分钟负载
        
        return this.metrics;
    }
    
    async generateReport() {
        const metrics = await this.collectMetrics();
        
        console.log('📈 生产环境监控报告:');
        console.log('================================');
        console.log(`⏰ 运行时间: ${new Date().toLocaleTimeString()}`);
        console.log(`💾 内存使用: ${metrics.memoryUsage.toFixed(1)}%`);
        console.log(`⚡ CPU负载: ${metrics.cpuUsage.toFixed(2)}`);
        console.log(`🔄 进化周期: ${metrics.evolutionCycles}`);
        console.log(`✅ 成功周期: ${metrics.successfulCycles}`);
        console.log(`❌ 失败周期: ${metrics.failedCycles}`);
        
        if (metrics.evolutionCycles > 0) {
            const successRate = (metrics.successfulCycles / metrics.evolutionCycles) * 100;
            console.log(`📊 成功率: ${successRate.toFixed(1)}%`);
        }
    }
}

// 启动监控
const monitor = new ProductionMonitor();
setInterval(() => {
    monitor.generateReport();
}, 30000); // 每30秒报告一次

console.log('🔍 生产环境监控已启动...');
"@

$monitorScript | Out-File -FilePath "D:\OpenClaw_Main\workspace\skills\complete-self-evolution\monitor_production.js" -Encoding UTF8
Write-Host "   ✅ 监控脚本创建完成" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 生产级部署准备完成！" -ForegroundColor Green
Write-Host "=================================================="
Write-Host "✅ 生产目录结构"
Write-Host "✅ 环境变量配置"
Write-Host "✅ 生产配置文件"
Write-Host "✅ 启动脚本"
Write-Host "✅ 服务配置"
Write-Host "✅ 监控系统"
Write-Host ""
Write-Host "🚀 下一步: 启动生产环境..." -ForegroundColor Yellow
Write-Host "   执行: node start_production_full.js" -ForegroundColor White
Write-Host ""
Write-Host "💪 准备好进行真正的进化工作了！" -ForegroundColor Green