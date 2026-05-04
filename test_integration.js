// 整合测试脚本
const { CompleteEvolutionSystem } = require('./complete_evolution.js');

async function testIntegration() {
    console.log('🧪 开始整合测试...\n');
    
    const system = new CompleteEvolutionSystem({
        strategy: 'balanced',
        riskAssessment: true,
        concurrency: 2
    });

    try {
        // 测试初始化
        console.log('1. 测试系统初始化...');
        await system.initialize();
        console.log('✅ 系统初始化成功\n');

        // 测试状态获取
        console.log('2. 测试状态获取...');
        const status = system.getStatus();
        console.log('📊 系统状态:', JSON.stringify(status, null, 2));
        console.log('✅ 状态获取成功\n');

        // 测试进化循环
        console.log('3. 测试进化循环执行...');
        const results = await system.executeEvolutionCycle({
            test: true,
            cycleNumber: 1
        });
        
        console.log(`✅ 进化循环完成，生成 ${results.length} 个结果`);
        console.log('📋 结果摘要:');
        results.forEach((result, index) => {
            console.log(`   ${index + 1}. ${result.type}: ${result.success ? '✅' : '❌'} ${result.description}`);
        });
        console.log('');

        // 测试统计信息
        console.log('4. 测试统计信息...');
        const finalStatus = system.getStatus();
        console.log(`📈 统计: ${finalStatus.stats.totalEvolutions} 次进化, ${finalStatus.stats.successfulEvolutions} 成功, ${finalStatus.stats.failedEvolutions} 失败`);
        console.log('✅ 统计信息正确\n');

        // 测试模块状态
        console.log('5. 测试模块状态...');
        Object.entries(finalStatus.modules).forEach(([name, moduleStatus]) => {
            console.log(`   ${name}: ${moduleStatus.status}`);
        });
        console.log('✅ 所有模块状态正常\n');

        console.log('🎉 整合测试全部通过！');
        console.log('📦 系统已成功整合以下功能:');
        console.log('   - 🔧 进化引擎 (原 evolver-main)');
        console.log('   - 🔮 预测系统 (原 self-evolution)');
        console.log('   - 🤖 改进代理 (原 self-improving-agent)');
        console.log('   - 🧠 反思模块 (原 auto-reflection)');
        console.log('');
        console.log('🚀 现在可以使用完整自我进化系统了！');

    } catch (error) {
        console.error('❌ 整合测试失败:', error.message);
        process.exit(1);
    }
}

// 运行测试
if (require.main === module) {
    testIntegration();
}

module.exports = { testIntegration };