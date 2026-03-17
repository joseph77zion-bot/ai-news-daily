import os
import json
from datetime import datetime

def main():
    # 3月17日の最新ニュースデータ
    data = {
        "date": "2026年3月17日",
        "hero_stat_1_num": "4.45兆ドル",
        "hero_stat_1_label": "NVIDIA 時価総額",
        "hero_stat_2_num": "1560億元",
        "hero_stat_2_label": "Alibaba Cloud 売上予測",
        "hero_stat_3_num": "183.22",
        "hero_stat_3_label": "NVIDIA (NVDA)",
        "investment_news": "米株式市場、AI関連株主導で続伸。MetaやNVIDIAなどのAI関連株が買われ、主要指数が上昇。",
        "enterprise_news": "Dell、AI導入による10%の人員削減を発表。Alibaba Cloudは2026年度売上230億ドルの強気予測。",
        "tech_news": "NVIDIA、AIエージェント基盤「NemoClaw」発表。次世代AIチップ「Groq 3」も衝撃の推論速度を達成。",
        "labor_news": "Dellの大規模削減は、ホワイトカラー職種におけるAI置換の現実味を市場に突きつけました。",
        "security_news": "WWTとCrowdStrike、「Securing AI Lab」を開設。AIモデルへの攻撃やデータ漏洩を防ぐための専用ラボ。",
        "regional_news": "日本：スタートアップ政策推進分科会開催。中国：テックセクターへの融資拡大。"
    }

    # テンプレートの読み込み
    template_path = "template_original.html"
    if not os.path.exists(template_path):
        template_path = "index.html"
    
    with open(template_path, "r", encoding="utf-8") as f:
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
    output_path = "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)
        
    print(f"Dashboard updated successfully to {output_path}")

if __name__ == "__main__":
    main()
