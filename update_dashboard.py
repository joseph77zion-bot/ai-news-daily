import os
import json
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

    # テンプレートの読み込み（元のデザインを保持）
    with open("/home/ubuntu/ai-news-daily-repo/template_original.html", "r", encoding="utf-8") as f:
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
        
        "risk_1_label": data["risks"][0]["label"],
        "risk_1_pct": str(data["risks"][0]["pct"]),
        "risk_1_color": data["risks"][0]["color"],
        "risk_2_label": data["risks"][1]["label"],
        "risk_2_pct": str(data["risks"][1]["pct"]),
        "risk_2_color": data["risks"][1]["color"],
        "risk_3_label": data["risks"][2]["label"],
        "risk_3_pct": str(data["risks"][2]["pct"]),
        "risk_3_color": data["risks"][2]["color"],
        "risk_4_label": data["risks"][3]["label"],
        "risk_4_pct": str(data["risks"][3]["pct"]),
        "risk_4_color": data["risks"][3]["color"],
        
        "investment_news": create_news_item_html(data["categories"]["investment"]),
        "enterprise_news": create_news_item_html(data["categories"]["enterprise"]),
        "model_news": create_news_item_html(data["categories"]["model"]),
        "labor_news": create_news_item_html(data["categories"]["labor"]),
        "security_news": create_news_item_html(data["categories"]["security"]),
        "regional_news": create_news_item_html(data["categories"]["regional"])
    }

    # テキスト置換の実行
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    # Chart.js データの置換
    # stockPriceChart
    template = template.replace(
        "labels: [{{stock_price_labels}}]",
        f"labels: {json.dumps(data['charts']['stock_price']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [{{nvidia_stock_data}}]",
        f"data: {json.dumps(data['charts']['stock_price']['nvidia_data'])}"
    )
    template = template.replace(
        "data: [{{adobe_stock_data}}]",
        f"data: {json.dumps(data['charts']['stock_price']['adobe_data'])}"
    )
    template = template.replace(
        "data: [{{furukawa_stock_data}}]",
        f"data: {json.dumps(data['charts']['stock_price']['furukawa_data'])}"
    )

    # aiStrategyChart
    template = template.replace(
        "labels: [{{ai_strategy_labels}}]",
        f"labels: {json.dumps(data['charts']['ai_strategy']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [{{ai_strategy_data}}]",
        f"data: {json.dumps(data['charts']['ai_strategy']['values'])}"
    )

    # chipPerformanceChart
    template = template.replace(
        "labels: [{{chip_performance_labels}}]",
        f"labels: {json.dumps(data['charts']['chip_performance']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "label: '{{groq_label}}'",
        f"label: '{data['charts']['chip_performance']['datasets'][0]['label']}'"
    )
    template = template.replace(
        "data: [{{groq_data}}]",
        f"data: {json.dumps(data['charts']['chip_performance']['datasets'][0]['data'])}"
    )
    template = template.replace(
        "label: '{{nvidia_chip_label}}'",
        f"label: '{data['charts']['chip_performance']['datasets'][1]['label']}'"
    )
    template = template.replace(
        "data: [{{nvidia_chip_data}}]",
        f"data: {json.dumps(data['charts']['chip_performance']['datasets'][1]['data'])}"
    )

    # jobImpactChart
    template = template.replace(
        "labels: [{{job_impact_labels}}]",
        f"labels: {json.dumps(data['charts']['job_impact']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [{{job_impact_data}}]",
        f"data: {json.dumps(data['charts']['job_impact']['values'])}"
    )

    # cyberAttacksChart
    template = template.replace(
        "labels: [{{cyber_attacks_labels}}]",
        f"labels: {json.dumps(data['charts']['cyber_attacks']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [{{cyber_attacks_data}}]",
        f"data: {json.dumps(data['charts']['cyber_attacks']['values'])}"
    )

    # regionalInvestmentChart
    template = template.replace(
        "labels: [{{regional_investment_labels}}]",
        f"labels: {json.dumps(data['charts']['regional_investment']['labels'], ensure_ascii=False)}"
    )
    template = template.replace(
        "data: [{{regional_investment_data}}]",
        f"data: {json.dumps(data['charts']['regional_investment']['values'])}"
    )

    # 結果の保存
    with open("/home/ubuntu/ai_news_daily/index.html", "w", encoding="utf-8") as f:
        f.write(template)
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    main()
