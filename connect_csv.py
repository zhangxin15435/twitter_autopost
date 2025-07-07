#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV文件数据源管理模块 - 立即可用的替代方案
"""

import os
import csv
import logging
from typing import Dict, List, Optional

class CSVDataSource:
    """CSV文件数据源管理类"""
    
    def __init__(self, csv_file_path: str = "content_data.csv"):
        """初始化CSV数据源"""
        self.csv_file_path = csv_file_path
        self.required_columns = ['标题', '内容', '作者', '来源', '已发布']
        
        # 如果CSV文件不存在，创建示例文件
        if not os.path.exists(self.csv_file_path):
            self.create_sample_csv()
        
        logging.info(f"CSV数据源初始化完成: {self.csv_file_path}")
    
    def create_sample_csv(self):
        """创建示例CSV文件"""
        sample_data = [
            ['标题', '内容', '作者', '来源', '已发布'],
            ['AI技术发展趋势', '人工智能正在快速发展，机器学习和深度学习技术日趋成熟。这些技术正在改变我们的工作和生活方式，为各行各业带来新的机遇和挑战。', '技术小编', '科技资讯', '否'],
            ['数据科学入门指南', '数据科学是当今最热门的领域之一。学习数据科学需要掌握统计学、编程和机器学习等多个方面的知识。Python和R是最常用的编程语言。', '数据分析师', '学习资料', '否'],
            ['云计算的未来前景', '云计算技术正在重塑企业的IT架构。随着5G、边缘计算等技术的发展，云计算将变得更加智能和高效，为企业数字化转型提供强大支撑。', '云架构师', '行业分析', '否']
        ]
        
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(sample_data)
        
        logging.info(f"创建示例CSV文件: {self.csv_file_path}")
        print(f"✅ 创建了示例CSV文件: {self.csv_file_path}")
        print(f"   包含 {len(sample_data)-1} 条示例内容")
    
    def read_csv_data(self) -> List[Dict]:
        """读取CSV文件数据"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
                
                # 验证必要的列是否存在
                if data and not all(col in data[0].keys() for col in self.required_columns):
                    missing_cols = [col for col in self.required_columns if col not in data[0].keys()]
                    logging.error(f"CSV文件缺少必要的列: {missing_cols}")
                    return []
                
                return data
                
        except FileNotFoundError:
            logging.error(f"CSV文件不存在: {self.csv_file_path}")
            return []
        except Exception as e:
            logging.error(f"读取CSV文件时发生错误: {str(e)}")
            return []
    
    def get_article_content(self) -> Optional[Dict]:
        """获取未发布的文章内容"""
        try:
            data = self.read_csv_data()
            
            if not data:
                logging.warning("CSV文件中没有数据")
                return None
            
            # 查找未发布的文章
            for i, row in enumerate(data):
                title = row.get('标题', '').strip()
                content = row.get('内容', '').strip()
                
                if not title or not content:
                    continue
                
                published = row.get('已发布', '').strip().lower()
                
                if not published or published in ['false', '否', '0', '']:
                    article = {
                        'title': title,
                        'content': content,
                        'author': row.get('作者', '').strip(),
                        'source': row.get('来源', '').strip(),
                        'published': published,
                        '_row_index': i,
                        '_original_data': row
                    }
                    
                    logging.info(f"找到未发布文章: {title}")
                    return article
            
            logging.info("没有找到未发布的文章")
            return None
            
        except Exception as e:
            logging.error(f"获取文章内容时发生错误: {str(e)}")
            return None
    
    def mark_as_published(self, row_index: int) -> bool:
        """标记文章为已发布"""
        try:
            data = self.read_csv_data()
            
            if row_index >= len(data):
                logging.error(f"行索引超出范围: {row_index}")
                return False
            
            # 更新数据
            data[row_index]['已发布'] = '是'
            
            # 写回CSV文件
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            logging.info(f"成功标记第{row_index+1}行为已发布")
            return True
            
        except Exception as e:
            logging.error(f"标记已发布时发生错误: {str(e)}")
            return False
    
    def add_new_article(self, title: str, content: str, author: str = "", source: str = "") -> bool:
        """添加新文章到CSV文件"""
        try:
            data = self.read_csv_data()
            
            new_article = {
                '标题': title.strip(),
                '内容': content.strip(),
                '作者': author.strip(),
                '来源': source.strip(),
                '已发布': '否'
            }
            
            data.append(new_article)
            
            # 写回CSV文件
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = self.required_columns
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logging.info(f"成功添加新文章: {title}")
            return True
            
        except Exception as e:
            logging.error(f"添加新文章时发生错误: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """获取内容统计信息"""
        try:
            data = self.read_csv_data()
            
            if not data:
                return {'total': 0, 'published': 0, 'unpublished': 0}
            
            total = len(data)
            published = sum(1 for row in data if row.get('已发布', '').strip().lower() in ['true', '是', '1'])
            unpublished = total - published
            
            return {
                'total': total,
                'published': published,
                'unpublished': unpublished
            }
            
        except Exception as e:
            logging.error(f"获取统计信息时发生错误: {str(e)}")
            return {'total': 0, 'published': 0, 'unpublished': 0}

def test_csv_data_source():
    """测试CSV数据源功能"""
    print("🧪 测试CSV数据源功能")
    print("=" * 40)
    
    try:
        # 初始化CSV数据源
        csv_source = CSVDataSource()
        
        # 获取统计信息
        stats = csv_source.get_statistics()
        print(f"📊 内容统计:")
        print(f"   总数: {stats['total']}")
        print(f"   已发布: {stats['published']}")
        print(f"   未发布: {stats['unpublished']}")
        
        # 获取未发布文章
        article = csv_source.get_article_content()
        
        if article:
            print(f"\n📝 找到未发布文章:")
            print(f"   标题: {article['title']}")
            print(f"   内容: {article['content'][:50]}...")
            print(f"   作者: {article['author']}")
            print(f"   来源: {article['source']}")
            print(f"   行索引: {article['_row_index']}")
            
            # 测试标记为已发布（可选）
            # csv_source.mark_as_published(article['_row_index'])
            # print(f"✅ 测试标记为已发布完成")
        else:
            print(f"\n⚠️ 没有找到未发布的文章")
        
        print(f"\n✅ CSV数据源测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_csv_data_source() 