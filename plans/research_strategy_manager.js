// 🧠 研究策略管理器 - 完整实现
class ResearchStrategyManager {
    constructor() {
        this.strategies = {
            EXPLORATORY: {
                name: '探索性研究',
                description: '广泛探索主题，发现新的信息源和观点',
                parameters: {
                    maxDepth: 5,
                    timeout: 30000,
                    minSources: 3
                },
                execute: async (engine, topic, params = {}) => {
                    return await engine.exploratoryResearch(topic, params.maxDepth || 5);
                }
            },
            
            TARGETED: {
                name: '目标导向研究',
                description: '针对特定网站或资源进行深度信息提取',
                parameters: {
                    extractionSelectors: {},
                    waitUntil: 'networkidle',
                    timeout: 45000
                },
                execute: async (engine, url, params = {}) => {
                    return await engine.targetedResearch(url, params.extractionSelectors || {});
                }
            },
            
            COMPARATIVE: {
                name: '比较分析研究',
                description: '对比多个来源的信息，进行差异分析',
                parameters: {
                    urls: [],
                    comparisonCriteria: [],
                    analysisDepth: 'standard'
                },
                execute: async (engine, urls, params = {}) => {
                    return await engine.comparativeResearch(urls, params.comparisonCriteria || []);
                }
            },
            
            VERIFICATION: {
                name: '验证性研究',
                description: '验证特定主张或信息的真实性',
                parameters: {
                    claim: '',
                    sources: [],
                    verificationThreshold: 0.6
                },
                execute: async (engine, claim, params = {}) => {
                    return await engine.verificationResearch(claim, params.sources || []);
                }
            }
        };
        
        this.researchHistory = [];
        this.performanceMetrics = {};
    }

    // 🎯 执行研究策略
    async executeStrategy(strategyType, ...args) {
        const strategy = this.strategies[strategyType];
        if (!strategy) {
            throw new Error(`未知的研究策略: ${strategyType}`);
        }
        
        const startTime = Date.now();
        
        try {
            const result = await strategy.execute(...args);
            const executionTime = Date.now() - startTime;
            
            // 记录研究历史
            this.recordResearch({
                strategy: strategyType,
                parameters: args.slice(1),
                executionTime,
                success: true,
                result: this.sanitizeResult(result)
            });
            
            // 更新性能指标
            this.updatePerformanceMetrics(strategyType, executionTime, true);
            
            return result;
            
        } catch (error) {
            const executionTime = Date.now() - startTime;
            
            this.recordResearch({
                strategy: strategyType,
                parameters: args.slice(1),
                executionTime,
                success: false,
                error: error.message
            });
            
            this.updatePerformanceMetrics(strategyType, executionTime, false);
            
            throw error;
        }
    }

    // 📊 记录研究活动
    recordResearch(record) {
        const researchRecord = {
            id: this.generateId(),
            timestamp: new Date().toISOString(),
            ...record
        };
        
        this.researchHistory.push(researchRecord);
        
        // 保持历史记录大小
        if (this.researchHistory.length > 1000) {
            this.researchHistory = this.researchHistory.slice(-1000);
        }
        
        return researchRecord;
    }

    // 📈 更新性能指标
    updatePerformanceMetrics(strategyType, executionTime, success) {
        if (!this.performanceMetrics[strategyType]) {
            this.performanceMetrics[strategyType] = {
                totalExecutions: 0,
                successfulExecutions: 0,
                totalTime: 0,
                avgTime: 0,
                successRate: 0
            };
        }
        
        const metrics = this.performanceMetrics[strategyType];
        metrics.totalExecutions++;
        metrics.totalTime += executionTime;
        metrics.avgTime = metrics.totalTime / metrics.totalExecutions;
        
        if (success) {
            metrics.successfulExecutions++;
        }
        
        metrics.successRate = metrics.successfulExecutions / metrics.totalExecutions;
    }

    // 🎪 智能策略推荐
    recommendStrategy(topic, constraints = {}) {
        const recommendations = [];
        
        // 基于主题类型的推荐
        if (this.isBroadTopic(topic)) {
            recommendations.push({
                strategy: 'EXPLORATORY',
                confidence: 0.8,
                reason: '广泛主题适合探索性研究'
            });
        }
        
        if (this.isSpecificQuery(topic)) {
            recommendations.push({
                strategy: 'TARGETED',
                confidence: 0.7,
                reason: '具体查询适合目标导向研究'
            });
        }
        
        if (this.involvesComparison(topic)) {
            recommendations.push({
                strategy: 'COMPARATIVE',
                confidence: 0.9,
                reason: '涉及比较的主题适合比较分析'
            });
        }
        
        if (this.isVerificationNeeded(topic)) {
            recommendations.push({
                strategy: 'VERIFICATION',
                confidence: 0.85,
                reason: '需要验证的主题适合验证性研究'
            });
        }
        
        // 基于性能历史调整置信度
        recommendations.forEach(rec => {
            const metrics = this.performanceMetrics[rec.strategy];
            if (metrics && metrics.successRate > 0) {
                rec.confidence *= metrics.successRate;
            }
        });
        
        // 按置信度排序
        return recommendations.sort((a, b) => b.confidence - a.confidence);
    }

