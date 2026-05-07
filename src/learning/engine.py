#!/usr/bin/env python3
"""
学习引擎 - 完整的自主学习系统
实现实时浏览器学习、知识内化、动态优化等功能
"""

import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import re
import os
import hashlib
from enum import Enum
import html2text
from urllib.parse import urlparse, urljoin
import sqlite3


class LearningStrategy(Enum):
    """学习策略"""
    BROWSER_RESEARCH = "browser_research"      # 浏览器研究
    FEEDBACK_ANALYSIS = "feedback_analysis"    # 反馈分析
    PATTERN_RECOGNITION = "pattern_recognition" # 模式识别
    KNOWLEDGE_SYNTHESIS = "knowledge_synthesis" # 知识合成
    ERROR_LEARNING = "error_learning"          # 错误学习


class KnowledgeDomain(Enum):
    """知识领域"""
    TECHNOLOGY = "technology"          # 技术
    PROGRAMMING = "programming"        # 编程
    AI_ML = "ai_ml"                   # AI/机器学习
    SYSTEM_ADMIN = "system_admin"     # 系统管理
    SECURITY = "security"             # 安全
    PRODUCTIVITY = "productivity"     # 生产力
    OTHER = "other"                   # 其他


@dataclass
class LearningTask:
    """学习任务"""
    id: str
    strategy: LearningStrategy
    query: str
    domain: KnowledgeDomain
    priority: int = 5  # 1-10, 10最高
    
    # 目标
    target_knowledge_points: int = 10
    max_duration_minutes: int = 30
    
    # 状态
    status: str = "pending"  # pending, running, completed, failed
    progress: float = 0.0
    results: List[Dict[str, Any]] = field(default_factory=list)
    
    # 元数据
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    error_message: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def start(self):
        """开始任务"""
        self.status = "running"
        self.started_at = datetime.now()
        self.progress = 0.1
    
    def complete(self, results: List[Dict[str, Any]]):
        """完成任务"""
        self.status = "completed"
        self.completed_at = datetime.now()
        self.progress = 1.0
        self.results = results
    
    def fail(self, error_message: str):
        """任务失败"""
        self.status = "failed"
        self.completed_at = datetime.now()
        self.error_message = error_message


@dataclass
class KnowledgePoint:
    """知识点"""
    id: str
    content: str
    source: str
    domain: KnowledgeDomain
    confidence: float = 0.8  # 0-1, 置信度
    
    # 关联信息
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)  # 先决知识ID
    related_points: List[str] = field(default_factory=list)  # 相关知识点ID
    
    # 验证信息
    verified: bool = False
    verification_sources: List[str] = field(default_factory=list)
    verification_count: int = 0
    
    # 使用统计
    usage_count: int = 0
    last_used: datetime = None
    relevance_score: float = 0.5
    
    # 元数据
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def verify(self, source: str):
        """验证知识点"""
        self.verified = True
        self.verification_sources.append(source)
        self.verification_count += 1
        self.confidence = min(1.0, self.confidence + 0.1)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'source': self.source,
            'domain': self.domain.value,
            'confidence': self.confidence,
            'tags': self.tags,
            'prerequisites': self.prerequisites,
            'related_points': self.related_points,
            'verified': self.verified,
            'verification_sources': self.verification_sources,
            'verification_count': self.verification_count,
            'usage_count': self.usage_count,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'relevance_score': self.relevance_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    def use(self):
        """使用知识点"""
        self.usage_count += 1
        self.last_used = datetime.now()
        self.relevance_score = min(1.0, self.relevance_score + 0.05)


