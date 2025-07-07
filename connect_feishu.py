#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格API连接模块
用于获取飞书多维表格中的文章内容
"""

import os
import requests
import json
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeishuAPI:
    """飞书API连接类"""
    
    def __init__(self):
        """初始化飞书API配置"""
        self.app_id = os.getenv('FEISHU_APP_ID')
        self.app_secret = os.getenv('FEISHU_APP_SECRET')
        self.bitable_token = os.getenv('FEISHU_BITABLE_TOKEN')
        self.table_id = os.getenv('FEISHU_TABLE_ID')
        self.access_token = None
        
        # 验证配置
        if not all([self.app_id, self.app_secret, self.bitable_token, self.table_id]):
            raise ValueError("请检查飞书API配置是否完整")
    
    def get_access_token(self) -> str:
        """获取飞书API访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') == 0:
                self.access_token = result.get('tenant_access_token')
                logger.info("成功获取飞书访问令牌")
                return self.access_token
            else:
                logger.error(f"获取访问令牌失败: {result.get('msg')}")
                raise Exception(f"获取访问令牌失败: {result.get('msg')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求访问令牌时发生错误: {str(e)}")
            raise
    
    def get_table_records(self, page_size: int = 100) -> List[Dict]:
        """获取多维表格记录"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.bitable_token}/tables/{self.table_id}/records"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "page_size": page_size
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') == 0:
                records = result.get('data', {}).get('items', [])
                logger.info(f"成功获取 {len(records)} 条记录")
                return records
            else:
                logger.error(f"获取记录失败: {result.get('msg')}")
                raise Exception(f"获取记录失败: {result.get('msg')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求记录时发生错误: {str(e)}")
            raise
    
    def get_article_content(self, record_id: Optional[str] = None) -> Optional[Dict]:
        """
        获取文章内容
        
        Args:
            record_id: 特定记录ID，如果不指定则随机获取一条
            
        Returns:
            包含文章内容的字典，格式为：
            {
                'title': '标题',
                'content': '内容',
                'author': '作者',
                'source': '来源',
                'published': '是否已发布',
                'record_id': '记录ID'
            }
        """
        try:
            records = self.get_table_records()
            
            if not records:
                logger.warning("没有找到任何记录")
                return None
            
            # 如果指定了记录ID，查找特定记录
            if record_id:
                target_record = None
                for record in records:
                    if record.get('record_id') == record_id:
                        target_record = record
                        break
                
                if not target_record:
                    logger.warning(f"未找到记录ID: {record_id}")
                    return None
                
                records = [target_record]
            
            # 过滤未发布的记录
            available_records = []
            for record in records:
                fields = record.get('fields', {})
                # 假设表格字段：标题、内容、作者、来源、已发布
                published = fields.get('已发布', False)
                if not published:  # 只获取未发布的内容
                    available_records.append(record)
            
            if not available_records:
                logger.warning("没有未发布的记录")
                return None
            
            # 随机选择一条记录
            import random
            selected_record = random.choice(available_records)
            fields = selected_record.get('fields', {})
            
            article_data = {
                'title': fields.get('标题', ''),
                'content': fields.get('内容', ''),
                'author': fields.get('作者', ''),
                'source': fields.get('来源', ''),
                'published': fields.get('已发布', False),
                'record_id': selected_record.get('record_id', '')
            }
            
            logger.info(f"成功获取文章: {article_data.get('title', 'Unknown')}")
            return article_data
            
        except Exception as e:
            logger.error(f"获取文章内容时发生错误: {str(e)}")
            return None
    
    def mark_as_published(self, record_id: str) -> bool:
        """标记记录为已发布"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.bitable_token}/tables/{self.table_id}/records/{record_id}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "fields": {
                "已发布": True
            }
        }
        
        try:
            response = requests.put(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') == 0:
                logger.info(f"成功标记记录 {record_id} 为已发布")
                return True
            else:
                logger.error(f"标记记录失败: {result.get('msg')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"标记记录时发生错误: {str(e)}")
            return False


def test_feishu_connection():
    """测试飞书API连接"""
    try:
        feishu = FeishuAPI()
        
        # 测试获取访问令牌
        token = feishu.get_access_token()
        print(f"访问令牌: {token[:20]}...")
        
        # 测试获取记录
        records = feishu.get_table_records()
        print(f"获取到 {len(records)} 条记录")
        
        # 测试获取文章内容
        article = feishu.get_article_content()
        if article:
            print(f"文章标题: {article.get('title')}")
            print(f"文章内容: {article.get('content')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    test_feishu_connection() 