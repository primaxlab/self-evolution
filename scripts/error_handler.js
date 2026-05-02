// 🔧 错误处理和重试系统
// 版本: 1.0
// 最后更新: 2026-04-05

class ResearchErrorHandler {
  constructor() {
    this.maxRetries = 3;
    this.retryDelays = [1000, 3000, 5000]; // 1s, 3s, 5s
    this.errorStats = new Map();
    this.circuitBreakers = new Map();
  }
  
  // 执行带重试的操作
  async executeWithRetry(operation, operationName, context = {}) {
    let lastError;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      // 检查熔断器
      if (this.isCircuitBreakerOpen(operationName)) {
        throw new Error(`服务暂时不可用: ${operationName} (熔断器开启)`);
      }
      
      try {
        const result = await operation();
        
        // 成功时重置错误统计
        this.recordSuccess(operationName);
        return result;
        
      } catch (error) {
        lastError = error;
        
        // 记录错误
        this.recordError(operationName, error, context);
        
        // 如果是最后一次尝试，直接抛出错误
        if (attempt === this.maxRetries) {
          break;
        }
        
        // 计算延迟时间
        const delay = this.calculateRetryDelay(attempt, operationName);
        console.log(`🔄 重试 ${attempt}/${this.maxRetries}: ${operationName} (${delay}ms后)`);
        
        // 等待重试
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
    
    // 所有重试都失败
    throw this.wrapError(lastError, operationName, context);
  }
  
  // 计算重试延迟
  calculateRetryDelay(attempt, operationName) {
    const baseDelay = this.retryDelays[attempt - 1] || 5000;
    
    // 根据错误率调整延迟
    const errorRate = this.getErrorRate(operationName);
    if (errorRate > 0.5) {
      return baseDelay * 2; // 错误率高时加倍延迟
    }
    
    return baseDelay;
  }
  
  // 记录错误
  recordError(operationName, error, context) {
    const now = Date.now();
    const errorKey = `${operationName}_${error.name}`;
    
    if (!this.errorStats.has(errorKey)) {
      this.errorStats.set(errorKey, {
        count: 0,
        lastError: null,
        firstOccurrence: now,
        lastOccurrence: now
      });
    }
    
    const stats = this.errorStats.get(errorKey);
    stats.count++;
    stats.lastError = error;
    stats.lastOccurrence = now;
    
    console.error(`❌ 错误记录: ${operationName} - ${error.message}`);
    
    // 检查是否需要触发熔断器
    this.checkCircuitBreaker(operationName, stats);
  }
  
  // 记录成功
  recordSuccess(operationName) {
    // 重置错误统计
    const errorKeys = Array.from(this.errorStats.keys())
      .filter(key => key.startsWith(operationName));
    
    errorKeys.forEach(key => {
      this.errorStats.delete(key);
    });
    
    // 关闭熔断器（如果存在）
    if (this.circuitBreakers.has(operationName)) {
      const breaker = this.circuitBreakers.get(operationName);
      if (breaker.open && Date.now() - breaker.openedAt > breaker.resetTimeout) {
        this.circuitBreakers.delete(operationName);
        console.log(`✅ 熔断器关闭: ${operationName}`);
      }
    }
  }
  
  // 检查熔断器
  checkCircuitBreaker(operationName, stats) {
    // 如果在短时间内错误太多，触发熔断器
    const timeWindow = 5 * 60 * 1000; // 5分钟
    const errorThreshold = 10; // 10次错误
    
    if (stats.count >= errorThreshold && 
        Date.now() - stats.firstOccurrence < timeWindow) {
      this.openCircuitBreaker(operationName);
    }
  }
  
  // 开启熔断器
  openCircuitBreaker(operationName) {
    if (!this.circuitBreakers.has(operationName)) {
      this.circuitBreakers.set(operationName, {
        open: true,
        openedAt: Date.now(),
        resetTimeout: 5 * 60 * 1000 // 5分钟
      });
      
      console.warn(`⚡ 熔断器开启: ${operationName} - 服务暂时不可用`);
    }
  }
  
  // 检查熔断器是否开启
  isCircuitBreakerOpen(operationName) {
    const breaker = this.circuitBreakers.get(operationName);
    if (!breaker || !breaker.open) {
      return false;
    }
    
    // 检查是否超过重置时间
    if (Date.now() - breaker.openedAt > breaker.resetTimeout) {
      this.circuitBreakers.delete(operationName);
      return false;
    }
    
    return true;
  }
  
  // 获取错误率
  getErrorRate(operationName) {
    const totalErrors = Array.from(this.errorStats.keys())
      .filter(key => key.startsWith(operationName))
      .reduce((sum, key) => sum + this.errorStats.get(key).count, 0);
    
    // 简单估算错误率（需要更复杂的实现）
    return Math.min(1, totalErrors / 20);
  }
  
  // 包装错误信息
  wrapError(error, operationName, context) {
    const wrappedError = new Error(
      `${operationName} 失败: ${error.message} (重试 ${this.maxRetries} 次后)`
    );
    
    wrappedError.name = 'ResearchError';
    wrappedError.originalError = error;
    wrappedError.operation = operationName;
    wrappedError.context = context;
    wrappedError.timestamp = new Date().toISOString();
    wrappedError.retryCount = this.maxRetries;
    
    return wrappedError;
  }
  
  // 获取错误统计
  getErrorStatistics() {
    return {
      totalErrors: this.errorStats.size,
      errorDetails: Object.fromEntries(this.errorStats),
      circuitBreakers: Object.fromEntries(this.circuitBreakers),
      timestamp: new Date().toISOString()
    };
  }
  
  // 清除错误统计
  clearErrorStats() {
    this.errorStats.clear();
    this.circuitBreakers.clear();
    console.log('✅ 错误统计已清除');
  }
}

// 导出供其他系统使用
module.exports = ResearchErrorHandler;

// 测试代码
if (require.main === module) {
  async function testErrorHandler() {
    const errorHandler = new ResearchErrorHandler();
    
    // 模拟失败的操作
    let attempt = 0;
    const failingOperation = async () => {
      attempt++;
      if (attempt < 3) {
        throw new Error(`模拟失败 (尝试 ${attempt})`);
      }
      return '最终成功';
    };
    
    try {
      const result = await errorHandler.executeWithRetry(
        failingOperation,
        '测试操作',
        { test: true }
      );
      
      console.log('✅ 测试成功:', result);
      
    } catch (error) {
      console.error('❌ 测试失败:', error.message);
    }
    
    console.log('📊 错误统计:', errorHandler.getErrorStatistics());
  }
  
  testErrorHandler();
}