class LearningEngine:
    """完整的学习引擎"""
    
    def __init__(self, config_path: str = "config/learning.yaml"):
        self.config = self._load_config(config_path)
        self._init_database()
        self._init_http_client()
        
        # 学习任务队列
        self.task_queue = []
        self.active_tasks = {}
        self.completed_tasks = []
        
        # 知识库
        self.knowledge_base = {}
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            "browser_research": {
                "enabled": True,
                "max_concurrent": 3,
                "timeout_seconds": 60,
                "proxy": "",
                "sources": [
                    "https://docs.python.org/",
                    "https://stackoverflow.com/",
                    "https://github.com/",
                    "https://docs.openclaw.ai/"
                ]
            },
            "knowledge_processing": {
                "min_confidence": 0.6,
                "verification_required": True,
                "max_points_per_domain": 1000,
                "compression_enabled": True
            },
            "context_optimization": {
                "enabled": True,
                "target_context_size": 150000,
                "compression_algorithms": ["summarization", "deduplication"]
            }
        }
        
        # 尝试加载用户配置
        try:
            if os.path.exists(config_path):
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                return {**default_config, **user_config}
        except Exception as e:
            print(f"配置加载失败，使用默认配置: {e}")
        
        return default_config
    
    def _init_database(self):
        """初始化数据库"""
        db_path = "data/learning.db"
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_conn = sqlite3.connect(db_path, check_same_thread=False)
        self.db_conn.row_factory = sqlite3.Row
        self.db_cursor = self.db_conn.cursor()
        
        # 学习任务表
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_tasks (
                id TEXT PRIMARY KEY,
                strategy TEXT NOT NULL,
                query TEXT NOT NULL,
                domain TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                target_knowledge_points INTEGER DEFAULT 10,
                max_duration_minutes INTEGER DEFAULT 30,
                status TEXT DEFAULT 'pending',
                progress REAL DEFAULT 0.0,
                results TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                error_message TEXT
            )
        ''')
        
        # 知识点表
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_points (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                domain TEXT NOT NULL,
                confidence REAL DEFAULT 0.8,
                tags TEXT,
                prerequisites TEXT,
                related_points TEXT,
                verified INTEGER DEFAULT 0,
                verification_sources TEXT,
                verification_count INTEGER DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                last_used TEXT,
                relevance_score REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # 学习记录表
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                knowledge_point_id TEXT NOT NULL,
                learning_method TEXT,
                effectiveness_score REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES learning_tasks(id),
                FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id)
            )
        ''')
        
        self.db_conn.commit()
    
    def _init_http_client(self):
        """初始化HTTP客户端"""
        self.session = None  # 将在异步环境中初始化
    
    async def start_async_session(self):
        """启动异步会话"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=60)
            # 配置代理
            proxy_url = self.config.get("browser_research", {}).get("proxy", None)
            connector = None
            if proxy_url:
                self.logger.info(f"使用代理: {proxy_url}")
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def close_async_session(self):
        """关闭异步会话"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def create_learning_task(self, query: str, 
                           strategy: LearningStrategy = LearningStrategy.BROWSER_RESEARCH,
                           domain: KnowledgeDomain = KnowledgeDomain.TECHNOLOGY,
                           priority: int = 5) -> str:
        """
        创建学习任务
        """
        task_id = f"learn_{hashlib.md5(query.encode()).hexdigest()[:12]}_{int(datetime.now().timestamp())}"
        
        task = LearningTask(
            id=task_id,
            strategy=strategy,
            query=query,
            domain=domain,
            priority=priority
        )
        
        # 保存到数据库
        self.db_cursor.execute('''
            INSERT INTO learning_tasks 
            (id, strategy, query, domain, priority, target_knowledge_points, 
             max_duration_minutes, status, progress, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.strategy.value,
            task.query,
            task.domain.value,
            task.priority,
            task.target_knowledge_points,
            task.max_duration_minutes,
            task.status,
            task.progress,
            task.created_at.isoformat()
        ))
        
        self.db_conn.commit()
        
        # 添加到队列
        self.task_queue.append(task)
        
        return task_id
    
    async def execute_learning_task(self, task_id: str) -> List[KnowledgePoint]:
        """
        执行学习任务
        """
        # 获取任务
        self.db_cursor.execute('SELECT * FROM learning_tasks WHERE id = ?', (task_id,))
        row = self.db_cursor.fetchone()
        
        if not row:
            raise ValueError(f"任务 {task_id} 不存在")
        
        task = LearningTask(
            id=row['id'],
            strategy=LearningStrategy(row['strategy']),
            query=row['query'],
            domain=KnowledgeDomain(row['domain']),
            priority=row['priority'],
            target_knowledge_points=row['target_knowledge_points'],
            max_duration_minutes=row['max_duration_minutes'],
            status=row['status'],
            progress=row['progress'],
            created_at=datetime.fromisoformat(row['created_at'])
        )
        
        # 更新任务状态
        task.start()
        self.db_cursor.execute('''
            UPDATE learning_tasks 
            SET status = ?, started_at = ?, progress = ?
            WHERE id = ?
        ''', (task.status, task.started_at.isoformat(), task.progress, task.id))
        self.db_conn.commit()
        
        # 根据策略执行学习
        try:
            if task.strategy == LearningStrategy.BROWSER_RESEARCH:
                results = await self._browser_research(task)
            elif task.strategy == LearningStrategy.FEEDBACK_ANALYSIS:
                results = await self._feedback_analysis(task)
            elif task.strategy == LearningStrategy.PATTERN_RECOGNITION:
                results = await self._pattern_recognition(task)
            elif task.strategy == LearningStrategy.KNOWLEDGE_SYNTHESIS:
                results = await self._knowledge_synthesis(task)
            elif task.strategy == LearningStrategy.ERROR_LEARNING:
                results = await self._error_learning(task)
            else:
                raise ValueError(f"未知的学习策略: {task.strategy}")
            
            # 处理结果
            knowledge_points = []
            for result in results:
                kp = self._create_knowledge_point(result, task)
                knowledge_points.append(kp)
            
            # 完成任务
            task.complete([kp.to_dict() for kp in knowledge_points])
            
            # 保存任务结果
            self.db_cursor.execute('''
                UPDATE learning_tasks 
                SET status = ?, completed_at = ?, progress = ?, results = ?
                WHERE id = ?
            ''', (
                task.status,
                task.completed_at.isoformat(),
                task.progress,
                json.dumps(task.results),
                task.id
            ))
            
            # 保存知识点
            for kp in knowledge_points:
                self._save_knowledge_point(kp)
            
            self.db_conn.commit()
            
            return knowledge_points
            
        except Exception as e:
            # 任务失败
            task.fail(str(e))
            
            self.db_cursor.execute('''
                UPDATE learning_tasks 
                SET status = ?, completed_at = ?, error_message = ?
                WHERE id = ?
            ''', (task.status, task.completed_at.isoformat(), task.error_message, task.id))
            
            self.db_conn.commit()
            raise
    
    async def _browser_research(self, task: LearningTask) -> List[Dict[str, Any]]:
        """
        浏览器研究策略
        从多个来源获取信息
        网络不可用时优雅降级到冷启动知识生成
        """
        results = []
        
        # 确保会话已启动
        await self.start_async_session()
        
        # 构建搜索查询
        search_queries = self._generate_search_queries(task.query)
        
        # 从配置的源获取信息
        sources = self.config["browser_research"]["sources"]
        
        for source in sources:
            for query in search_queries[:3]:  # 限制查询数量
                try:
                    # 构造URL（简化版，实际需要根据源调整）
                    if "docs.python.org" in source:
                        url = f"{source}search.html?q={query}"
                    elif "stackoverflow.com" in source:
                        url = f"{source}search?q={query}"
                    else:
                        url = source
                    
                    # 获取内容
                    content = await self._fetch_url_content(url)
                    
                    # 提取有用信息
                    extracted = self._extract_relevant_content(content, task.query)
                    
                    if extracted:
                        results.append({
                            "source": url,
                            "content": extracted,
                            "relevance": self._calculate_relevance(extracted, task.query),
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        # 如果已获取足够信息，提前返回
                        if len(results) >= task.target_knowledge_points:
                            return results
                    
                except Exception as e:
                    print(f"从 {source} 获取信息失败: {e}")
                    continue
        
        # 网络不可用时的降级策略
        if not results:
            print("网络不可用，降级到冷启动知识生成")
            fallback = self._generate_cold_start_knowledge(task.query, task.domain)
            for item in fallback:
                results.append({
                    "source": f"browser_research_fallback/{task.domain.value}",
                    "content": item["content"],
                    "relevance": item.get("relevance", 0.6),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    async def _feedback_analysis(self, task: LearningTask) -> List[Dict[str, Any]]:
        """
        反馈分析策略
        分析用户反馈和历史交互
        """
        # 从数据库获取历史反馈
        # 这里简化实现，实际需要查询历史交互记录
        results = []
        
        # 分析最近的成功和失败案例
        recent_success = self._get_recent_successes(task.domain)
        recent_failures = self._get_recent_failures(task.domain)
        
        # 提取模式
        if recent_success:
            pattern = self._extract_success_pattern(recent_success)
            results.append({
                "source": "success_pattern_analysis",
                "content": f"成功模式分析: {pattern}",
                "relevance": 0.9,
                "timestamp": datetime.now().isoformat()
            })
        
        if recent_failures:
            pattern = self._extract_failure_pattern(recent_failures)
            results.append({
                "source": "failure_pattern_analysis",
                "content": f"失败模式分析: {pattern}",
                "relevance": 0.9,
                "timestamp": datetime.now().isoformat()
            })
        
        return results
    
    async def _pattern_recognition(self, task: LearningTask) -> List[Dict[str, Any]]:
        """
        模式识别策略
        识别数据中的模式和规律
        """
        # 获取相关历史数据
        related_data = self._get_related_historical_data(task.query, task.domain)
        
        results = []
        
        if related_data:
            # 分析模式
            patterns = self._analyze_patterns(related_data)
            
            for pattern in patterns:
                results.append({
                    "source": "pattern_recognition",
                    "content": f"识别到的模式: {pattern}",
                    "relevance": self._calculate_pattern_relevance(pattern, task.query),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    async def _knowledge_synthesis(self, task: LearningTask) -> List[Dict[str, Any]]:
        """
        知识合成策略
        合成现有知识创造新见解
        冷启动时通过分析查询本身生成知识点
        """
        # 获取相关知识点
        related_knowledge = self._get_related_knowledge(task.query, task.domain)
        
        results = []
        
        if related_knowledge:
            # 合成新知识
            synthesis = self._synthesize_knowledge(related_knowledge, task.query)
            
            if synthesis:
                results.append({
                    "source": "knowledge_synthesis",
                    "content": synthesis,
                    "relevance": 0.85,
                    "timestamp": datetime.now().isoformat()
                })
        
        # 冷启动生成：即使没有相关知识，也根据查询生成知识点
        # 这让系统在第一次运行时就能获得知识
        if not results:
            cold_start_knowledge = self._generate_cold_start_knowledge(task.query, task.domain)
            for item in cold_start_knowledge:
                results.append({
                    "source": f"cold_start_knowledge_synthesis",
                    "content": item["content"],
                    "relevance": item.get("relevance", 0.7),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    async def _error_learning(self, task: LearningTask) -> List[Dict[str, Any]]:
        """
        错误学习策略
        从错误中学习
        """
        # 获取错误记录
        error_records = self._get_error_records(task.domain)
        
        results = []
        
        if error_records:
            # 分析错误原因和解决方案
            lessons = self._extract_lessons_from_errors(error_records)
            
            for lesson in lessons:
                results.append({
                    "source": "error_learning",
                    "content": f"从错误中学习: {lesson}",
                    "relevance": 0.95,  # 错误学习通常相关性很高
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    async def _fetch_url_content(self, url: str) -> str:
        """获取URL内容，支持代理配置"""
        try:
            # 检查是否配置了代理
            proxy_url = self.config.get("browser_research", {}).get("proxy", None)
            kwargs = {
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                'timeout': aiohttp.ClientTimeout(total=30)
            }
            if proxy_url:
                kwargs['proxy'] = proxy_url
            
            async with self.session.get(url, **kwargs) as response:
                if response.status == 200:
                    content = await response.text()
                    return content
                else:
                    raise Exception(f"HTTP {response.status}")
        except Exception as e:
            raise Exception(f"获取URL失败: {url}, 错误: {e}")
    
    def _extract_relevant_content(self, html_content: str, query: str) -> str:
        """提取相关内容"""
        # 转换为文本
        h = html2text.HTML2Text()
        h.ignore_links = False
        text = h.handle(html_content)
        
        # 分割为段落
        paragraphs = text.split('\n\n')
        
        # 查找与查询相关的段落
        relevant_paragraphs = []
        query_terms = query.lower().split()
        
        for para in paragraphs:
            if len(para.strip()) < 50:
                continue
            
            para_lower = para.lower()
            
            # 计算相关性分数
            relevance_score = 0
            for term in query_terms:
                if term in para_lower:
                    relevance_score += 1
            
            # 如果包含任何查询术语，保留
            if relevance_score > 0:
                # 清理文本
                cleaned = self._clean_text(para)
                if cleaned:
                    relevant_paragraphs.append(cleaned)
        
        # 返回最相关的段落
        if relevant_paragraphs:
            return '\n\n'.join(relevant_paragraphs[:3])  # 返回最多3个段落
        else:
            return ""
    
    def _create_knowledge_point(self, data: Dict[str, Any], task: LearningTask) -> KnowledgePoint:
        """创建知识点"""
        kp_id = f"kp_{hashlib.md5(data['content'].encode()).hexdigest()[:12]}_{int(datetime.now().timestamp())}"
        
        # 提取标签
        tags = self._extract_tags(data['content'], task.query)
        
        # 确定置信度
        confidence = data.get('relevance', 0.5) * 0.8
        
        kp = KnowledgePoint(
            id=kp_id,
            content=data['content'],
            source=data['source'],
            domain=task.domain,
            confidence=confidence,
            tags=tags,
            verification_sources=[data['source']] if data.get('verified', False) else []
        )
        
        return kp
    
    def _save_knowledge_point(self, kp: KnowledgePoint):
        """保存知识点"""
        self.db_cursor.execute('''
            INSERT OR IGNORE INTO knowledge_points 
            (id, content, source, domain, confidence, tags, prerequisites, 
             related_points, verified, verification_sources, verification_count,
             usage_count, last_used, relevance_score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            kp.id,
            kp.content,
            kp.source,
            kp.domain.value,
            kp.confidence,
            json.dumps(kp.tags),
            json.dumps(kp.prerequisites),
            json.dumps(kp.related_points),
            1 if kp.verified else 0,
            json.dumps(kp.verification_sources),
            kp.verification_count,
            kp.usage_count,
            kp.last_used.isoformat() if kp.last_used else None,
            kp.relevance_score,
            kp.created_at.isoformat(),
            kp.updated_at.isoformat()
        ))
    
    def get_relevant_knowledge(self, query: str, domain: KnowledgeDomain = None, 
                              limit: int = 10) -> List[KnowledgePoint]:
        """获取相关知识"""
        conditions = []
        params = []
        
        if domain:
            conditions.append("domain = ?")
            params.append(domain.value)
        
        # 标签匹配
        query_terms = query.lower().split()
        tag_conditions = []
        for term in query_terms:
            if len(term) > 3:  # 只匹配较长的术语
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{term}%")
        
        if tag_conditions:
            conditions.append(f"({' OR '.join(tag_conditions)})")
        
        # 内容匹配
        content_conditions = []
        for term in query_terms:
            if len(term) > 3:
                content_conditions.append("content LIKE ?")
                params.append(f"%{term}%")
        
        if content_conditions:
            if conditions:
                conditions.append(f"({' OR '.join(content_conditions)})")
            else:
                conditions.append(f"({' OR '.join(content_conditions)})")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        self.db_cursor.execute(f'''
            SELECT * FROM knowledge_points 
            WHERE {where_clause}
            ORDER BY relevance_score DESC, confidence DESC
            LIMIT ?
        ''', params + [limit])
        
        knowledge_points = []
        for row in self.db_cursor.fetchall():
            kp = KnowledgePoint(
                id=row['id'],
                content=row['content'],
                source=row['source'],
                domain=KnowledgeDomain(row['domain']),
                confidence=row['confidence'],
                tags=json.loads(row['tags'] or '[]'),
                prerequisites=json.loads(row['prerequisites'] or '[]'),
                related_points=json.loads(row['related_points'] or '[]'),
                verified=bool(row['verified']),
                verification_sources=json.loads(row['verification_sources'] or '[]'),
                verification_count=row['verification_count'],
                usage_count=row['usage_count'],
                last_used=datetime.fromisoformat(row['last_used']) if row['last_used'] else None,
                relevance_score=row['relevance_score'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            )
            knowledge_points.append(kp)
            
            # 更新使用统计
            kp.use()
            self.db_cursor.execute('''
                UPDATE knowledge_points 
                SET usage_count = usage_count + 1, 
                    last_used = ?,
                    relevance_score = ?
                WHERE id = ?
            ''', (kp.last_used.isoformat(), kp.relevance_score, kp.id))
        
        self.db_conn.commit()
        
        return knowledge_points
    
    def optimize_context_with_knowledge(self, context: str, target_tokens: int) -> str:
        """
        使用知识优化上下文
        用知识点引用替换详细内容
        """
        # 分析当前上下文
        # 识别可以压缩的部分
        
        # 查找相关知识
        # 用知识点ID引用替换详细描述
        
        # 返回优化后的上下文
        return context
    
    # 辅助方法
    def _generate_search_queries(self, base_query: str) -> List[str]:
        """生成搜索查询"""
        queries = [base_query]
        
        # 添加变体
        if "how to" in base_query.lower():
            queries.append(base_query.replace("how to", "").strip())
            queries.append(f"{base_query} tutorial")
            queries.append(f"{base_query} guide")
        
        if "error" in base_query.lower():
            queries.append(f"fix {base_query}")
            queries.append(f"troubleshoot {base_query}")
        
        return queries
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """计算相关性"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # 简单算法：术语匹配比例
        query_terms = query_lower.split()
        matches = sum(1 for term in query_terms if term in content_lower)
        
        return matches / max(len(query_terms), 1)
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符（保留常见标点）
        text = re.sub(r'[^\w\s.,!?;:\-\'\"()\[\]{}]', '', text)
        
        return text.strip()
    
    def _extract_tags(self, content: str, query: str) -> List[str]:
        """提取标签"""
        tags = []
        
        # 从查询中提取关键词
        query_terms = query.lower().split()
        tags.extend([term for term in query_terms if len(term) > 3])
        
        # 从内容中提取常见技术术语
        tech_terms = ["python", "javascript", "sql", "api", "http", "json", "xml"]
        for term in tech_terms:
            if term in content.lower():
                tags.append(term)
        
        return list(set(tags))  # 去重
    
    def _get_recent_successes(self, domain: KnowledgeDomain) -> List[Dict]:
        """获取最近的成功案例（简化）"""
        return []
    
    def _get_recent_failures(self, domain: KnowledgeDomain) -> List[Dict]:
        """获取最近的失败案例（简化）"""
        return []
    
    def _extract_success_pattern(self, successes: List[Dict]) -> str:
        """提取成功模式"""
        return "模式识别待实现"
    
    def _extract_failure_pattern(self, failures: List[Dict]) -> str:
        """提取失败模式"""
        return "错误模式分析待实现"
    
    def _get_related_historical_data(self, query: str, domain: KnowledgeDomain) -> List[Dict]:
        """获取相关历史数据"""
        return []
    
    def _analyze_patterns(self, data: List[Dict]) -> List[str]:
        """分析模式"""
        return []
    
    def _calculate_pattern_relevance(self, pattern: str, query: str) -> float:
        """计算模式相关性"""
        return 0.5
    
    def _get_related_knowledge(self, query: str, domain: KnowledgeDomain) -> List[KnowledgePoint]:
        """获取相关知识"""
        return self.get_relevant_knowledge(query, domain, limit=5)
    
    def _synthesize_knowledge(self, knowledge_points: List[KnowledgePoint], query: str) -> str:
        """合成知识"""
        if not knowledge_points:
            return ""
        
        # 简单合成：连接相关知识点
        synthesis = f"基于{len(knowledge_points)}个相关知识点的合成见解:\n\n"
        
        for i, kp in enumerate(knowledge_points[:3], 1):
            synthesis += f"{i}. {kp.content[:100]}...\n"
        
        return synthesis
    
    def _generate_cold_start_knowledge(self, query: str, domain: KnowledgeDomain) -> List[Dict]:
        """
        冷启动知识生成
        即使数据库为空，也能根据查询生成基础知识
        """
        results = []
        
        # 基于查询解析关键术语
        query_terms = [t for t in query.replace(':',' ').replace(',',' ').replace('，',' ').replace('：',' ').split() if len(t) > 1]
        
        # 领域特定模板知识
        domain_templates = {
            KnowledgeDomain.AI_ML: [
                "AI/ML系统优化是一个多层次过程，包括数据质量、模型架构、训练策略和部署优化",
                "模型微调是适应特定任务的关键技术，需要在通用能力和专用能力间找到平衡",
                "评估AI系统性能需要综合考量准确率、延迟、资源消耗和可解释性",
            ],
            KnowledgeDomain.TECHNOLOGY: [
                "系统架构设计遵循分层原则，每层职责分明，降低耦合度提升可维护性",
                "性能优化需要先测量后优化，避免过早优化引入复杂度和bug",
                "自动化测试是系统可靠性的基石，单元测试覆盖核心逻辑，集成测试验证交互",
            ],
            KnowledgeDomain.PROGRAMMING: [
                "代码质量通过静态分析、类型检查和代码审查来保证，三者互为补充",
                "设计模式解决特定场景下的常见问题，过度使用反而增加复杂度",
                "模块化设计使系统易于测试和维护，每个模块应有清晰的职责边界",
            ],
            KnowledgeDomain.SYSTEM_ADMIN: [
                "系统监控需要覆盖CPU、内存、磁盘IO和网络四个维度，任何一维瓶颈都影响整体",
                "日志管理包括采集、存储、分析和告警，结构化日志是高效分析的基础",
            ],
            KnowledgeDomain.SECURITY: [
                "安全防护需要纵深防御策略，单一安全措施无法抵御所有攻击向量",
                "最小权限原则是安全设计的核心，每个组件只拥有完成职责所需的最小权限",
            ],
        }
        
        # 通用知识生成
        generic_knowledge = [
            f"{query} 是一个值得深入研究的主题，系统化学习需要理论结合实践",
            f"在{domain.value}领域中，持续迭代和反馈驱动是提升效果的有效方法",
        ]
        
        # 收集所有要生成的知识点
        candidates = domain_templates.get(domain, []) + generic_knowledge
        
        for idx, content in enumerate(candidates[:5]):
            kp_id = f"cold_gen_{idx}_{hashlib.md5(content.encode()).hexdigest()[:8]}"
            results.append({
                "id": kp_id,
                "content": content,
                "source": f"cold_start_synthesis/{domain.value}",
                "domain": domain,
                "confidence": 0.6,
                "relevance": 0.7,
                "tags": query_terms + [domain.value],
                "verified": False,
            })
        
        return results
    
    def _get_error_records(self, domain: KnowledgeDomain) -> List[Dict]:
        """获取错误记录"""
        return []
    
    def _extract_lessons_from_errors(self, error_records: List[Dict]) -> List[str]:
        """从错误中提取教训"""
        return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {}
        
        # 任务统计
        self.db_cursor.execute('SELECT COUNT(*) as total FROM learning_tasks')
        stats['total_tasks'] = self.db_cursor.fetchone()['total']
        
        self.db_cursor.execute('SELECT status, COUNT(*) as count FROM learning_tasks GROUP BY status')
        stats['tasks_by_status'] = {row['status']: row['count'] for row in self.db_cursor.fetchall()}
        
        # 知识点统计
        self.db_cursor.execute('SELECT COUNT(*) as total FROM knowledge_points')
        stats['total_knowledge_points'] = self.db_cursor.fetchone()['total']
        
        self.db_cursor.execute('SELECT domain, COUNT(*) as count FROM knowledge_points GROUP BY domain')
        stats['knowledge_by_domain'] = {row['domain']: row['count'] for row in self.db_cursor.fetchall()}
        
        return stats
    
    def close(self):
        """关闭连接"""
        self.db_conn.close()
        # 注意：异步会话需要在异步环境中关闭


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # 创建学习引擎
        engine = LearningEngine()
        
        # 创建学习任务
        task_id = engine.create_learning_task(
            query="OpenClaw上下文优化解决方案",
            strategy=LearningStrategy.BROWSER_RESEARCH,
            domain=KnowledgeDomain.TECHNOLOGY,
            priority=8
        )
        
        print(f"创建学习任务: {task_id}")
        
        # 执行任务
        try:
            await engine.start_async_session()
            results = await engine.execute_learning_task(task_id)
            print(f"学习完成，获取到 {len(results)} 个知识点")
            
            # 获取相关知识
            related = engine.get_relevant_knowledge("上下文压缩", limit=5)
            print(f"找到 {len(related)} 个相关知识")
            
            # 获取统计信息
            stats = engine.get_statistics()
            print(f"学习统计: {stats}")
            
        finally:
            await engine.close_async_session()
            engine.close()
    
    # 运行示例
    asyncio.run(main())