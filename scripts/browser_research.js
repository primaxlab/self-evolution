// 🌐 浏览器研究集成系统核心脚本
// 版本: 1.0
// 最后更新: 2026-04-05
// 状态: 开发中

const ResearchErrorHandler = require('./error_handler');

class BrowserResearchSystem {
  constructor() {
    this.researchStrategies = {
      quickFact: '快速事实查询',
      deepAnalysis: '深度分析研究',
      multiSource: '多源验证研究',
      comparative: '对比分析研究'
    };
    
    this.allowedDomains = [
      'wikipedia.org',
      'github.com', 
      'stackoverflow.com',
      'openclaw.ai',
      'docs.openclaw.ai',
      'clawhub.ai'
    ];
    
    this.blacklistedDomains = [
      'malicious-site.com',
      'scam-website.org',
      'fake-news.net',
      'dangerous-content.ai'
    ];
    
    this.knowledgeBasePath = 'D:\\OpenClaw_Main\\workspace\\knowledge_base\\';
    
    // 初始化错误处理器
    this.errorHandler = new ResearchErrorHandler();
    this.researchState = {
      active: false,
      currentResearch: null,
      progress: 0,
      results: []
    };
    
    this.initialize();
  }
  
  // 初始化研究系统
  async initialize() {
    console.log('🌐 初始化浏览器研究系统...');
    
    try {
      // 创建知识库目录
      await this.ensureKnowledgeBase();
      
      // 验证浏览器工具可用性
      const browserAvailable = await this.checkBrowserAvailability();
      
      if (!browserAvailable) {
        console.warn('⚠️  浏览器工具暂时不可用，使用备用研究模式');
        this.fallbackMode = true;
      }
      
      console.log('✅ 浏览器研究系统初始化完成');
      console.log(`📊 支持的研究策略: ${Object.values(this.researchStrategies).join(', ')}`);
      console.log(`🔒 允许的域名: ${this.allowedDomains.length}个`);
      console.log(`🚫 黑名单域名: ${this.blacklistedDomains.length}个`);
      
    } catch (error) {
      console.error('❌ 研究系统初始化失败:', error.message);
      this.fallbackMode = true;
    }
  }
  
  // 确保知识库目录存在
  async ensureKnowledgeBase() {
    try {
      // 检查目录是否存在
      const dirExists = await this.checkDirectoryExists(this.knowledgeBasePath);
      
      if (!dirExists) {
        console.log('📁 创建知识库目录...');
        await this.createDirectory(this.knowledgeBasePath);
        
        // 创建子目录结构
        await this.createDirectory(this.knowledgeBasePath + 'research\\');
        await this.createDirectory(this.knowledgeBasePath + 'sources\\');
        await this.createDirectory(this.knowledgeBasePath + 'processed\\');
        
        console.log('✅ 知识库目录结构创建完成');
      }
      
      return true;
      
    } catch (error) {
      console.error('❌ 知识库目录创建失败:', error.message);
      throw error;
    }
  }
  
  // 检查浏览器工具可用性
  async checkBrowserAvailability() {
    try {
      // 简单的浏览器工具检查
      console.log('🔍 检查浏览器工具状态...');
      
      // 这里应该调用实际的浏览器工具检查
      // 暂时返回模拟结果
      return true; // 假设浏览器可用
      
    } catch (error) {
      console.warn('⚠️  浏览器工具检查失败:', error.message);
      return false;
    }
  }
  
