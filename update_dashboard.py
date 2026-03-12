import os
import json
import re
from datetime import datetime

def create_news_item_html(news_list):
    html_output = ""
    for i, news in enumerate(news_list):
        tags_html = "".join([f'<span class="news-badge bg-blue-100 text-blue-800">{tag}</span>' for tag in news.get("tags", [])])
        html_output += f"""
        <div class="news-item">
          <div class="news-num">{i + 1}</div>
          <div class="news-content">
            <div class="news-title">{news["title"]}</div>
            <div class="news-desc">{news["description"]}</div>
            <div class="news-meta">
              {tags_html}
            </div>
          </div>
        </div>"""
    return html_output

def main():
    # データの読み込み
    with open("/home/ubuntu/ai-news-daily-repo/news_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # テンプレートの読み込み
    with open("/home/ubuntu/ai-news-daily-repo/template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 置換用辞書の作成
    replacements = {
        "date": data["date"],
        "hero_stat_1_num": data["hero_stats"]["stat1"]["num"],
        "hero_stat_1_label": data["hero_stats"]["stat1"]["label"],
        "hero_stat_2_num": data["hero_stats"]["stat2"]["num"],
        "hero_stat_2_label": data["hero_stats"]["stat2"]["label"],
        "hero_stat_3_num": data["hero_stats"]["stat3"]["num"],
        "hero_stat_3_label": data["hero_stats"]["stat3"]["label"],
        
        "overview_card_1_title": data["overview"][0]["title"],
        "overview_card_1_source": data["overview"][0]["source"],
        "overview_card_1_body": data["overview"][0]["body"],
        "overview_card_2_title": data["overview"][1]["title"],
        "overview_card_2_source": data["overview"][1]["source"],
        "overview_card_2_body": data["overview"][1]["body"],
        
        "metric_1_num": data["metrics"][0]["num"],
        "metric_1_label": data["metrics"][0]["label"],
        "metric_1_change_class": data["metrics"][0]["change_class"],
        "metric_1_change_icon": data["metrics"][0]["change_icon"],
        "metric_1_change_value": data["metrics"][0]["change_value"],
        
        "metric_2_num": data["metrics"][1]["num"],
        "metric_2_label": data["metrics"][1]["label"],
        "metric_2_change_class": data["metrics"][1]["change_class"],
        "metric_2_change_icon": data["metrics"][1]["change_icon"],
        "metric_2_change_value": data["metrics"][1]["change_value"],
        
        "metric_3_num": data["metrics"][2]["num"],
        "metric_3_label": data["metrics"][2]["label"],
        "metric_3_change_class": data["metrics"][2]["change_class"],
        "metric_3_change_icon": data["metrics"][2]["change_icon"],
        "metric_3_change_value": data["metrics"][2]["change_value"],
        
        "risk_1_pct": str(data["risks"][0]["pct"]),
        "risk_1_color": data["risks"][0]["color"],
        "risk_2_pct": str(data["risks"][1]["pct"]),
        "risk_2_color": data["risks"][1]["color"],
        "risk_3_pct": str(data["risks"][2]["pct"]),
        "risk_3_color": data["risks"][2]["color"],
        "risk_4_pct": str(data["risks"][3]["pct"]),
        "risk_4_color": data["risks"][3]["color"],
        
        "investment_news": create_news_item_html(data["categories"]["investment"]),
        "model_news": create_news_item_html(data["categories"]["model"]),
        "labor_news": create_news_item_html(data["categories"]["labor"]),
        "security_news": create_news_item_html(data["categories"]["security"]),
        "regional_news": create_news_item_html(data["categories"]["regional"])
    }

    # テキスト置換の実行
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    # Chart.js データの置換 (正規表現の代わりに文字列置換を使用)
    
    # 市場規模
    template = template.replace(
        "labels: ['2024', '2025', '2026', '2027', '2028', '2029', '2030']",
        f"labels: {json.dumps(data['charts']['market_size']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [0.5, 0.8, 1.3, 2.0, 3.2, 5.0, 8.9]",
        f"data: {json.dumps(data['charts']['market_size']['values'])}"
    )
    
    # 投資比率
    template = template.replace(
        "labels: ['Microsoft', 'Google', 'Amazon', 'NVIDIA', 'その他']",
        f"labels: {json.dumps(data['charts']['investment_ratio']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [30, 25, 20, 15, 10]",
        f"data: {json.dumps(data['charts']['investment_ratio']['values'])}"
    )
    
    # LLM性能 (Radar Chart)
    # GPT-5.4 -> GPT-5
    template = template.replace(
        "label: 'GPT-5.4',\n              data: [90, 85, 92, 88, 75, 70]",
        f"label: '{data['charts']['llm_performance']['datasets'][0]['label']}',\n              data: {json.dumps(data['charts']['llm_performance']['datasets'][0]['data'])}"
    )
    # Claude Opus 4.6 -> Claude 4.5
    template = template.replace(
        "label: 'Claude Opus 4.6',\n              data: [88, 80, 90, 95, 80, 72]",
        f"label: '{data['charts']['llm_performance']['datasets'][1]['label']}',\n              data: {json.dumps(data['charts']['llm_performance']['datasets'][1]['data'])}"
    )
    # Gemini 3.1 -> Gemini 2.5
    template = template.replace(
        "label: 'Gemini 3.1',\n              data: [92, 90, 88, 85, 90, 80]",
        f"label: '{data['charts']['llm_performance']['datasets'][2]['label']}',\n              data: {json.dumps(data['charts']['llm_performance']['datasets'][2]['data'])}"
    )
    
    # 職務影響
    template = template.replace(
        "data: [97, 133, 85]",
        f"data: {json.dumps(data['charts']['job_impact']['values'])}"
    )
    
    # サイバー攻撃
    template = template.replace(
        "labels: ['2023Q1', '2023Q2', '2023Q3', '2023Q4', '2024Q1', '2024Q2', '2024Q3', '2024Q4', '2025Q1', '2025Q2', '2025Q3', '2025Q4', '2026Q1']",
        f"labels: {json.dumps(data['charts']['cyber_attacks']['labels'])}"
    )
    template = template.replace(
        "data: [10, 15, 25, 40, 60, 90, 130, 190, 280, 400, 550, 750, 1000]",
        f"data: {json.dumps(data['charts']['cyber_attacks']['values'])}"
    )
    
    # 地域別投資
    template = template.replace(
        "data: [120, 70, 90, 30]",
        f"data: {json.dumps(data['charts']['regional_investment']['values'])}"
    )

    # 結果の保存
    with open("/home/ubuntu/ai_news_daily/index.html", "w", encoding="utf-8") as f:
        f.write(template)
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    main()
