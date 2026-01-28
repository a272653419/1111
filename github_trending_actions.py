# -*- coding: utf-8 -*-
"""
GitHub热门项目推送脚本（改进版）
包含详细简介和项目评价
"""
import requests
from datetime import datetime, timedelta
import os
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN', '')
PUSHPLUS_URL = 'http://www.pushplus.plus/send'
GITHUB_API_URL = 'https://api.github.com/search/repositories'
def get_evaluation(stars, language):
    """根据star数和语言给出评价"""
    if stars >= 10000:
        level = "🔥 爆火项目"
    elif stars >= 5000:
        level = "⭐ 热门项目"
    elif stars >= 1000:
        level = "📈 高质量项目"
    elif stars >= 500:
        level = "💎 值得关注"
    else:
        level = "🌟 潜力项目"
    
    return level
def get_language_icon(language):
    """为不同语言添加图标"""
    icons = {
        'Python': '🐍',
        'JavaScript': '⚡',
        'TypeScript': '📘',
        'Java': '☕',
        'Go': '🐹',
        'Rust': '🦀',
        'C++': '⚙️',
        'HTML': '🌐',
        'CSS': '🎨',
        'PHP': '🐘',
        'Ruby': '💎',
        'Swift': '🍎',
        'Kotlin': '🤖',
    }
    return icons.get(language, '💻')
def get_github_trending():
    """获取GitHub热门项目"""
    try:
        query = 'stars:>10 created:>=' + (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.github.v3+json',
        }
        
        response = requests.get(GITHUB_API_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        items = response.json().get('items', [])
        
        repos = []
        for item in items:
            stars = item['stargazers_count']
            language = item['language'] or '未知'
            
            repo = {
                'name': item['full_name'],
                'url': item['html_url'],
                'description': item['description'] or '暂无描述，点击查看详情',
                'language': language,
                'language_icon': get_language_icon(language),
                'stars': stars,
                'forks': item['forks_count'],
                'evaluation': get_evaluation(stars, language),
                'issues': item.get('open_issues_count', 0),
                'updated': item.get('updated_at', ''),
            }
            repos.append(repo)
        
        return repos
        
    except Exception as e:
        print(f"获取失败: {e}")
        return []
def format_message(repos):
    """格式化消息"""
    if not repos:
        return "🔍 今日暂无新发布的热门项目数据"
    
    message = f"""
🚀 {datetime.now().strftime('%Y年%m月%d日')} GitHub 热门项目推荐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for i, repo in enumerate(repos, 1):
        # 排名图标
        rank_icons = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        rank = rank_icons[i-1] if i <= 10 else f'{i}️⃣'
        
        message += f"""
{rank} <b>{repo['name']}</b>
   {repo['evaluation']}
   📝 <b>项目简介：</b>
   {repo['description'][:150]}{'...' if len(repo['description']) > 150 else ''}
   💻 <b>开发语言：</b>{repo['language_icon']} {repo['language']}
   ⭐ <b>星标数：</b>{repo['stars']:,}  🍴 <b>Fork：</b>{repo['forks']:,}
   📊 <b>活跃度：</b>{repo['issues']} 个待解决问题
   🔗 <a href="{repo['url']}">点击查看项目详情</a>
"""
    
    message += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 温馨提示：点击项目名称或链接可查看详细信息
📅 数据来源：GitHub API | 时间：{time}
"""
    
    return message
def main():
    """主函数"""
    print("=" * 60)
    print("开始获取GitHub热门项目...")
    print("=" * 60)
    
    if not PUSHPLUS_TOKEN:
        print("✗ 错误: 未设置PUSHPLUS_TOKEN环境变量")
        return
    
    repos = get_github_trending()
    
    if not repos:
        print("✗ 未获取到数据")
        return
    
    print(f"✅ 成功获取 {len(repos)} 个热门项目")
    
    for repo in repos:
        print(f"  - {repo['name']}: {repo['stars']}⭐ | {repo['evaluation']}")
    
    message = format_message(repos)
    
    print("\n正在发送推送...")
    try:
        response = requests.post(
            PUSHPLUS_URL,
            json={
                'token': PUSHPLUS_TOKEN,
                'title': f"🚀 GitHub今日热门推荐 ({datetime.now().strftime('%m/%d')})",
                'content': message,
                'template': 'html'
            },
            timeout=10
        )
        
        result = response.json()
        
        if result.get('code') == 200:
            print("✅ 推送成功！")
            print("\n" + "=" * 60)
            print("✅ 任务完成！")
            print("=" * 60)
        else:
            print(f"✗ 推送失败: {result}")
            print("\n" + "=" * 60)
            print("✗ 任务失败！")
            print("=" * 60)
            
    except Exception as e:
        print(f"✗ 推送异常: {e}")
        print("\n" + "=" * 60)
        print("✗ 任务失败！")
        print("=" * 60)
if __name__ == '__main__':
    main()