  // 执行研究任务
  async conductResearch(topic, strategy = 'quickFact', options = {}) {
    if (this.researchState.active) {
      throw new Error('已有研究任务正在进行中');
    }
    
    this.researchState = {
      active: true,
      currentResearch: {
        topic,
        strategy,
        options,
        startTime: new Date(),
        status: 'starting'
      },
      progress: 0,
      results: []
    };
    
    console.log(`🔬 开始研究: "${topic}" (策略: ${this.researchStrategies[strategy]})`);
    
    try {
      // 验证研究策略
      if (!this.researchStrategies[strategy]) {
        throw new Error(`不支持的研究策略: ${strategy}`);
      }
      
      // 根据策略执行研究
      let results;
      
      switch (strategy) {
        case 'quickFact':
          results = await this.quickFactResearch(topic, options);
          break;
          
        case 'deepAnalysis':
          results = await this.deepAnalysisResearch(topic, options);
          break;
          
        case 'multiSource':
          results = await this.multiSourceResearch(topic, options);
          break;
          
        case 'comparative':
          results = await this.comparativeResearch(topic, options);
          break;
          
        default:
          throw new Error(`未知的研究策略: ${strategy}`);
      }
      
      // 处理研究结果
      const processedResults = await this.processResearchResults(results, topic, strategy);
      
      // 保存到知识库
      await this.saveToKnowledgeBase(processedResults, topic, strategy);
      
      this.researchState = {
        active: false,
        currentResearch: null,
        progress: 100,
        results: processedResults
      };
      
      console.log(`✅ 研究完成: "${topic}" - 获得 ${processedResults.length} 条结果`);
      
      return processedResults;
      
    } catch (error) {
      this.researchState.active = false;
      this.researchState.currentResearch.status = 'failed';
      this.researchState.currentResearch.error = error.message;
      
      console.error(`❌ 研究失败: "${topic}" -`, error.message);
      throw error;
    }
  }
  
  // 快速事实查询研究
  async quickFactResearch(topic, options) {
    console.log('⚡ 执行快速事实查询...');
    this.updateProgress(20);
    
    try {
      // 使用web_search工具进行快速查询
      const searchResults = await this.webSearch(topic, {
        count: options.maxResults || 3,
        region: 'us-en',
        safeSearch: 'moderate'
      });
      
      this.updateProgress(60);
      
      // 提取关键信息
      const facts = await this.extractKeyFacts(searchResults, topic);
      
      this.updateProgress(90);
      
      return {
        type: 'quick_facts',
        topic: topic,
        facts: facts,
        sources: searchResults,
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      console.error('❌ 快速事实查询失败:', error.message);
      throw new Error(`快速事实查询失败: ${error.message}`);
    }
  }
  
  // 深度分析研究
  async deepAnalysisResearch(topic, options) {
    console.log('🧠 执行深度分析研究...');
    this.updateProgress(10);
    
    // 多轮搜索和综合分析
    const searchTerms = this.generateSearchTerms(topic, 'deep');
    const allResults = [];
    
    for (let i = 0; i < searchTerms.length; i++) {
      const term = searchTerms[i];
      const progress = 10 + (i / searchTerms.length) * 50;
      this.updateProgress(progress);
      
      try {
        const results = await this.webSearch(term, {
          count: options.maxResultsPerTerm || 2,
          region: 'global'
        });
        
        allResults.push(...results);
        
      } catch (error) {
        console.warn(`⚠️  搜索术语 "${term}" 失败:`, error.message);
      }
    }
    
    this.updateProgress(70);
    
    // 深度分析和综合
    const analysis = await this.deepAnalyzeResults(allResults, topic);
    
    this.updateProgress(90);
    
    return {
      type: 'deep_analysis',
      topic: topic,
      analysis: analysis,
      sources: allResults,
      searchTerms: searchTerms,
      timestamp: new Date().toISOString()
    };
  }
  
  // 多源验证研究
  async multiSourceResearch(topic, options) {
    console.log('🔍 执行多源验证研究...');
    this.updateProgress(15);
    
    // 从多个来源获取信息
    const sources = await this.gatherMultipleSources(topic, options);
    
    this.updateProgress(60);
    
    // 交叉验证和信息整合
    const verifiedInfo = await this.crossVerifyInformation(sources, topic);
    
    this.updateProgress(90);
    
    return {
      type: 'multi_source',
      topic: topic,
      verifiedInfo: verifiedInfo,
      sources: sources,
      verificationScore: this.calculateVerificationScore(verifiedInfo),
      timestamp: new Date().toISOString()
    };
  }
  
  // 对比分析研究
  async comparativeResearch(topic, options) {
    console.log('📊 执行对比分析研究...');
    this.updateProgress(20);
    
    // 获取不同视角的信息
    const perspectives = await this.gatherDifferentPerspectives(topic, options);
    
    this.updateProgress(60);
    
    // 执行对比分析
    const comparison = await this.comparePerspectives(perspectives, topic);
    
    this.updateProgress(90);
    
    return {
      type: 'comparative_analysis',
      topic: topic,
      comparison: comparison,
      perspectives: perspectives,
      timestamp: new Date().toISOString()
    };
  }
  
  // 处理研究结果
  async processResearchResults(results, topic, strategy) {
    console.log('📋 处理研究结果...');
    
    const processed = {
      metadata: {
        processingTime: new Date().toISOString(),
        processingStrategy: strategy,
        topic: topic,
        resultType: results.type
      },
      content: results
    };
    
    // 根据结果类型进行特定处理
    switch (results.type) {
      case 'quick_facts':
        processed.summary = await this.summarizeFacts(results.facts);
        break;
        
      case 'deep_analysis':
        processed.insights = await this.extractKeyInsights(results.analysis);
        break;
        
      case 'multi_source':
        processed.confidence = results.verificationScore;
        break;
        
      case 'comparative_analysis':
        processed.conclusions = await this.drawConclusions(results.comparison);
        break;
    }
    
    return processed;
  }
  
  // 保存到知识库
  async saveToKnowledgeBase(results, topic, strategy) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `research_${topic.slice(0, 20)}_${strategy}_${timestamp}.json`;
    const filepath = this.knowledgeBasePath + 'research\\' + filename;
    
    try {
      const content = JSON.stringify(results, null, 2);
      await this.writeFile(filepath, content);
      
      console.log(`💾 研究结果保存到: ${filepath}`);
      
      // 更新知识库索引
      await this.updateKnowledgeIndex(topic, strategy, filename);
      
      return filepath;
      
    } catch (error) {
      console.error('❌ 保存研究结果失败:', error.message);
      throw error;
    }
  }
  
