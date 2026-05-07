#!/usr/bin/env python3
"""
记忆存储系统 - 完整的跨会话记忆存储引擎
"""

import sqlite3
import json
import pickle
import hashlib
import zlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os
import re
from enum import Enum


class MemoryType(Enum):
    """记忆类型"""
    EXPERIENCE = "experience"      # 经验记忆
    KNOWLEDGE = "knowledge"       # 知识记忆
    SKILL = "skill"              # 技能记忆
    PREFERENCE = "preference"    # 偏好记忆
    ERROR = "error"              # 错误记忆
    SUCCESS = "success"          # 成功记忆
    INTERACTION = "interaction"  # 交互记忆
    REFLECTION = "reflection"    # 反思记忆


class ImportanceLevel(Enum):
    """重要性级别"""
    CRITICAL = 10     # 关键记忆
    HIGH = 8          # 高重要性
    MEDIUM = 5        # 中等重要性
    LOW = 3           # 低重要性
    TRIVIAL = 1       # 琐碎记忆


@dataclass
class MemoryRecord:
    """记忆记录"""
    id: str                      # 唯一ID
    type: MemoryType             # 记忆类型
    content: str                 # 记忆内容
    timestamp: datetime          # 创建时间
    session_id: str              # 会话ID
    importance: ImportanceLevel  # 重要性级别
    
    # 关联信息
    associations: List[str] = None      # 关联的记忆ID
    tags: List[str] = None             # 标签
    metadata: Dict[str, Any] = None    # 元数据
    
    # 使用统计
    access_count: int = 0               # 访问次数
    last_accessed: datetime = None      # 最后访问时间
    relevance_score: float = 0.0        # 相关性分数
    
    def __post_init__(self):
        if self.associations is None:
            self.associations = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.last_accessed is None:
            self.last_accessed = self.timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['type'] = self.type.value
        data['importance'] = self.importance.value
        data['timestamp'] = self.timestamp.isoformat()
        data['last_accessed'] = self.last_accessed.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryRecord':
        """从字典创建"""
        data = data.copy()
        data['type'] = MemoryType(data['type'])
        data['importance'] = ImportanceLevel(data['importance'])
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        if data.get('last_accessed'):
            data['last_accessed'] = datetime.fromisoformat(data['last_accessed'])
        
        return cls(**data)


