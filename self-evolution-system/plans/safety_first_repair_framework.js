// 安全优先修复框架 v1.0
// 基于老板"安全第一、渐进修复、学习修复"三原则

const fs = require('fs');
const path = require('path');

class SafetyFirstRepairFramework {
  constructor() {
    this.workspacePath = path.join(__dirname, '.');
    this.backupDir = path.join(this.workspacePath, 'repair_backups');
    this.knowledgeBasePath = path.join(this.workspacePath, 'repair_knowledge.json');
    
    // 确保目录存在
    this.ensureDirectories();
    
    // 加载修复知识库
    this.knowledgeBase = this.loadKnowledgeBase();
  }

  ensureDirectories() {
    const dirs = [this.backupDir];
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  loadKnowledgeBase() {
    try {
      if (fs.existsSync(this.knowledgeBasePath)) {
        return JSON.parse(fs.readFileSync(this.knowledgeBasePath, 'utf8'));
      }
    } catch (error) {
      console.warn('修复知识库加载失败，使用默认:', error.message);
    }
    
    return {
      version: '1.0.0',
      successfulRepairs: [],
      failedRepairs: [],
      learnedPatterns: [],
      repairStrategies: {
        'exec_tool_failure': {
          description: 'exec工具调用失败修复',
          steps: ['检查命令语法', '验证权限', '测试简单命令', '逐步复杂化'],
          successRate: 0.85,
          lastUsed: null
        },
        'session_congestion': {
          description: '会话卡顿修复',
          steps: ['检查上下文使用率', '智能清理会话', '重启会话', '验证响应速度'],
          successRate: 0.95,
          lastUsed: '2026-03-17T05:52:00Z'
        }
      }
    };
  }

  async safeRepair(problem, causeAnalysis) {
    console.log(`🛠️ 开始安全修复: ${problem.type}`);
    
    const repairId = `repair_${Date.now()}_${problem.type.replace(/\s+/g, '_')}`;
    const repairLog = {
      id: repairId,
      timestamp: new Date().toISOString(),
      problem: problem,
      causeAnalysis: causeAnalysis,
      phases: [],
      status: 'initiated'
    };

    try {
      // 原则1：安全第一 - 修复前备份
      console.log('💾 原则1: 安全第一 - 创建备份');
      const backup = await this.createBackup(repairId, problem);
      repairLog.backup = backup;
      repairLog.phases.push({ name: 'backup_created', status: 'completed', timestamp: new Date().toISOString() });

      // 验证修复安全性
      const safetyValidation = await this.validateRepairSafety(problem, causeAnalysis);
      if (!safetyValidation.safe) {
        repairLog.status = 'aborted';
        repairLog.abortReason = 'safety_validation_failed';
        repairLog.safetyValidation = safetyValidation;
        await this.recordRepairResult(repairLog);
        
        console.log('❌ 修复中止: 安全验证失败');
        return {
          status: 'aborted',
          reason: 'safety_validation_failed',
          validation: safetyValidation
        };
      }
      repairLog.safetyValidation = safetyValidation;
      repairLog.phases.push({ name: 'safety_validated', status: 'passed', timestamp: new Date().toISOString() });

      // 原则2：渐进修复 - 创建渐进计划
      console.log('🔄 原则2: 渐进修复 - 创建修复计划');
      const repairPlan = await this.createProgressiveRepairPlan(problem, causeAnalysis, safetyValidation);
      repairLog.repairPlan = repairPlan;

      // 分阶段执行修复
      let allPhasesSuccessful = true;
      
      for (let i = 0; i < repairPlan.phases.length; i++) {
        const phase = repairPlan.phases[i];
        console.log(`📝 执行阶段 ${i + 1}/${repairPlan.phases.length}: ${phase.name}`);
        
        const phaseStartTime = new Date().toISOString();
        
        try {
          // 执行阶段
          const phaseResult = await this.executeRepairPhase(phase, problem, i);
          repairLog.phases.push({
            name: phase.name,
            status: 'completed',
            startTime: phaseStartTime,
            endTime: new Date().toISOString(),
            result: phaseResult
          });

          // 阶段验证
          const phaseValidation = await this.validateRepairPhase(phaseResult, phase);
          repairLog.phases[repairLog.phases.length - 1].validation = phaseValidation;

          if (!phaseValidation.success) {
            console.log(`⚠️ 阶段验证失败: ${phaseValidation.reason}`);
            
            // 评估是否需要回滚
            if (this.shouldRollback(phaseValidation, i, repairPlan.phases.length)) {
              console.log('🔄 触发自动回滚');
              const rollbackResult = await this.rollbackToBackup(backup, repairLog);
              repairLog.rollback = rollbackResult;
              repairLog.status = 'rolled_back';
              
              await this.recordRepairResult(repairLog);
              
              return {
                status: 'rolled_back',
                phase: phase.name,
                rollback: rollbackResult,
                repairLogId: repairId
              };
            } else {
              // 继续下一阶段（风险可控）
              console.log('⏭️ 风险可控，继续下一阶段');
            }
          }

        } catch (phaseError) {
          console.error(`❌ 阶段执行失败: ${phaseError.message}`);
          repairLog.phases.push({
            name: phase.name,
            status: 'failed',
            startTime: phaseStartTime,
            endTime: new Date().toISOString(),
            error: phaseError.message
          });
          
          allPhasesSuccessful = false;
          
          // 立即回滚
          const rollbackResult = await this.rollbackToBackup(backup, repairLog);
          repairLog.rollback = rollbackResult;
          repairLog.status = 'rolled_back_due_to_error';
          
          await this.recordRepairResult(repairLog);
          
          return {
            status: 'rolled_back',
            reason: 'phase_execution_error',
            phase: phase.name,
            error: phaseError.message,
            rollback: rollbackResult,
            repairLogId: repairId
          };
        }
      }

      // 所有阶段完成后的最终验证
      console.log('🔍 最终修复验证');
      const finalValidation = await this.validateFinalRepair(repairLog);
      repairLog.finalValidation = finalValidation;

      if (finalValidation.success) {
        // 原则3：学习修复 - 记录成功经验
        console.log('📚 原则3: 学习修复 - 记录成功经验');
        await this.recordSuccessfulRepair(repairLog, finalValidation);
        
        repairLog.status = 'success';
        await this.recordRepairResult(repairLog);
        
        console.log('✅ 修复成功完成');
        return {
          status: 'success',
          repairId: repairId,
          phases: repairLog.phases.length,
          finalValidation: finalValidation,
          backupKept: backup.location
        };
      } else {
        // 最终验证失败，回滚
        console.log('❌ 最终验证失败，触发回滚');
        const rollbackResult = await this.rollbackToBackup(backup, repairLog);
        repairLog.rollback = rollbackResult;
        repairLog.status = 'rolled_back_final_validation_failed';
        
        await this.recordRepairResult(repairLog);
        
        return {
          status: 'rolled_back',
          reason: 'final_validation_failed',
          validation: finalValidation,
          rollback: rollbackResult,
          repairLogId: repairId
        };
      }

    } catch (error) {
      console.error('❌ 修复过程意外失败:', error);
      repairLog.status = 'unexpected_failure';
      repairLog.error = error.message;
      await this.recordRepairResult(repairLog);
      
      return {
        status: 'failed',
        error: error.message,
        repairLogId: repairId
      };
    }
  }

  async createBackup(repairId, problem) {
    const backupId = `backup_${repairId}`;
    const backupPath = path.join(this.backupDir, `${backupId}.json`);
    
    const backupData = {
      id: backupId,
      timestamp: new Date().toISOString(),
      repairId: repairId,
      problem: problem,
      systemState: {
        // 这里应该包含实际的系统状态快照
        configFiles: this.getConfigFileList(),
        currentSettings: this.getCurrentSettings(),
        runtimeState: this.getRuntimeState()
      },
      metadata: {
        createdBy: 'SafetyFirstRepairFramework',
        version: '1.0.0'
      }
    };
    
    fs.writeFileSync(backupPath, JSON.stringify(backupData, null, 2));
    
    console.log(`💾 备份创建完成: ${backupPath}`);
    
    return {
      id: backupId,
      location: backupPath,
      timestamp: backupData.timestamp,
      size: fs.statSync(backupPath).size
    };
  }

  async validateRepairSafety(problem, causeAnalysis) {
    console.log('🛡️ 验证修复安全性...');
    
    const safetyChecks = [
      this.checkRiskLevel(problem),
      this.checkImpactScope(causeAnalysis),
      this.checkRecoveryPlan(problem),
      this.checkHumanApprovalRequired(problem)
    ];
    
    const results = await Promise.all(safetyChecks);
    
    const passedChecks = results.filter(r => r.passed);
    const failedChecks = results.filter(r => !r.passed);
    
    return {
      safe: failedChecks.length === 0,
      passedChecks: passedChecks.length,
      totalChecks: results.length,
      failedChecks: failedChecks.map(fc => fc.name),
      details: results
    };
  }

  async checkRiskLevel(problem) {
    // 评估问题风险等级
    const riskLevels = {
      'exec_tool_failure': 'medium',
      'session_congestion': 'high',
      'configuration_error': 'medium',
      'memory_issue': 'high',
      'performance_degradation': 'medium'
    };
    
    const riskLevel = riskLevels[problem.type] || 'unknown';
    const isSafe = riskLevel !== 'high' || (riskLevel === 'high' && this.hasLowRiskMitigation(problem));
    
    return {
      name: 'risk_level_check',
      passed: isSafe,
      riskLevel: riskLevel,
      description: `问题类型 "${problem.type}" 风险等级: ${riskLevel}`
    };
  }

  async checkImpactScope(causeAnalysis) {
    // 评估修复影响范围
    const impactScope = this.assessImpactScope(causeAnalysis);
    const isSafe = impactScope !== 'system_wide';
    
    return {
      name: 'impact_scope_check',
      passed: isSafe,
      impactScope: impactScope,
      description: `修复影响范围: ${impactScope}`
    };
  }

  async checkRecoveryPlan(problem) {
    // 检查是否有恢复计划
    const hasRecoveryPlan = this.hasRecoveryPlanForProblem(problem);
    
    return {
      name: 'recovery_plan_check',
      passed: hasRecoveryPlan,
      hasRecoveryPlan: hasRecoveryPlan,
      description: hasRecoveryPlan ? '存在恢复计划' : '缺少恢复计划'
    };
  }

  async checkHumanApprovalRequired(problem) {
    // 检查是否需要人工批准
    const requiresApproval = this.problemRequiresHumanApproval(problem);
    const hasApproval = !requiresApproval || this.hasHumanApproval(problem);
    
    return {
      name: 'human_approval_check',
      passed: hasApproval,
      requiresApproval: requiresApproval,
      hasApproval: hasApproval,
      description: requiresApproval ? 
        (hasApproval ? '已获得人工批准' : '需要人工批准') : 
        '无需人工批准'
    };
  }

  async createProgressiveRepairPlan(problem, causeAnalysis, safetyValidation) {
    console.log('📋 创建渐进修复计划...');
    
    // 基于问题类型和原因分析创建分阶段计划
    const basePlan = this.getBaseRepairPlan(problem.type);
    
    // 根据安全验证结果调整计划
    const adjustedPlan = this.adjustPlanForSafety(basePlan, safetyValidation);
    
    // 添加验证阶段
    const planWithValidation = this.addValidationPhases(adjustedPlan);
    
    return {
      id: `plan_${Date.now()}_${problem.type}`,
      problemType: problem.type,
      createdAt: new Date().toISOString(),
      safetyValidation: safetyValidation,
      phases: planWithValidation,
      estimatedDuration: this.estimateDuration(planWithValidation),
      rollbackStrategy: this.getRollbackStrategy(problem)
    };
  }

  getBaseRepairPlan(problemType) {
    // 基于问题类型获取基础修复计划
    const basePlans = {
      'exec_tool_failure': [
        { name: 'diagnose_exec_environment', action: '检查执行环境', duration: 1000 },
        { name: 'test_simple_command', action: '测试简单命令', duration: 2000 },
        { name: 'verify_permissions', action: '验证权限', duration: 1500 },
        { name: 'optimize_command_execution', action: '优化命令执行', duration: 3000 }
      ],
      'session_congestion': [
        { name: 'analyze_context_usage', action: '分析上下文使用', duration: 1000 },
        { name: 'smart_cleanup', action: '智能清理', duration: 2000 },
        { name: 'session_restart', action: '重启会话', duration: 3000 },
        { name: 'verify_response_improvement', action: '验证响应改善', duration: 1500 }
      ]
    };
    
    return basePlans[problemType] || [
      { name: 'general_diagnosis', action: '通用诊断', duration: 2000 },
      { name: 'safe_repair_attempt', action: '安全修复尝试', duration: 3000 },
      { name: 'validation', action: '验证修复效果', duration: 1500 }
    ];
  }

  async executeRepairPhase(phase, problem, phaseIndex) {
    console.log(`⚙️ 执行修复阶段: ${phase.name} (${phase.action})`);
    
    // 模拟阶段执行
    await new Promise(resolve => setTimeout(resolve, phase.duration || 1000));
    
    // 这里应该执行实际的修复操作
    // 暂时返回模拟结果
    return {
      phaseName: phase.name,
      phaseIndex: phaseIndex,
      executedAt: new Date().toISOString(),
      result: 'simulated_execution_complete',
      metrics: {
        executionTime: phase.duration || 1000,
        success: Math.random() > 0.1 // 90%成功率
      }
    };
  }

  async validateRepairPhase(phaseResult, phase) {
    // 验证阶段执行结果
    const isValid = phaseResult.metrics?.success !== false;
    
    return {
      phase: phase.name,
      success: isValid,
      reason: isValid ? 'phase_execution_successful' : 'phase_execution_failed',
      validationTime: new Date().toISOString(),
      details: phaseResult
    };
  }

  shouldRollback(phaseValidation, currentPhaseIndex, totalPhases) {
    // 决定是否需要回滚
    if (!phaseValidation.success) {
      // 高风险阶段失败时回滚
      if (currentPhaseIndex === 0) return true; // 第一阶段失败
      if (phaseValidation.reason.includes('critical')) return true;
    }
    
    return false;
  }

  async rollbackToBackup(backup, repairLog) {
    console.log(`🔄 执行回滚到备份: ${backup.id}`);
    
    try {
      // 这里应该执行实际的回滚操作
      // 暂时模拟
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const rollbackResult = {
        backupId: backup.id,
        rolledBackAt: new Date().toISOString(),
        success: true,
        restoredState: 'simulated_restore_complete'
      };
      
      // 记录回滚到知识库
      await this.recordRollbackKnowledge(repairLog, rollbackResult);
      
      return rollbackResult;
      
    } catch (error) {
      console.error('❌ 回滚失败:', error);
      return {
        backupId: backup.id,
        rolledBackAt: new Date().toISOString(),
        success: false,
        error: error.message
      };
    }
  }

  async validateFinalRepair(repairLog) {
    console.log('🔍 执行最终修复验证...');
    
    // 模拟最终验证
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 检查所有阶段是否成功
    const allPhasesSuccessful = repairLog.phases.every(p => 
      p.status === 'completed' && (!p.validation || p.validation.success)
    );
    
    return {
      success: allPhasesSuccessful,
      validatedAt: new Date().toISOString(),
      phaseCount: repairLog.phases.length,
      successfulPhases: repairLog.phases.filter(p => 
        p.status === 'completed' && (!p.validation || p.validation.success)
      ).length,
      details: 'simulated_final_validation'
    };
  }

  async recordSuccessfulRepair(repairLog, finalValidation) {
    // 记录成功修复到知识库
    const successRecord = {
      id: repairLog.id,
      timestamp: repairLog.timestamp,
      problemType: repairLog.problem.type,
      phases: repairLog.phases.length,
      finalValidation: finalValidation,
      learnedLessons: this.extractLessons(repairLog)
    };
    
    this.knowledgeBase.successfulRepairs.push(successRecord);
    
    // 更新修复策略成功率
    this.updateRepairStrategySuccessRate(repairLog.problem.type, true);
    
    // 保存知识库
    await this.saveKnowledgeBase();
    
    console.log(`📚 成功修复记录到知识库: ${repairLog.id}`);
  }

  async recordRepairResult(repairLog) {
    const repairsDir = path.join(this.workspacePath, 'repair_logs');
    if (!fs.existsSync(repairsDir)) {
      fs.mkdirSync(repairsDir, { recursive: true });
    }
    
    const logPath = path.join(repairsDir, `${repairLog.id}.json`);
    fs.writeFileSync(logPath, JSON.stringify(repairLog, null, 2));
    
    console.log(`📝 修复日志保存: ${logPath}`);
  }

  async recordRollbackKnowledge(repairLog, rollbackResult) {
    // 记录回滚经验到知识库
    const rollbackRecord = {
      repairId: repairLog.id,
      rolledBackAt: rollbackResult.rolledBackAt,
      reason: repairLog.status,
      phaseCount: repairLog.phases.length,
      learnedLessons: this.extractRollbackLessons(repairLog, rollbackResult)
    };
    
    this.knowledgeBase.failedRepairs.push(rollbackRecord);
    
    // 更新修复策略成功率
    this.updateRepairStrategySuccessRate(repairLog.problem.type, false);
    
    // 保存知识库
    await this.saveKnowledgeBase();
    
    console.log(`📚 回滚经验记录到知识库`);
  }

  extractLessons(repairLog) {
    // 从修复日志中提取经验教训
    return [
      `问题类型: ${repairLog.problem.type}`,
      `使用策略: ${repairLog.repairPlan?.id || 'unknown'}`,
      `阶段数: ${repairLog.phases.length}`,
      `关键成功因素: 渐进执行和阶段验证`
    ];
  }

  extractRollbackLessons(repairLog, rollbackResult) {
    // 从回滚中提取经验教训
    return [
      `回滚原因: ${repairLog.status}`,
      `失败阶段: ${repairLog.phases.find(p => p.status === 'failed')?.name || 'unknown'}`,
      `学习点: ${rollbackResult.success ? '回滚成功' : '回滚失败，需改进'}`,
      `改进建议: 加强阶段验证和风险评估`
    ];
  }

  updateRepairStrategySuccessRate(problemType, success) {
    // 更新修复策略的成功率
    if (this.knowledgeBase.repairStrategies[problemType]) {
      const strategy = this.knowledgeBase.repairStrategies[problemType];
      const totalAttempts = (strategy.successCount || 0) + (strategy.failureCount || 0) + 1;
      
      if (success) {
        strategy.successCount = (strategy.successCount || 0) + 1;
      } else {
        strategy.failureCount = (strategy.failureCount || 0) + 1;
      }
      
      strategy.successRate = (strategy.successCount || 0) / totalAttempts;
      strategy.lastUsed = new Date().toISOString();
    }
  }

  async saveKnowledgeBase() {
    fs.writeFileSync(this.knowledgeBasePath, JSON.stringify(this.knowledgeBase, null, 2));
  }

  // 辅助方法（模拟实现）
  getConfigFileList() {
    return ['openclaw.json', 'session_management.json5'];
  }

  getCurrentSettings() {
    return { model: 'deepseek-v3.2', timeout: 30000 };
  }

  getRuntimeState() {
    return { memoryUsage: process.memoryUsage(), uptime: process.uptime() };
  }

  hasLowRiskMitigation(problem) {
    return problem.type === 'session_congestion'; // 已有成熟解决方案
  }

  assessImpactScope(causeAnalysis) {
    if (causeAnalysis?.immediate_cause?.includes('system')) return 'system_wide';
    if (causeAnalysis?.immediate_cause?.includes('config')) return 'configuration';
    return 'localized';
  }

  hasRecoveryPlanForProblem(problem) {
    const problemsWithRecovery = ['session_congestion', 'exec_tool_failure'];
    return problemsWithRecovery.includes(problem.type);
  }

  problemRequiresHumanApproval(problem) {
    return problem.type === 'configuration_error' || problem.severity === 'critical';
  }

  hasHumanApproval(problem) {
    // 模拟：假设已获得批准
    return true;
  }

  adjustPlanForSafety(basePlan, safetyValidation) {
    // 根据安全验证结果调整计划
    if (safetyValidation.failedChecks.length > 0) {
      // 添加额外的安全措施
      return [
        { name: 'enhanced_safety_precheck', action: '增强安全检查', duration: 1000 },
        ...basePlan
      ];
    }
    return basePlan;
  }

  addValidationPhases(plan) {
    // 在每个主要阶段后添加验证阶段
    const planWithValidation = [];
    
    plan.forEach((phase, index) => {
      planWithValidation.push(phase);
      
      // 在每个阶段后添加验证（除了最后一个）
      if (index < plan.length - 1) {
        planWithValidation.push({
          name: `validate_${phase.name}`,
          action: `验证 ${phase.action} 结果`,
          duration: 500
        });
      }
    });
    
    return planWithValidation;
  }

  estimateDuration(phases) {
    return phases.reduce((total, phase) => total + (phase.duration || 1000), 0);
  }

  getRollbackStrategy(problem) {
    return {
      triggerConditions: ['phase_failure', 'validation_failure', 'timeout'],
      rollbackSteps: ['停止当前操作', '恢复备份', '验证恢复状态'],
      estimatedTime: 2000
    };
  }
}

// 如果直接运行，测试修复框架
if (require.main === module) {
  const repairFramework = new SafetyFirstRepairFramework();
  
  // 测试修复exec工具失败问题
  const testProblem = {
    type: 'exec_tool_failure',
    severity: 'medium',
    description: 'exec工具成功率85%偏低',
    detectedBy: 'SelfPerceptionSystem',
    timestamp: new Date().toISOString()
  };
  
  const testCauseAnalysis = {
    immediate_cause: ['命令执行超时', '权限限制'],
    underlying_patterns: ['复杂命令执行', '系统资源限制'],
    future_risks: ['任务执行失败率可能上升']
  };
  
  console.log('🧪 测试安全优先修复框架...');
  console.log(`问题: ${testProblem.description}`);
  
  repairFramework.safeRepair(testProblem, testCauseAnalysis).then(result => {
    console.log('\n📊 修复结果:');
    console.log(`状态: ${result.status}`);
    console.log(`修复ID: ${result.repairLogId || 'N/A'}`);
    
    if (result.phases) {
      console.log(`阶段数: ${result.phases}`);
    }
    
    if (result.finalValidation) {
      console.log(`最终验证: ${result.finalValidation.success ? '通过' : '未通过'}`);
    }
    
    if (result.backupKept) {
      console.log(`备份位置: ${result.backupKept}`);
    }
    
    process.exit(0);
  }).catch(error => {
    console.error('修复测试失败:', error);
    process.exit(1);
  });
}

module.exports = SafetyFirstRepairFramework;