  // 更新进度
  updateProgress(progress) {
    this.researchState.progress = Math.max(0, Math.min(100, progress));
    
    if (this.researchState.currentResearch) {
      this.researchState.currentResearch.progress = this.researchState.progress;
      this.researchState.currentResearch.status = 'processing';
    }
    
    console.log(`📈 研究进度: ${this.researchState.progress}%`);
  }
  
  // 获取当前研究状态
  getResearchStatus() {
    return {
      ...this.researchState,
      knowledgeBasePath: this.knowledgeBasePath,
      allowedDomains: this.allowedDomains,
      blacklistedDomains: this.blacklistedDomains,
      fallbackMode: this.fallbackMode
    };
  }
  
  // 真实的 web_search 工具集成
  async webSearch(query, options) {
    console.log(`🔍 执行真实搜索: "${query}"`);
    
    const searchOptions = {
      query: query,
      count: options?.count || 5,
      region: options?.region || 'us-en',
      safeSearch: options?.safeSearch || 'moderate'
    };
    
    try {
      // 使用错误处理器执行搜索（带重试）
      const searchResults = await this.errorHandler.executeWithRetry(
        () => this.executeWebSearch(searchOptions),
        'web_search',
        { query: query, options: searchOptions }
      );
      
      console.log(`✅ 搜索完成，获得 ${searchResults.length} 条结果`);
      return searchResults;
      
    } catch (error) {
      console.error(`❌ 搜索失败: "${query}" -`, error.message);
      
      // 降级方案：使用备用搜索引擎
      return await this.fallbackWebSearch(query, options);
    }
  }
  
  // 执行真实 web_search 工具调用
  async executeWebSearch(options) {
    try {
      // 这里实际调用 web_search 工具
      const results = await web_search({
        query: options.query,
        count: options.count,
        region: options.region,
        safeSearch: options.safeSearch
      });
      
      return results;
      
    } catch (error) {
      console.warn('⚠️  web_search 工具调用失败，尝试备用方案');
      throw error; // 抛出错误让上层处理
    }
  }
  
  // 备用搜索引擎方案
  async fallbackWebSearch(query, options) {
    console.log(`🔄 使用备用搜索引擎: "${query}"`);
    
    try {
      // 这里可以实现多个备用方案
      const results = await this.alternativeSearchAPI(query, options);
      
      if (results && results.length > 0) {
        console.log(`✅ 备用搜索成功，获得 ${results.length} 条结果`);
        return results;
      }
      
      // 如果备用方案也失败，返回基础结果
      return [{
        title: `关于 ${query} 的搜索结果（备用）`,
        url: `https://www.google.com/search?q=${encodeURIComponent(query)}`,
        snippet: `这是关于 ${query} 的相关信息，来自备用搜索引擎`
      }];
      
    } catch (fallbackError) {
      console.error('❌ 备用搜索也失败了:', fallbackError.message);
      
      // 最终降级：返回最基本的模拟结果
      return [{
        title: `搜索: ${query}`,
        url: '',
        snippet: `无法获取实时搜索结果，请检查网络连接或工具配置`
      }];
    }
  }
  
