// Unified Evolution System Core
// 整合: evolver-main + self-evolution + self-improving-agent + auto-reflection

const { EvolutionEngine } = require('../engines/evolution_engine');
const { PredictiveSystem } = require('../systems/predictive_system');
const { ImprovementAgent } = require('../agents/improvement_agent');
const { ReflectionModule } = require('../modules/reflection_module');

class UnifiedEvolutionSystem {
    constructor(config = {}) {
        this.config = {
            strategy: config.strategy || 'balanced',
            riskAssessment: config.riskAssessment !== false,
            autoReflection: config.autoReflection !== false,
            concurrency: config.concurrency || 4,
            ...config
        };

        // 初始化所有整合的模块
        this.engines = {
            evolution: new EvolutionEngine(this.config),
            predictive: new PredictiveSystem(this.config),
            improvement: new ImprovementAgent(this.config),
            reflection: new ReflectionModule(this.config)
        };

        this.initialized = false;
        this.evolutionCycleCount = 0;
    }

    async initialize() {
        if (this.initialized) return;

        console.log('🚀 初始化统一进化系统...');
        
        // 并行初始化所有引擎
        await Promise.all([
            this.engines.evolution.initialize(),
            this.engines.predictive.initialize(),
            this.engines.improvement.initialize(),
            this.engines.reflection.initialize()
        ]);

        this.initialized = true;
        console.log('✅ 统一进化系统初始化完成');
    }

    async executeEvolutionCycle(context = {}) {
        if (!this.initialized) {
            await this.initialize();
        }

        this.evolutionCycleCount++;
        console.log(`🔄 执行第 ${this.evolutionCycleCount} 次进化循环...`);

        try {
            // 1. 预测性分析
            const analysis = await this.engines.predictive.analyze({
                ...context,
                cycleCount: this.evolutionCycleCount
            });

            // 2. 生成改进方案
            const improvements = await this.engines.improvement.generateImprovements(analysis);

            // 3. 反射验证
            const validated = await this.engines.reflection.validateImprovements(improvements);

            // 4. 执行进化
            const results = await this.engines.evolution.implementImprovements(validated);

            // 5. 学习反馈
            await this.learnFromCycle({
                analysis,
                improvements,
                validated,
                results,
                context
            });

            console.log(`✅ 第 ${this.evolutionCycleCount} 次进化循环完成`);
            return results;

        } catch (error) {
            console.error(`❌ 进化循环失败:`, error.message);
            await this.handleEvolutionError(error);
            throw error;
        }
    }

    async learnFromCycle(cycleData) {
        // 向所有引擎传递学习数据
        await Promise.all([
            this.engines.predictive.learn(cycleData),
            this.engines.improvement.learn(cycleData),
            this.engines.reflection.learn(cycleData),
            this.engines.evolution.learn(cycleData)
        ]);
    }

    async handleEvolutionError(error) {
        // 错误处理和学习
        const errorData = {
            error: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            cycleCount: this.evolutionCycleCount
        };

        await this.engines.reflection.recordError(errorData);
        await this.engines.evolution.handleError(errorData);
    }

    async startContinuousEvolution(intervalMs = 3600000) { // 默认1小时
        console.log('🌐 启动持续进化模式...');
        
        this.continuousMode = true;
        
        while (this.continuousMode) {
            try {
                await this.executeEvolutionCycle();
                await new Promise(resolve => setTimeout(resolve, intervalMs));
            } catch (error) {
                console.error('持续进化模式错误:', error);
                // 错误后等待更长时间
                await new Promise(resolve => setTimeout(resolve, intervalMs * 2));
            }
        }
    }

    stopContinuousEvolution() {
        this.continuousMode = false;
        console.log('⏹️ 停止持续进化模式');
    }

    getStatus() {
        return {
            initialized: this.initialized,
            cycleCount: this.evolutionCycleCount,
            continuousMode: this.continuousMode,
            config: this.config,
            engines: {
                evolution: this.engines.evolution.getStatus(),
                predictive: this.engines.predictive.getStatus(),
                improvement: this.engines.improvement.getStatus(),
                reflection: this.engines.reflection.getStatus()
            }
        };
    }
}

module.exports = { UnifiedEvolutionSystem };