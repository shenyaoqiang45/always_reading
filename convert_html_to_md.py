#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML to Markdown Converter
将always_reading仓库中的HTML文件批量转换为Markdown格式
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text


def convert_html_to_markdown(html_file_path):
    """
    将单个HTML文件转换为Markdown格式
    
    Args:
        html_file_path: HTML文件路径
        
    Returns:
        转换后的Markdown内容
    """
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除script和style标签
    for script in soup(['script', 'style']):
        script.decompose()
    
    # 提取标题
    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text().strip()
    
    # 提取主要内容
    # 尝试找到content或container类的div
    content_div = soup.find('div', class_=['content', 'container'])
    if content_div:
        content_html = str(content_div)
    else:
        # 如果没有找到特定的content div,使用body
        body = soup.find('body')
        if body:
            content_html = str(body)
        else:
            content_html = str(soup)
    
    # 使用html2text转换
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # 不自动换行
    h.unicode_snob = True  # 使用Unicode字符
    h.skip_internal_links = False
    
    markdown_content = h.handle(content_html)
    
    # 清理多余的空行(超过2个连续空行的压缩为2个)
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    # 如果有标题,添加到开头
    if title and not markdown_content.startswith('#'):
        markdown_content = f"# {title}\n\n{markdown_content}"
    
    return markdown_content.strip() + "\n"


def batch_convert(root_dir):
    """
    批量转换目录下所有HTML文件
    
    Args:
        root_dir: 根目录路径
    """
    root_path = Path(root_dir)
    html_files = list(root_path.rglob('*.html'))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    success_count = 0
    fail_count = 0
    
    for html_file in html_files:
        try:
            # 生成对应的MD文件路径
            md_file = html_file.with_suffix('.md')
            
            # 转换
            markdown_content = convert_html_to_markdown(html_file)
            
            # 写入MD文件
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            success_count += 1
            print(f"✓ 转换成功: {html_file.relative_to(root_path)} -> {md_file.name}")
            
        except Exception as e:
            fail_count += 1
            print(f"✗ 转换失败: {html_file.relative_to(root_path)}")
            print(f"  错误: {str(e)}")
    
    print(f"\n转换完成!")
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")


if __name__ == '__main__':
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    
    # 执行批量转换
    batch_convert(script_dir)