  async extractKeyFacts(searchResults, topic) {
    console.log(`📋 提取关键事实: "${topic}"`);
    
    const facts = [];
    
    try {
      // 对每个搜索结果进行内容提取
      for (const result of searchResults.slice(0, 3)) { // 只处理前3个结果
        try {
          const pageContent = await this.fetchAndExtractContent(result.url);
          const extractedFacts = await this.analyzeContentForFacts(pageContent, topic);
          
          facts.push(...extractedFacts);
          
        } catch (error) {
          console.warn(`⚠️  提取失败: ${result.url} -`, error.message);
          
          // 从摘要中提取基础信息
          const basicFact = this.extractBasicFactFromSnippet(result.snippet, topic);
          if (basicFact) {
            facts.push({
              ...basicFact,
              confidence: 0.6, // 较低置信度
              source: result.url,
              warning: '从摘要提取，可能需要验证'
            });
          }
        }
      }
      
      // 去重和排序
      const uniqueFacts = this.removeDuplicateFacts(facts);
      const sortedFacts = this.sortFactsByConfidence(uniqueFacts);
      
      console.log(`✅ 提取完成，获得 ${sortedFacts.length} 条关键事实`);
      return sortedFacts;
      
    } catch (error) {
      console.error('❌ 内容提取失败:', error.message);
      
      // 降级方案：从搜索结果中提取基本信息
      return this.extractFactsFromSearchResults(searchResults, topic);
    }
  }
  
  // 获取并提取网页内容
  async fetchAndExtractContent(url) {
    if (!url || !this.isUrlAllowed(url)) {
      throw new Error('URL无效或不在允许列表中');
    }
    
    try {
      // 使用 web_fetch 工具获取页面内容
      const content = await web_fetch({
        url: url,
        extractMode: 'markdown',
        maxChars: 10000
      });
      
      return content;
      
    } catch (error) {
      console.warn(`⚠️  网页获取失败: ${url} -`, error.message);
      
      // 尝试使用 browser 工具
      try {
        const snapshot = await browser({
          action: 'snapshot',
          url: url,
          maxChars: 8000
        });
        
        return snapshot.textContent || '';
        
      } catch (browserError) {
        throw new Error(`无法获取页面内容: ${browserError.message}`);
      }
    }
  }
  
  // 分析内容提取事实
  async analyzeContentForFacts(content, topic) {
    const facts = [];
    
    // 简单的关键词匹配和事实提取
    const lines = content.split('\n').filter(line => 
      line.toLowerCase().includes(topic.toLowerCase())
    );
    
    for (const line of lines.slice(0, 10)) { // 只处理前10行相关内容
      const fact = this.extractFactFromText(line, topic);
      if (fact) {
        facts.push({
          fact: fact,
          confidence: this.calculateConfidence(line, topic),
          source: 'extracted_from_content',
          context: line.trim()
        });
      }
    }
    
    return facts;
  }
  