class MemoryStorage:
    """完整的记忆存储系统"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._init_database()
        self._init_cache()
        
    def _init_database(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # 创建记忆表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                compressed_content BLOB,
                timestamp TEXT NOT NULL,
                session_id TEXT NOT NULL,
                importance INTEGER NOT NULL,
                associations TEXT,
                tags TEXT,
                metadata TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                relevance_score REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(type)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_session ON memories(session_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)')
        
        # 创建关联表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_associations (
                memory_id TEXT NOT NULL,
                associated_id TEXT NOT NULL,
                association_strength REAL DEFAULT 1.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (memory_id, associated_id),
                FOREIGN KEY (memory_id) REFERENCES memories(id),
                FOREIGN KEY (associated_id) REFERENCES memories(id)
            )
        ''')
        
        # 创建访问日志表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                memory_id TEXT NOT NULL,
                access_time TEXT NOT NULL,
                access_context TEXT,
                relevance_change REAL,
                FOREIGN KEY (memory_id) REFERENCES memories(id)
            )
        ''')
        
        self.conn.commit()
    
    def _init_cache(self):
        """初始化缓存"""
        self.cache = {}  # 内存缓存
        self.cache_size_limit = 1000
        
    def store_memory(self, memory: MemoryRecord, compress: bool = True) -> str:
        """
        存储记忆
        """
        # 生成唯一ID
        if not memory.id:
            content_hash = hashlib.md5(memory.content.encode()).hexdigest()[:16]
            memory.id = f"mem_{content_hash}_{int(datetime.now().timestamp())}"
        
        # 准备数据
        compressed_content = None
        if compress:
            compressed_content = self._compress_content(memory.content)
        
        # 存储到数据库
        self.cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, type, content, compressed_content, timestamp, session_id, 
             importance, associations, tags, metadata, access_count, 
             last_accessed, relevance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.type.value,
            memory.content if not compress else "",
            compressed_content,
            memory.timestamp.isoformat(),
            memory.session_id,
            memory.importance.value,
            json.dumps(memory.associations),
            json.dumps(memory.tags),
            json.dumps(memory.metadata),
            memory.access_count,
            memory.last_accessed.isoformat(),
            memory.relevance_score
        ))
        
        # 存储关联
        for assoc_id in memory.associations:
            self.cursor.execute('''
                INSERT OR REPLACE INTO memory_associations 
                (memory_id, associated_id)
                VALUES (?, ?)
            ''', (memory.id, assoc_id))
        
        self.conn.commit()
        
        # 更新缓存
        self.cache[memory.id] = {
            'memory': memory,
            'timestamp': datetime.now()
        }
        
        # 清理缓存
        if len(self.cache) > self.cache_size_limit:
            self._clean_cache()
        
        return memory.id
    
    def retrieve_memory(self, memory_id: str, decompress: bool = True) -> Optional[MemoryRecord]:
        """
        检索记忆
        """
        # 检查缓存
        if memory_id in self.cache:
            cached_data = self.cache[memory_id]
            # 更新访问统计
            self._update_access_stats(memory_id)
            return cached_data['memory']
        
        # 从数据库检索
        self.cursor.execute('''
            SELECT id, type, content, compressed_content, timestamp, session_id,
                   importance, associations, tags, metadata, access_count,
                   last_accessed, relevance_score
            FROM memories
            WHERE id = ?
        ''', (memory_id,))
        
        row = self.cursor.fetchone()
        if not row:
            return None
        
        # 解析数据
        content = row['content']
        if not content and row['compressed_content'] and decompress:
            content = self._decompress_content(row['compressed_content'])
        
        memory = MemoryRecord(
            id=row['id'],
            type=MemoryType(row['type']),
            content=content,
            timestamp=datetime.fromisoformat(row['timestamp']),
            session_id=row['session_id'],
            importance=ImportanceLevel(row['importance']),
            associations=json.loads(row['associations'] or '[]'),
            tags=json.loads(row['tags'] or '[]'),
            metadata=json.loads(row['metadata'] or '{}'),
            access_count=row['access_count'],
            last_accessed=datetime.fromisoformat(row['last_accessed']),
            relevance_score=row['relevance_score']
        )
        
        # 更新缓存
        self.cache[memory_id] = {
            'memory': memory,
            'timestamp': datetime.now()
        }
        
        # 更新访问统计
        self._update_access_stats(memory_id)
        
        return memory
    
    def search_memories(self, 
                       query: str = None,
                       memory_type: MemoryType = None,
                       tags: List[str] = None,
                       min_importance: int = None,
                       date_range: Tuple[datetime, datetime] = None,
                       limit: int = 100,
                       offset: int = 0) -> List[MemoryRecord]:
        """
        搜索记忆
        """
        # 构建查询条件
        conditions = []
        params = []
        
        if query:
            conditions.append("(content LIKE ? OR tags LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        if memory_type:
            conditions.append("type = ?")
            params.append(memory_type.value)
        
        if tags:
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
            if tag_conditions:
                conditions.append(f"({' OR '.join(tag_conditions)})")
        
        if min_importance is not None:
            conditions.append("importance >= ?")
            params.append(min_importance)
        
        if date_range:
            start_date, end_date = date_range
            conditions.append("timestamp BETWEEN ? AND ?")
            params.extend([start_date.isoformat(), end_date.isoformat()])
        
        # 执行查询
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        self.cursor.execute(f'''
            SELECT id, type, content, compressed_content, timestamp, session_id,
                   importance, associations, tags, metadata, access_count,
                   last_accessed, relevance_score
            FROM memories
            WHERE {where_clause}
            ORDER BY relevance_score DESC, importance DESC, timestamp DESC
            LIMIT ? OFFSET ?
        ''', params + [limit, offset])
        
        # 解析结果
        memories = []
        for row in self.cursor.fetchall():
            content = row['content']
            if not content and row['compressed_content']:
                content = self._decompress_content(row['compressed_content'])
            
            memory = MemoryRecord(
                id=row['id'],
                type=MemoryType(row['type']),
                content=content,
                timestamp=datetime.fromisoformat(row['timestamp']),
                session_id=row['session_id'],
                importance=ImportanceLevel(row['importance']),
                associations=json.loads(row['associations'] or '[]'),
                tags=json.loads(row['tags'] or '[]'),
                metadata=json.loads(row['metadata'] or '{}'),
                access_count=row['access_count'],
                last_accessed=datetime.fromisoformat(row['last_accessed']),
                relevance_score=row['relevance_score']
            )
            memories.append(memory)
            
            # 更新访问统计
            self._update_access_stats(row['id'])
        
        return memories
    
    def get_context_memories(self, 
                           current_session_id: str,
                           current_task: str = None,
                           limit: int = 50) -> List[MemoryRecord]:
        """
        获取当前上下文相关记忆
        智能选择最相关的记忆注入上下文
        """
        # 1. 获取最近的重要记忆
        recent_memories = self.search_memories(
            memory_type=None,
            min_importance=ImportanceLevel.MEDIUM.value,
            limit=limit // 2,
            offset=0
        )
        
        # 2. 获取与当前任务相关的记忆
        task_related = []
        if current_task:
            task_related = self.search_memories(
                query=current_task,
                limit=limit // 2,
                offset=0
            )
        
        # 3. 合并并去重
        all_memories = {}
        for mem in recent_memories + task_related:
            if mem.id not in all_memories:
                all_memories[mem.id] = mem
        
        # 4. 按相关性排序
        sorted_memories = sorted(
            all_memories.values(),
            key=lambda m: (
                m.relevance_score * 0.4 +
                m.importance.value * 0.3 +
                (1 if m.session_id == current_session_id else 0) * 0.3
            ),
            reverse=True
        )
        
        return sorted_memories[:limit]
    
    def update_relevance(self, memory_id: str, relevance_score: float):
        """
        更新记忆相关性分数
        """
        self.cursor.execute('''
            UPDATE memories 
            SET relevance_score = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (relevance_score, memory_id))
        
        self.conn.commit()
        
        # 更新缓存
        if memory_id in self.cache:
            self.cache[memory_id]['memory'].relevance_score = relevance_score
    
    def add_association(self, memory_id: str, associated_id: str, strength: float = 1.0):
        """
        添加记忆关联
        """
        self.cursor.execute('''
            INSERT OR REPLACE INTO memory_associations 
            (memory_id, associated_id, association_strength)
            VALUES (?, ?, ?)
        ''', (memory_id, associated_id, strength))
        
        self.conn.commit()
        
        # 更新内存中的记忆对象
        if memory_id in self.cache:
            memory = self.cache[memory_id]['memory']
            if associated_id not in memory.associations:
                memory.associations.append(associated_id)
    
    def get_associated_memories(self, memory_id: str, limit: int = 20) -> List[MemoryRecord]:
        """
        获取关联记忆
        """
        self.cursor.execute('''
            SELECT m.*
            FROM memories m
            JOIN memory_associations ma ON m.id = ma.associated_id
            WHERE ma.memory_id = ?
            ORDER BY ma.association_strength DESC
            LIMIT ?
        ''', (memory_id, limit))
        
        associated = []
        for row in self.cursor.fetchall():
            content = row['content']
            if not content and row['compressed_content']:
                content = self._decompress_content(row['compressed_content'])
            
            memory = MemoryRecord(
                id=row['id'],
                type=MemoryType(row['type']),
                content=content,
                timestamp=datetime.fromisoformat(row['timestamp']),
                session_id=row['session_id'],
                importance=ImportanceLevel(row['importance']),
                associations=json.loads(row['associations'] or '[]'),
                tags=json.loads(row['tags'] or '[]'),
                metadata=json.loads(row['metadata'] or '{}'),
                access_count=row['access_count'],
                last_accessed=datetime.fromisoformat(row['last_accessed']),
                relevance_score=row['relevance_score']
            )
            associated.append(memory)
        
        return associated
    
    def cleanup_old_memories(self, 
                           retention_days: int = 365,
                           min_importance: int = ImportanceLevel.LOW.value):
        """
        清理旧记忆
        保留重要记忆，清理不重要且旧的记忆
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        self.cursor.execute('''
            DELETE FROM memories 
            WHERE timestamp < ? AND importance < ?
        ''', (cutoff_date.isoformat(), min_importance))
        
        deleted_count = self.cursor.rowcount
        
        # 清理关联表
        self.cursor.execute('''
            DELETE FROM memory_associations 
            WHERE memory_id NOT IN (SELECT id FROM memories) 
               OR associated_id NOT IN (SELECT id FROM memories)
        ''')
        
        self.conn.commit()
        
        # 清理缓存
        self._clean_cache()
        
        return deleted_count
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        """
        stats = {}
        
        # 总数统计
        self.cursor.execute('SELECT COUNT(*) as total FROM memories')
        stats['total_memories'] = self.cursor.fetchone()['total']
        
        # 按类型统计
        self.cursor.execute('SELECT type, COUNT(*) as count FROM memories GROUP BY type')
        stats['by_type'] = {row['type']: row['count'] for row in self.cursor.fetchall()}
        
        # 按重要性统计
        self.cursor.execute('SELECT importance, COUNT(*) as count FROM memories GROUP BY importance')
        stats['by_importance'] = {row['importance']: row['count'] for row in self.cursor.fetchall()}
        
        # 存储大小
        self.cursor.execute('SELECT SUM(LENGTH(content) + LENGTH(compressed_content)) as size FROM memories')
        size_row = self.cursor.fetchone()
        stats['total_size_bytes'] = size_row['size'] or 0
        
        # 缓存统计
        stats['cache_size'] = len(self.cache)
        stats['cache_hit_rate'] = self._calculate_cache_hit_rate()
        
        return stats
    
    def export_memories(self, export_path: str, format: str = 'json'):
        """
        导出记忆
        """
        memories = self.search_memories(limit=10000)  # 导出所有记忆
        
        if format == 'json':
            data = [mem.to_dict() for mem in memories]
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format == 'sql':
            # 导出SQL格式
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write('-- Memory Storage Export\n')
                f.write('BEGIN TRANSACTION;\n\n')
                
                for mem in memories:
                    f.write(f"INSERT OR REPLACE INTO memories VALUES (\n")
                    f.write(f" '{mem.id}',\n")
                    f.write(f" '{mem.type.value}',\n")
                    escaped = mem.content.replace("'", "''")
                    f.write(f" '{escaped}',\n")
                    f.write(f" NULL,\n")
                    # \u538b\u7f29\u5185\u5bb9\u4e0d\u5bfc\u51fa
                    f.write(f" '{mem.timestamp.isoformat()}',\n")
                    f.write(f" '{mem.session_id}',\n")
                    f.write(f" {mem.importance.value},\n")
                    f.write(f" '{json.dumps(mem.associations)}',\n")
                    f.write(f" '{json.dumps(mem.tags)}',\n")
                    f.write(f" '{json.dumps(mem.metadata)}',\n")
                    f.write(f" {mem.access_count},\n")
                    f.write(f" '{mem.last_accessed.isoformat()}',\n")
                    f.write(f" {mem.relevance_score}\n")
                

    
    def import_memories(self, import_path: str, format: str = 'json'):
        """
        导入记忆
        """
        if format == 'json':
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for mem_data in data:
                memory = MemoryRecord.from_dict(mem_data)
                self.store_memory(memory)
    
    def _compress_content(self, content: str) -> bytes:
        """压缩内容"""
        return zlib.compress(content.encode('utf-8'), level=9)
    
    def _decompress_content(self, compressed: bytes) -> str:
        """解压缩内容"""
        return zlib.decompress(compressed).decode('utf-8')
    
    def _update_access_stats(self, memory_id: str):
        """更新访问统计"""
        now = datetime.now()
        
        # 更新记忆表的访问统计
        self.cursor.execute('''
            UPDATE memories 
            SET access_count = access_count + 1,
                last_accessed = ?
            WHERE id = ?
        ''', (now.isoformat(), memory_id))
        
        # 记录访问日志
        self.cursor.execute('''
            INSERT INTO access_logs (memory_id, access_time)
            VALUES (?, ?)
        ''', (memory_id, now.isoformat()))
        
        self.conn.commit()
        
        # 更新缓存
        if memory_id in self.cache:
            memory = self.cache[memory_id]['memory']
            memory.access_count += 1
            memory.last_accessed = now
    
    def _clean_cache(self):
        """清理缓存"""
        if len(self.cache) <= self.cache_size_limit:
            return
        
        # 按最后访问时间排序，清理最早的缓存
        cache_items = list(self.cache.items())
        cache_items.sort(key=lambda x: x[1]['timestamp'])
        
        items_to_remove = len(cache_items) - self.cache_size_limit
        for i in range(items_to_remove):
            memory_id, _ = cache_items[i]
            del self.cache[memory_id]
    
    def _calculate_cache_hit_rate(self) -> float:
        """计算缓存命中率（简化版本）"""
        # 这里可以扩展为实际统计
        return 0.0
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# 使用示例
if __name__ == "__main__":
    # 创建存储系统
    storage = MemoryStorage("test_memory.db")
    
    # 创建测试记忆
    test_memory = MemoryRecord(
        id="test_memory_001",
        type=MemoryType.EXPERIENCE,
        content="今天解决了OpenClaw上下文超限问题，实现了智能压缩算法。",
        timestamp=datetime.now(),
        session_id="session_001",
        importance=ImportanceLevel.HIGH,
        tags=["openclaw", "上下文", "优化"],
        metadata={"problem": "context_overflow", "solution": "compression"}
    )
    
    # 存储记忆
    memory_id = storage.store_memory(test_memory)
    print(f"存储记忆: {memory_id}")
    
    # 检索记忆
    retrieved = storage.retrieve_memory(memory_id)
    print(f"检索记忆: {retrieved.content[:50]}...")
    
    # 搜索记忆
    results = storage.search_memories(query="上下文", limit=5)
    print(f"搜索结果数: {len(results)}")
    
    # 获取统计信息
    stats = storage.get_statistics()
    print(f"记忆总数: {stats['total_memories']}")
    
    # 清理
    storage.close()