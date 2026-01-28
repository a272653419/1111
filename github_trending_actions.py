# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
import os
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN', '')
PUSHPLUS_URL = 'http://www.pushplus.plus/send'
GITHUB_API_URL = 'https://api.github.com/search/repositories'
def get_github_trending():
    try:
        query = 'stars:>10 created:>=' + (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params = {'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': 10}
        response = requests.get(GITHUB_API_URL, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        return [{'name': item['full_name'], 'url': item['html_url'], 'desc': item['description'] or '暂无', 'lang': item['language'] or '未知', 'stars': item['stargazers_count'], 'forks': item['forks_count']} for item in response.json().get('items', [])]
    except:
        return []
def format_msg(repos):
    if not repos: return "暂无数据"
    msg = f"🚀 {datetime.now().strftime('%Y年%m月%d日')} GitHub热门\n" + "="*50 + "\n\n"
    for i, r in enumerate(repos, 1):
        emoji = '🥇' if i==1 else '🥈' if i==2 else '🥉' if i==3 else '🔹'
        msg += f"{emoji} <b>{r['name']}</b>\n   📝 {r['desc'][:80]}\n   💻 {r['lang']} | ⭐ {r['stars']} | 🍴 {r['forks']}\n   🔗 <a href=\"{r['url']}\">{r['url']}</a>\n\n"
    return msg
def main():
    print("开始获取...")
    repos = get_github_trending()
    if not repos: return print("未获取到数据")
    print(f"获取到{len(repos)}个")
    if PUSHPLUS_TOKEN:
        requests.post(PUSHPLUS_URL, json={'token': PUSHPLUS_TOKEN, 'title': f"🚀 GitHub今日热门", 'content': format_msg(repos), 'template': 'html'}, timeout=10)
        print("推送成功")
if __name__ == '__main__':
    main()
