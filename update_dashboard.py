import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import yfinance as yf

def fetch_latest_ai_news():
    url = "https://www.artificialintelligence-news.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Herring/90.1.1161.2"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.content, "html.parser")
        
        news_items = []
        # サイトの構造に合わせてセレクタを調整
        # より汎用的なセレクタを使用し、複数のニュースソースに対応できるようにする
        # ここでは一例として、主要なニュースサイトの構造を想定
        for article in soup.select("div.entry-content-wrapper article.entry-card"): # 適切なセレクタに修正
            title_element = article.select_one("h3.entry-title a") # 適切なセレクタに修正
            summary_element = article.select_one("div.entry-content p") # 適切なセレクタに修正
            
            if title_element and summary_element:
                title = title_element.text.strip()
                summary = summary_element.text.strip()
                news_items.append({"title": title, "description": summary, "tags": ["AI", "最新"]})
                if len(news_items) >= 5: # 5件取得したら終了
                    break
        return news_items
    except requests.exceptions.RequestException as e:
        print(f"ニュース取得エラー: {e}")
        return []

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="7d")
        if not hist.empty:
            latest_close = hist["Close"].iloc[-1]
            previous_close = hist["Close"].iloc[-2]
            change = (latest_close - previous_close) / previous_close * 100
            change_class = "up" if change > 0 else "down"
            change_icon = "▲" if change > 0 else "▼"
            return {"num": f"{latest_close:.2f}", "label": f"{ticker}", "change_class": change_class, "change_icon": change_icon, "change_value": f"{abs(change):.2f}%", "history": hist["Close"].tolist()}
        return None
    except Exception as e:
        print(f"{ticker}の株価取得エラー: {e}")
        return None

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
    from datetime import timedelta, timezone
    jst = timezone(timedelta(hours=9))
    current_date = datetime.now(jst).strftime("%Y年%m月%d日")

    # リアルタイムデータの取得
    latest_news = fetch_latest_ai_news()
    nvidia_stock = fetch_stock_data("NVDA")
    adobe_stock = fetch_stock_data("ADBE")
    furukawa_stock = fetch_stock_data("5801.T")

    # news_data.jsonの構造を動的に生成
    data = {
        "date": current_date,
        "hero_stats": {
            "stat1": {"num": "N/A", "label": "NVIDIA 時価総額"},
            "stat2": {"num": "N/A", "label": "Alibaba Cloud 売上予測"},
            "stat3": {"num": "N/A", "label": "NVIDIA (NVDA)"}
        },
        "overview": [],
        "metrics": [],
        "risks": [
            {"label": "軍事利用の倫理的懸念", "pct": 85, "color": "#f59e0b"},
            {"label": "データセンターへのサイバー攻撃", "pct": 72, "color": "#f59e0b"},
            {"label": "AIインフラの供給不足", "pct": 60, "color": "#ef4444"},
            {"label": "AIモデルの透明性不足", "pct": 55, "color": "#f59e0b"}
        ],
        "categories": {
            "investment": [],
            "enterprise": [],
            "model": [],
            "labor": [],
            "security": [],
            "regional": []
        },
        "charts": {
            "stock_price": {"labels": [], "nvidia_data": [], "adobe_data": [], "furukawa_data": []},
            "ai_strategy": {"labels": ["研究開発", "M&A", "人材育成", "インフラ投資"], "values": [42, 18, 22, 18]},
            "chip_performance": {
                "labels": ["推論速度", "学習効率", "電力効率", "柔軟性", "コスト効率"],
                "datasets": [
                    {"label": "Groq 3 (推測)", "data": [9.2, 7.5, 8.2, 8.0, 7.2]},
                    {"label": "NVIDIA B100 (公称)", "data": [8.5, 9.2, 9.0, 7.5, 6.5]}
                ]
            },
            "job_impact": {"labels": ["代替される", "補完・強化される", "影響なし", "新たな職が創出"], "values": [22, 48, 14, 16]},
            "cyber_attacks": {"labels": ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1"], "values": [280, 400, 550, 750, 1000]},
            "regional_investment": {"labels": ["北米", "アジア", "欧州", "その他"], "values": [125, 95, 68, 32]}
        }
    }

    # ヒーロースタッツの更新
    if nvidia_stock:
        data["hero_stats"]["stat1"]["num"] = f"{nvidia_stock['num']}ドル"
        data["hero_stats"]["stat3"] = nvidia_stock

    # 概要ニュースの更新
    if latest_news:
        data["overview"] = latest_news[:2] # 上位2件を概要に
        # 残りのニュースをカテゴリに振り分ける（簡易的な例）
        for news in latest_news[2:]:
            if "NVIDIA" in news['title'] or "チップ" in news['title']:
                data["categories"]["model"].append(news)
            elif "企業" in news['title'] or "戦略" in news['title']:
                data["categories"]["enterprise"].append(news)
            else:
                data["categories"]["investment"].append(news)

    # 主要指標の更新
    if nvidia_stock: data["metrics"].append(nvidia_stock)
    if adobe_stock: data["metrics"].append(adobe_stock)
    if furukawa_stock: data["metrics"].append(furukawa_stock)

    # 株価チャートデータの更新
    if nvidia_stock and adobe_stock and furukawa_stock:
        data["charts"]["stock_price"]["labels"] = [f"3/{i}" for i in range(datetime.now().day - 6, datetime.now().day + 1)]
        data["charts"]["stock_price"]["nvidia_data"] = nvidia_stock['history'][-7:]
        data["charts"]["stock_price"]["adobe_data"] = adobe_stock['history'][-7:]
        data["charts"]["stock_price"]["furukawa_data"] = furukawa_stock['history'][-7:]

    # news_data.jsonを書き出す
    with open("/home/ubuntu/ai-news-daily-repo/news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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
        
        "overview_card_1_title": data["overview"][0]['title'] if len(data["overview"]) > 0 else "",
        "overview_card_1_source": data["overview"][0]['source'] if len(data["overview"]) > 0 else "",
        "overview_card_1_body": data["overview"][0]['description'] if len(data["overview"]) > 0 else "",
        "overview_card_2_title": data["overview"][1]['title'] if len(data["overview"]) > 1 else "",
        "overview_card_2_source": data["overview"][1]['source'] if len(data["overview"]) > 1 else "",
        "overview_card_2_body": data["overview"][1]['description'] if len(data["overview"]) > 1 else "",
        
        "metric_1_num": data["metrics"][0]['num'] if len(data["metrics"]) > 0 else "N/A",
        "metric_1_label": data["metrics"][0]['label'] if len(data["metrics"]) > 0 else "",
        "metric_1_change_class": data["metrics"][0]['change_class'] if len(data["metrics"]) > 0 else "",
        "metric_1_change_icon": data["metrics"][0]['change_icon'] if len(data["metrics"]) > 0 else "",
        "metric_1_change_value": data["metrics"][0]['change_value'] if len(data["metrics"]) > 0 else "",
        
        "metric_2_num": data["metrics"][1]['num'] if len(data["metrics"]) > 1 else "N/A",
        "metric_2_label": data["metrics"][1]['label'] if len(data["metrics"]) > 1 else "",
        "metric_2_change_class": data["metrics"][1]['change_class'] if len(data["metrics"]) > 1 else "",
        "metric_2_change_icon": data["metrics"][1]['change_icon'] if len(data["metrics"]) > 1 else "",
        "metric_2_change_value": data["metrics"][1]['change_value'] if len(data["metrics"]) > 1 else "",
        
        "metric_3_num": data["metrics"][2]['num'] if len(data["metrics"]) > 2 else "N/A",
        "metric_3_label": data["metrics"][2]['label'] if len(data["metrics"]) > 2 else "",
        "metric_3_change_class": data["metrics"][2]['change_class'] if len(data["metrics"]) > 2 else "",
        "metric_3_change_icon": data["metrics"][2]['change_icon'] if len(data["metrics"]) > 2 else "",
        "metric_3_change_value": data["metrics"][2]['change_value'] if len(data["metrics"]) > 2 else "",
        
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
        f"label: \'{data['charts']['chip_performance']['datasets'][0]['label']}\'"
    )
    template = template.replace(
        "data: [{{groq_data}}]",
        f"data: {json.dumps(data['charts']['chip_performance']['datasets'][0]['data'])}"
    )
    template = template.replace(
        "label: '{{nvidia_chip_label}}'",
        f"label: \'{data['charts']['chip_performance']['datasets'][1]['label']}\'"
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
    with open("/home/ubuntu/ai-news-daily-repo/index.html", "w", encoding="utf-8") as f:
        f.write(template)
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    main()
