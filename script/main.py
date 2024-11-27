from DrissionPage import ChromiumPage
import time
import random
import csv
from requests.exceptions import RequestException
import sys
import re

def get_current_page_number(url):
    """从URL中提取页码"""
    match = re.search(r'-(\d+)\.html$', url)
    return int(match.group(1)) if match else 1

def get_page_url(base_url, page_number):
    """生成指定页码的URL"""
    return re.sub(r'-\d+\.html$', f'-{page_number}.html', base_url)

def scrape_page(page, base_url, current_month, start_page=1):
    max_retries = 5
    retry_count = 0
    current_page = start_page
    
    while retry_count < max_retries:
        try:
            # 访问当前页面
            current_url = get_page_url(base_url, current_page)
            print(f"正在抓取 {current_month} 月份第 {current_page} 页")
            page.get(current_url, retry=3, show_errmsg=True, timeout=100)
            
            while True:
                time.sleep(random.uniform(1, 3))
                
                try:
                    # 抓取数据
                    trs = page.ele('tag:tbody').eles('tag:tr')
                    for tr in trs:
                        row = tr.texts()
                        row.append(current_month)
                        data = [row]
                        
                        # 保存数据
                        with open('zizhu.csv', 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerows(data)
                    
                    # 保存当前进度
                    save_progress(current_month, current_page)
                    
                    # 尝试翻页
                    try:
                        page.ele('.lineBlock next').click()
                        current_page += 1
                    except:
                        print(f'月份 {current_month} 抓取完成')
                        # 完成后删除进度文件
                        clear_progress(current_month)
                        return True
                        
                except Exception as e:
                    raise e  # 让外层错误处理来处理
                    
        except Exception as e:
            retry_count += 1
            if '502' in str(e):
                print(f'在第 {current_page} 页遇到502错误,正在进行第{retry_count}次重试...')
                time.sleep(random.uniform(5, 10))  # 增加重试间隔
                continue
            elif retry_count >= max_retries:
                print(f'重试{max_retries}次后仍然失败,记录失败位置: 月份 {current_month}, 页码 {current_page}')
                save_failed_record(current_month, current_page)
                return False
            else:
                print(f'在第 {current_page} 页发生错误: {str(e)}, 正在重试...')
                time.sleep(random.uniform(3, 7))
                continue
    
    return False

def save_progress(month, page):
    """保存抓取进度"""
    with open('scraping_progress.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([month, page])

def load_progress():
    """加载上次的抓取进度"""
    try:
        with open('scraping_progress.csv', 'r') as file:
            reader = csv.reader(file)
            row = next(reader)
            return row[0], int(row[1])
    except:
        return None, None

def clear_progress(month):
    """清除进度文件"""
    try:
        import os
        if os.path.exists('scraping_progress.csv'):
            os.remove('scraping_progress.csv')
    except:
        pass

def save_failed_record(month, page):
    """记录失败的月份和页码"""
    with open('failed_records.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([month, page])

def load_failed_records():
    """加载失败记录"""
    failed_records = {}
    try:
        with open('failed_records.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                failed_records[row[0]] = int(row[1])
    except:
        pass
    return failed_records

def main():
    page = ChromiumPage()
    
    dic = {
        # '燃油车':'https://xl.16888.com/city-2024-09-0-0-0-0-0-1-1.html',
        # '新能源':'https://xl.16888.com/city-2024-09-0-0-0-0-0-6-1.html',
        # '纯电动':'https://xl.16888.com/city-2024-09-0-0-0-0-0-2-1.html',
        # '增程车':'https://xl.16888.com/city-2024-09-0-0-0-0-0-3-1.html',
        # '油电混合':'https://xl.16888.com/city-2024-09-0-0-0-0-0-4-1.html'
        # '202206':'https://xl.16888.com/city-2022-06-0-0-0-0-1-0-1.html',
        # '202207':'https://xl.16888.com/city-2022-07-0-0-0-0-1-0-1.html',
        # '202208':'https://xl.16888.com/city-2022-08-0-0-0-0-1-0-1.html',
        # '202209':'https://xl.16888.com/city-2022-09-0-0-0-0-1-0-1.html',
        # '202210':'https://xl.16888.com/city-2022-10-0-0-0-0-1-0-1.html',
        # '202211':'https://xl.16888.com/city-2022-11-0-0-0-0-1-0-1.html',
        # '202212':'https://xl.16888.com/city-2022-12-0-0-0-0-1-0-1.html',
        # '202301':'https://xl.16888.com/city-2023-01-0-0-0-0-1-0-1.html',
        # '202302':'https://xl.16888.com/city-2023-02-0-0-0-0-1-0-1.html',
        # '202303':'https://xl.16888.com/city-2023-03-0-0-0-0-1-0-1.html',
        # '202304':'https://xl.16888.com/city-2023-04-0-0-0-0-1-0-1.html',
        # '202305':'https://xl.16888.com/city-2023-05-0-0-0-0-1-0-1.html',
        # '202306':'https://xl.16888.com/city-2023-06-0-0-0-0-1-0-1.html',
        # '202307':'https://xl.16888.com/city-2023-07-0-0-0-0-1-0-1.html',
        # '202308':'https://xl.16888.com/city-2023-08-0-0-0-0-1-0-1.html',
        # '202309':'https://xl.16888.com/city-2023-09-0-0-0-0-1-0-1.html',
        '202310':'https://xl.16888.com/city-2023-10-0-0-0-0-1-0-204.html',
        '202311':'https://xl.16888.com/city-2023-11-0-0-0-0-1-0-1.html',
        '202312':'https://xl.16888.com/city-2023-12-0-0-0-0-1-0-1.html',
        '202401':'https://xl.16888.com/city-2024-01-0-0-0-0-1-0-1.html',
        '202402':'https://xl.16888.com/city-2024-02-0-0-0-0-1-0-1.html',
        '202403':'https://xl.16888.com/city-2024-03-0-0-0-0-1-0-1.html',
        '202404':'https://xl.16888.com/city-2024-04-0-0-0-0-1-0-1.html',
        '202405':'https://xl.16888.com/city-2024-05-0-0-0-0-1-0-1.html',
        '202406':'https://xl.16888.com/city-2024-06-0-0-0-0-1-0-1.html',
        '202407':'https://xl.16888.com/city-2024-07-0-0-0-0-1-0-1.html',
        '202408':'https://xl.16888.com/city-2024-08-0-0-0-0-1-0-1.html',
        '202409':'https://xl.16888.com/city-2024-09-0-0-0-0-1-0-1.html'
    }
    
    # 检查是否有未完成的进度
    last_month, last_page = load_progress()
    if last_month and last_month in dic:
        print(f"发现未完成的抓取任务: {last_month} 月份, 第 {last_page} 页")
        success = scrape_page(page, dic[last_month], last_month, last_page)
        if not success:
            print(f"恢复抓取失败: {last_month}")
    
    # 加载失败记录
    failed_records = load_failed_records()
    
    # 处理其他月份
    for month in dic.keys():
        # 跳过已经处理过的月份
        if last_month and month <= last_month:
            continue
            
        # 如果这个月份之前失败过，从失败的页码继续
        start_page = failed_records.get(month, 1)
        print(f"开始抓取 {month} 月份数据, 从第 {start_page} 页开始")
        success = scrape_page(page, dic[month], month, start_page)
        if not success:
            print(f"抓取失败: {month}")
            
    # 输出最终失败月份汇总
    try:
        with open('failed_records.csv', 'r') as file:
            print("\n以下月份需要手动检查:")
            reader = csv.reader(file)
            for row in reader:
                print(f"月份: {row[0]}, 失败页码: {row[1]}")
    except:
        print("没有失败记录")

if __name__ == "__main__":
    main()