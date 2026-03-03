#!/usr/bin/env python3
"""
按拍摄时间分组建军照片的脚本
用途：读取照片EXIF信息，按日期分组整理
作者：建国
创建时间：2026-03-03
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ExifTags
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("警告: PIL/Pillow 未安装，将使用文件修改时间")
    print("安装方法: pip3 install Pillow")

# 配置
SOURCE_DIR = Path("/Users/tongxiaotong/littleCat/pic")
OUTPUT_BASE = Path("/Users/tongxiaotong/littleCat/pic_grouped")

def get_exif_date(image_path):
    """从EXIF中获取拍摄日期"""
    if not PILLOW_AVAILABLE:
        return None

    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data is None:
            return None

        # 查找拍摄日期标签
        for tag, value in exif_data.items():
            if tag in ExifTags.TAGS:
                tag_name = ExifTags.TAGS[tag]
                if tag_name in ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']:
                    # EXIF日期格式: "2025:08:01 12:34:56"
                    try:
                        dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        return dt
                    except (ValueError, TypeError):
                        continue

        return None
    except Exception as e:
        # print(f"读取 {image_path} EXIF失败: {e}")
        return None

def get_file_modification_date(image_path):
    """获取文件修改时间（备用方案）"""
    timestamp = os.path.getmtime(image_path)
    return datetime.fromtimestamp(timestamp)

def main():
    print("=== 开始按拍摄时间分组照片 ===")

    # 创建输出目录
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    # 统计
    total_files = 0
    grouped_files = 0
    skipped_files = 0

    # 支持的图片格式
    extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG'}

    # 按月统计
    monthly_stats = {}

    print(f"\n扫描目录: {SOURCE_DIR}")

    for image_file in SOURCE_DIR.iterdir():
        # 跳过非图片文件
        if image_file.suffix not in extensions:
            continue

        total_files += 1

        # 尝试从EXIF获取拍摄日期
        exif_date = get_exif_date(image_file)

        if exif_date:
            date = exif_date
            date_source = "EXIF"
        else:
            # 使用文件修改时间
            date = get_file_modification_date(image_file)
            date_source = "文件时间"

        # 按年月分组
        year_month = date.strftime("%Y-%m")
        day = date.strftime("%Y-%m-%d")

        # 创建目录
        month_dir = OUTPUT_BASE / year_month
        day_dir = month_dir / day
        day_dir.mkdir(parents=True, exist_ok=True)

        # 复制文件
        dest_file = day_dir / image_file.name
        shutil.copy2(image_file, dest_file)

        grouped_files += 1

        # 统计
        if year_month not in monthly_stats:
            monthly_stats[year_month] = 0
        monthly_stats[year_month] += 1

        # 每50个文件输出一次进度
        if total_files % 50 == 0:
            print(f"已处理 {total_files} 个文件...")

    # 输出统计
    print("\n=== 分组完成 ===")
    print(f"总文件数: {total_files}")
    print(f"成功分组: {grouped_files}")
    print(f"跳过文件: {skipped_files}")

    print("\n按月份统计:")
    for month in sorted(monthly_stats.keys()):
        count = monthly_stats[month]
        print(f"  {month}: {count} 张")

    print(f"\n照片已分组到: {OUTPUT_BASE}")

if __name__ == "__main__":
    main()
