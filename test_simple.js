// 简单测试脚本
import { CompleteEvolutionSystem } from './complete_evolution.js';

console.log('🚀 开始启动完整自我进化系统...');

const system = new CompleteEvolutionSystem({
    strategy: 'balanced',
    riskAssessment: true,
    autoReflection: true,
    concurrency: 2
});

console.log('✅ 进化系统实例创建成功！');
console.log('📋 配置信息:', JSON.stringify(system.config, null, 2));

// 尝试初始化
async function testInitialize() {
    try {
        console.log('🔄 尝试初始化系统...');
        await system.initialize();
        console.log('🎉 系统初始化成功！');
        
        // 显示模块状态
        console.log('\n📊 模块状态:');
        Object.entries(system.modules).forEach(([name, module]) => {
            console.log(`   ${name}: ${module.status}`);
        });
        
    } catch (error) {
        console.error('❌ 初始化失败:', error.message);
        console.error('详细错误:', error.stack);
    }
}

testInitialize();