    // 🔍 主题分析工具
    isBroadTopic(topic) {
        const broadIndicators = ['trend', 'development', 'overview', 'introduction', 'guide'];
        return broadIndicators.some(indicator => 
            topic.toLowerCase().includes(indicator)
        ) || topic.split(' ').length <= 3;
    }

    isSpecificQuery(topic) {
        const specificIndicators = ['how to', 'tutorial', 'step by step', 'guide for'];
        return specificIndicators.some(indicator => 
            topic.toLowerCase().includes(indicator)
        ) || topic.split(' ').length >= 5;
    }

    involvesComparison(topic) {
        const comparisonIndicators = ['vs', 'versus', 'compare', 'comparison', 'difference between'];
        return comparisonIndicators.some(indicator => 
            topic.toLowerCase().includes(indicator)
        );
    }

    isVerificationNeeded(topic) {
        const verificationIndicators = ['true or false', 'myth', 'fact check', 'verify', 'is it true'];
        return verificationIndicators.some(indicator => 
            topic.toLowerCase().includes(indicator)
        );
    }

    // 🧹 清理结果数据（避免循环引用）
    sanitizeResult(result) {
        if (typeof result !== 'object' || result === null) {
            return result;
        }
        
        try {
            // 简单克隆，移除函数和循环引用
            return JSON.parse(JSON.stringify(result, (key, value) => {
                if (typeof value === 'function') {
                    return undefined; // 移除函数
                }
                return value;
            }));
        } catch (error) {
            // 如果JSON序列化失败，返回简化版本
            return { 
                type: typeof result,
                simplified: true,
                message: 'Result contains circular references'
            };
        }
    }

    // 🆔 生成唯一ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // 📋 获取研究历史
    getResearchHistory(limit = 10, strategyFilter = null) {
        let history = this.researchHistory;
        
        if (strategyFilter) {
            history = history.filter(record => record.strategy === strategyFilter);
        }
        
        return history.slice(-limit).reverse();
    }

    // 📊 获取性能报告
    getPerformanceReport() {
        return {
            timestamp: new Date().toISOString(),
            totalResearchCount: this.researchHistory.length,
            strategyPerformance: this.performanceMetrics,
            overallSuccessRate: this.calculateOverallSuccessRate(),
            recommendations: this.generatePerformanceRecommendations()
        };
    }

    calculateOverallSuccessRate() {
        const total = Object.values(this.performanceMetrics)
            .reduce((sum, metrics) => sum + metrics.totalExecutions, 0);
        
        const successful = Object.values(this.performanceMetrics)
            .reduce((sum, metrics) => sum + metrics.successfulExecutions, 0);
        
        return total > 0 ? successful / total : 0;
    }

    generatePerformanceRecommendations() {
        const recommendations = [];
        
        Object.entries(this.performanceMetrics).forEach(([strategy, metrics]) => {
            if (metrics.successRate < 0.7 && metrics.totalExecutions > 5) {
                recommendations.push({
                    strategy,
                    issue: `成功率较低 (${(metrics.successRate * 100).toFixed(1)}%)`,
                    suggestion: '考虑优化参数配置或增加重试机制'
                });
            }
            
            if (metrics.avgTime > 60000 && metrics.totalExecutions > 3) {
                recommendations.push({
                    strategy,
                    issue: `执行时间较长 (${(metrics.avgTime / 1000).toFixed(1)}秒)`,
                    suggestion: '考虑优化网络请求或减少研究深度'
                });
            }
        });
        
        return recommendations;
    }

    // 🧪 策略参数验证
    validateStrategyParameters(strategyType, parameters) {
        const strategy = this.strategies[strategyType];
        if (!strategy) {
            return { valid: false, error: `未知策略: ${strategyType}` };
        }
        
        const validation = { valid: true, warnings: [] };
        
        // 检查必需参数
        if (strategyType === 'TARGETED' && (!parameters.url || !parameters.extractionSelectors)) {
            validation.valid = false;
            validation.error = '目标研究需要URL和提取选择器';
        }
        
        if (strategyType === 'COMPARATIVE' && (!parameters.urls || parameters.urls.length < 2)) {
            validation.warnings.push('比较分析需要至少2个URL');
        }
        
        if (strategyType === 'VERIFICATION' && (!parameters.claim || !parameters.sources)) {
            validation.valid = false;
            validation.error = '验证研究需要主张和来源列表';
        }
        
        return validation;
    }
}

// 📋 使用示例
async function strategyDemo() {
    const strategyManager = new ResearchStrategyManager();
    
    // 推荐策略
    const recommendations = strategyManager.recommendStrategy('人工智能发展趋势');
    console.log('策略推荐:', recommendations);
    
    // 获取性能报告
    const report = strategyManager.getPerformanceReport();
    console.log('性能报告:', report);
    
    return strategyManager;
}

// 导出模块
module.exports = ResearchStrategyManager;