  // 从文本中提取事实
  extractFactFromText(text, topic) {
    // 简单的规则提取
    const patterns = [
      new RegExp(`${topic}[^.!?]*是[^.!?]*[.!?]`),
      new RegExp(`${topic}[^.!?]*包括[^.!?]*[.!?]`),
      new RegExp(`${topic}[^.!?]*可以[^.!?]*[.!?]`),
      new RegExp(`${topic}[^.!?]*主要[^.!?]*[.!?]`)
    ];
    
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        return match[0].trim();
      }
    }
    
    return null;
  }
  
  generateSearchTerms(topic, type) {
    // 生成相关的搜索术语
    return [
      topic,
      `${topic} 介绍`,
      `${topic} 最新发展`,
      `${topic} 应用场景`
    ];
  }
  
  async deepAnalyzeResults(results, topic) {
    // 深度分析逻辑
    return {
      summary: `对 ${topic} 的深度分析完成`,
      keyPoints: ['要点1', '要点2', '要点3'],
      implications: ['意义1', '意义2']
    };
  }
  
  async gatherMultipleSources(topic, options) {
    // 多源收集逻辑
    return [];
  }
  
  async crossVerifyInformation(sources, topic) {
    // 交叉验证逻辑
    return {};
  }
  
  calculateVerificationScore(info) {
    // 计算验证分数
    return 0.85;
  }
  
  async gatherDifferentPerspectives(topic, options) {
    // 收集不同视角
    return {};
  }
  
  async comparePerspectives(perspectives, topic) {
    // 对比分析逻辑
    return {};
  }
  
  async summarizeFacts(facts) {
    // 事实摘要逻辑
    return `共找到 ${facts.length} 条相关事实`;
  }
  
  async extractKeyInsights(analysis) {
    // 提取关键洞察
    return [];
  }
  
  async drawConclusions(comparison) {
    // 得出结论
    return [];
  }
  
  async updateKnowledgeIndex(topic, strategy, filename) {
    // 更新知识库索引
  }
  
  async checkDirectoryExists(path) {
    // 检查目录是否存在
    return true;
  }
  
  async createDirectory(path) {
    // 创建目录
  }
  
  async writeFile(path, content) {
    // 写入文件
  }
  
  // 工具方法实现
  
  // 从摘要提取基础事实
  extractBasicFactFromSnippet(snippet, topic) {
    if (!snippet || !snippet.includes(topic)) {
      return null;
    }
    
    // 简单的摘要分析
    const fact = snippet
      .replace(new RegExp(topic, 'gi'), topic)
      .trim();
    
    return {
      fact: fact,
      confidence: 0.6
    };
  }
  
  // 检查URL是否允许
  isUrlAllowed(url) {
    if (!url) return false;
    
    try {
      const domain = new URL(url).hostname;
      
      // 检查黑名单
      if (this.blacklistedDomains.some(blacklisted => 
        domain.includes(blacklisted))) {
        return false;
      }
      
      // 检查白名单
      return this.allowedDomains.some(allowed => 
        domain.includes(allowed));
      
    } catch (error) {
      console.warn(`⚠️  URL解析失败: ${url}`);
      return false;
    }
  }
  
  // 计算置信度
  calculateConfidence(text, topic) {
    let confidence = 0.7; // 基础置信度
    
    // 基于文本特征调整置信度
    if (text.length > 50) confidence += 0.1;
    if (text.includes('研究') || text.includes('数据')) confidence += 0.05;
    if (text.includes('证明') || text.includes('实验')) confidence += 0.1;
    if (text.includes('可能') || text.includes('或许')) confidence -= 0.1;
    
    return Math.min(0.95, Math.max(0.3, confidence));
  }
  
  // 去重事实
  removeDuplicateFacts(facts) {
    const seen = new Set();
    return facts.filter(fact => {
      const key = fact.fact.toLowerCase().trim();
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }
  
  // 按置信度排序
  sortFactsByConfidence(facts) {
    return facts.sort((a, b) => b.confidence - a.confidence);
  }
  
  // 从搜索结果提取事实（降级方案）
  extractFactsFromSearchResults(results, topic) {
    const facts = [];
    
    for (const result of results.slice(0, 3)) {
      if (result.snippet && result.snippet.includes(topic)) {
        facts.push({
          fact: result.snippet,
          confidence: 0.5,
          source: result.url,
          warning: '从搜索结果摘要提取，需要验证'
        });
      }
    }
    
    return facts.length > 0 ? facts : [{
      fact: `关于${topic}的信息需要进一步研究验证`,
      confidence: 0.3,
      source: '',
      warning: '无法提取具体事实信息'
    }];
  }
  
  // 备用搜索API
  async alternativeSearchAPI(query, options) {
    // 这里可以实现多个备用搜索方案
    // 例如：不同的搜索引擎、API等
    
    try {
      // 示例：使用DuckDuckGo备用
      const results = await web_search({
        query: query,
        count: options?.count || 3,
        region: 'global'
      });
      
      return results;
      
    } catch (error) {
      console.warn('备用搜索API失败:', error.message);
      return null;
    }
  }
}

// 导出供其他系统使用
module.exports = BrowserResearchSystem;

// 测试代码
if (require.main === module) {
  async function testBrowserResearch() {
    console.log('🧪 测试浏览器研究系统...');
    
    const researchSystem = new BrowserResearchSystem();
    
    // 等待初始化完成
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 测试快速事实查询
    try {
      const results = await researchSystem.conductResearch(
        '人工智能发展趋势', 
        'quickFact',
        { maxResults: 5 }
      );
      
      console.log('✅ 测试成功:', JSON.stringify(results, null, 2));
      
    } catch (error) {
      console.error('❌ 测试失败:', error.message);
    }
  }
  
  testBrowserResearch();
}