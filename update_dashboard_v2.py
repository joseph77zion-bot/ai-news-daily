import os
import json

def main():
    # データの読み込み
    with open("/home/ubuntu/ai-news-daily-repo/news_data_20260314.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # テンプレートの読み込み（元のデザインを保持）
    with open("/home/ubuntu/ai-news-daily-repo/template_original.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 置換用辞書の作成
    replacements = {
        "date": data["date"],
        "hero_stat_1_num": data["hero_stat_1_num"],
        "hero_stat_1_label": data["hero_stat_1_label"],
        "hero_stat_2_num": data["hero_stat_2_num"],
        "hero_stat_2_label": data["hero_stat_2_label"],
        "hero_stat_3_num": data["hero_stat_3_num"],
        "hero_stat_3_label": data["hero_stat_3_label"],
        "investment_news": data["investment_news"],
        "enterprise_news": data["enterprise_news"],
        "tech_news": data["tech_news"],
        "labor_news": data["labor_news"],
        "security_news": data["security_news"],
        "regional_news": data["regional_news"]
    }

    # テキスト置換の実行
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    # 結果の保存
    output_path = "/home/ubuntu/ai_news_daily/index.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)
    
    # リポジトリ側にも保存
    repo_output_path = "/home/ubuntu/ai-news-daily-repo/index.html"
    with open(repo_output_path, "w", encoding="utf-8") as f:
        f.write(template)
        
    print(f"Dashboard updated successfully to {output_path}")

if __name__ == "__main__":
    main()
