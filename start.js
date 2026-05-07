#!/usr/bin/env node
/**
 * 自我进化系统 - 启动脚本
 * Node.js Version - 完整替代 Python 版本
 */

const { EvolutionEngine } = require('./src/core/evolution-engine');

// 颜色输出
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    dim: '\x1b[2m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

async function main() {
    log('\n' + '='.repeat(70), 'cyan');
    log('      SELF-EVOLUTION SYSTEM v2.0.0 (Node.js)', 'bright');
    log('      完整解决 OpenClaw 上下文超限问题', 'dim');
    log('='.repeat(70), 'cyan');
    
    // 加载配置
    let configPath = null;
    const args = process.argv.slice(2);
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--config' || args[i] === '-c') {
            configPath = args[i + 1];
            i++;
        }
    }

    // 创建进化引擎
    const engine = new EvolutionEngine(configPath);

    try {
        // 初始化
        log('\n[Phase 1] System Initialization', 'yellow');
        log('-'.repeat(40), 'dim');
        await engine.initialize();

        // 解决上下文超限
        log('\n[Phase 2] Solving Context Overflow', 'yellow');
        log('-'.repeat(40), 'dim');
        const solution = await engine.solveContextOverflow();
        
        if (solution.success) {
            log('✓ Context overflow resolved!', 'green');
        } else {
            log('⚠ Context problem not fully resolved', 'yellow');
        }

        // 运行完整进化
        log('\n[Phase 3] Running Full Evolution', 'yellow');
        log('-'.repeat(40), 'dim');
        const evolutionResult = await engine.evolve('full');

        if (evolutionResult.success) {
            log('✓ Full evolution completed!', 'green');
        } else {
            log('⚠ Evolution completed with warnings', 'yellow');
        }

        // 显示最终状态
        log('\n' + '='.repeat(70), 'cyan');
        log('      SYSTEM RUNNING - All modules active', 'bright');
        log('='.repeat(70), 'cyan');
        
        log('\n[System State]', 'yellow');
        const state = engine.getSystemState();
        log(`  Session ID:     ${state.sessionId}`, 'dim');
        log(`  Version:        ${state.version}`, 'dim');
        log(`  Evolutions:     ${state.evolutionCount}`, 'dim');
        log(`  Uptime:         ${(state.uptime / 1000).toFixed(2)}s`, 'dim');
        log(`  Platform:       ${state.platform} / Node ${state.nodeVersion}`, 'dim');
        log(`  CPU Cores:      ${state.cpuCores}`, 'dim');
        log(`  Memory (Heap):  ${(state.heapUsed / 1024 / 1024).toFixed(2)} MB / ${(state.heapTotal / 1024 / 1024).toFixed(2)} MB`, 'dim');

        // 保持运行
        log('\n[Info] System running. Press Ctrl+C to exit.', 'dim');
        
        // 阻止进程退出
        await new Promise(() => {});

    } catch (error) {
        log(`\n✗ Error: ${error.message}`, 'red');
        console.error(error.stack);
    }
}

// 处理 Ctrl+C
process.on('SIGINT', async () => {
    console.log('\n\nShutting down...');
    process.exit(0);
});

main().catch(console.error);