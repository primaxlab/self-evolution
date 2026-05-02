
// 会话自动启动脚本
import { autoStartFullSystem } from './auto_startup.js';

console.log('🤖 会话自动启动中...');

autoStartFullSystem()
    .then(system => {
        console.log('🎉 会话自动启动完成！');
        console.log('🚀 系统已准备好进行进化工作');
    })
    .catch(error => {
        console.error('❌ 自动启动错误:', error.message);
    });
