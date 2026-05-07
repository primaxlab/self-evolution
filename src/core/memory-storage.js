/**
 * 记忆存储系统 - 实现跨会话永久记忆
 * 完整实现，使用 JSON 文件存储
 */

const fs = require('fs').promises;
const path = require('path');
const zlib = require('zlib');

class MemoryStorage {
    constructor(config = {}) {
        this.config = {
            storageType: config.storageType || 'json',
            retentionDays: config.retentionDays || 365,
            compressionEnabled: config.compressionEnabled !== false,
            dbPath: config.dbPath || './data/memory.json'
        };
        
        this.dbPath = this.resolvePath(this.config.dbPath);
        this.data = {
            memories: [],
            knowledge: [],
            skills: [],
            preferences: [],
            errors: [],
            successes: []
        };
        
        this.stats = {
            totalMemories: 0,
            fragmentation: 0,
            compressionRatio: 1.0,
            lastCleanup: null
        };
    }

    resolvePath(dbPath) {
        if (path.isAbsolute(dbPath)) {
            return dbPath;
        }
        return path.join(process.cwd(), dbPath);
    }

    async initialize() {
        try {
            await fs.mkdir(path.dirname(this.dbPath), { recursive: true });
            
            try {
                const content = await fs.readFile(this.dbPath, 'utf8');
                const decompressed = this.decompress(content);
                this.data = JSON.parse(decompressed);
                this.updateStats();
                console.log(`  Loaded ${this.data.memories.length} existing memories`);
            } catch (e) {
                // 文件不存在或解析失败，使用空数据
                console.log('  Starting with fresh memory store');
            }
        } catch (error) {
            console.error('Memory storage initialization failed:', error.message);
        }
    }

    async save() {
        try {
            const jsonStr = JSON.stringify(this.data);
            const compressed = this.compress(jsonStr);
            await fs.writeFile(this.dbPath, compressed, 'utf8');
            this.updateStats();
        } catch (error) {
            console.error('Failed to save memory:', error.message);
        }
    }

    compress(data) {
        if (!this.config.compressionEnabled) {
            return data;
        }
        try {
            const buffer = zlib.deflateSync(Buffer.from(data, 'utf8'));
            return buffer.toString('base64');
        } catch (e) {
            return data;
        }
    }

    decompress(data) {
        if (!this.config.compressionEnabled) {
            return data;
        }
        try {
            const buffer = Buffer.from(data, 'base64');
            return zlib.inflateSync(buffer).toString('utf8');
        } catch (e) {
            return data;
        }
    }

    updateStats() {
        this.stats.totalMemories = this.data.memories.length;
        this.stats.lastCleanup = new Date().toISOString();
        
        // 简单的碎片化计算
        const totalItems = Object.values(this.data).reduce((sum, arr) => sum + arr.length, 0);
        const uniqueIds = new Set(this.data.memories.map(m => m.id)).size;
        this.stats.fragmentation = 1 - (uniqueIds / Math.max(this.data.memories.length, 1));
    }

    // 添加记忆
    async addMemory(content, type = 'general', importance = 0.5) {
        const memory = {
            id: this.generateId(),
            content: content,
            type: type,
            importance: importance,
            createdAt: new Date().toISOString(),
            accessedAt: new Date().toISOString(),
            accessCount: 0,
            tags: this.extractTags(content)
        };

        this.data.memories.push(memory);
        await this.save();
        
        return memory;
    }

    // 添加知识
    async addKnowledge(topic, content, source = 'internal') {
        const knowledge = {
            id: this.generateId(),
            topic: topic,
            content: content,
            source: source,
            confidence: 0.8,
            createdAt: new Date().toISOString(),
            verified: source !== 'internal'
        };

        this.data.knowledge.push(knowledge);
        await this.save();
        
        return knowledge;
    }

    // 添加技能
    async addSkill(skillName, description, level = 0.5) {
        const skill = {
            id: this.generateId(),
            name: skillName,
            description: description,
            level: level,
            experience: 0,
            lastUsed: new Date().toISOString(),
            useCount: 0
        };

        this.data.skills.push(skill);
        await this.save();
        
        return skill;
    }

    // 记录错误
    async recordError(error, context = {}) {
        const errorRecord = {
            id: this.generateId(),
            message: error.message || String(error),
            stack: error.stack,
            context: context,
            createdAt: new Date().toISOString()
        };

        this.data.errors.push(errorRecord);
        await this.save();
        
        return errorRecord;
    }

    // 记录成功
    async recordSuccess(action, result = {}) {
        const successRecord = {
            id: this.generateId(),
            action: action,
            result: result,
            createdAt: new Date().toISOString()
        };

        this.data.successes.push(successRecord);
        await this.save();
        
        return successRecord;
    }

    // 搜索记忆
    async search(query, options = {}) {
        const {
            type = null,
            minImportance = 0,
            limit = 10,
            sortBy = 'relevance'
        } = options;

        let results = this.data.memories.filter(m => {
            if (type && m.type !== type) return false;
            if (m.importance < minImportance) return false;
            return this.matchesQuery(m, query);
        });

        // 排序
        if (sortBy === 'importance') {
            results.sort((a, b) => b.importance - a.importance);
        } else if (sortBy === 'recent') {
            results.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        } else {
            // relevance - 按匹配度排序
            results.sort((a, b) => this.calculateRelevance(b, query) - this.calculateRelevance(a, query));
        }

        // 更新访问统计
        for (const memory of results) {
            memory.accessCount++;
            memory.accessedAt = new Date().toISOString();
        }

        return results.slice(0, limit);
    }

    matchesQuery(memory, query) {
        const queryLower = query.toLowerCase();
        return (
            memory.content.toLowerCase().includes(queryLower) ||
            memory.tags.some(tag => tag.toLowerCase().includes(queryLower))
        );
    }

    calculateRelevance(memory, query) {
        let score = memory.importance;
        const queryLower = query.toLowerCase();
        
        if (memory.content.toLowerCase().includes(queryLower)) {
            score += 0.3;
        }
        
        score += Math.min(memory.accessCount * 0.01, 0.2);
        
        return score;
    }

    extractTags(content) {
        // 简单的标签提取
        const words = content.split(/\s+/)
            .filter(w => w.length > 3)
            .filter(w => !['the', 'and', 'for', 'with', 'this', 'that'].includes(w.toLowerCase()));
        
        // 返回频率最高的词作为标签
        const frequency = {};
        words.forEach(w => {
            frequency[w] = (frequency[w] || 0) + 1;
        });
        
        return Object.entries(frequency)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([word]) => word);
    }

    generateId() {
        return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    async getStats() {
        return {
            ...this.stats,
            totalKnowledge: this.data.knowledge.length,
            totalSkills: this.data.skills.length,
            totalErrors: this.data.errors.length,
            totalSuccesses: this.data.successes.length
        };
    }

    async cleanup() {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - this.config.retentionDays);

        const beforeCount = this.data.memories.length;
        
        this.data.memories = this.data.memories.filter(m => {
            if (m.importance > 0.8) return true; // 高重要性永久保留
            return new Date(m.createdAt) > cutoffDate;
        });

        this.data.errors = this.data.errors.filter(e => 
            new Date(e.createdAt) > cutoffDate
        );

        await this.save();
        
        return {
            before: beforeCount,
            after: this.data.memories.length,
            removed: beforeCount - this.data.memories.length
        };
    }

    async close() {
        await this.save();
    }
}

module.exports = { MemoryStorage };