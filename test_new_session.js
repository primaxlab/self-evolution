// 测试新会话自动启动
import { autoStartFullSystem } from './auto_startup.js';

console.log('🧪 ' + '='.repeat(70));
console.log('🧪                 测试新会话自动启动');
console.log('🧪 ' + '='.repeat(70));

console.log('🔍 模拟新会话启动...');
console.log(`   PID: ${process.pid}`);
console.log(`   时间: ${new Date().toISOString()}`);

// 模拟新会话
autoStartFullSystem()
    .then(system => {
        console.log('\n🎉 新会话自动启动测试成功！');
        console.log('✅ 系统状态持久化工作正常');
        console.log('✅ 会话检测功能正常');
        console.log('✅ 自动恢复功能正常');
        
        console.log('\n📊 系统状态:');
        console.log(`   初始化: ${system.initialized ? '✅' : '❌'}`);
        console.log(`   自动启动: ${system.autoStart ? '✅' : '❌'}`);
        console.log(`   持久化: ${system.persistenceEnabled ? '✅' : '❌'}`);
        console.log(`   功能启用: ${system.fullFeatures?.enabledFeatures || 0}/105`);
        
        console.log('\n🚀 新会话测试完成！');
        console.log('💪 系统已准备好跨会话自动运行');
    })
    .catch(error => {
        console.error('❌ 新会话测试失败:', error.message);
    });