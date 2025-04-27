import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from snownlp import SnowNLP

matplotlib.use('Agg')
matplotlib.rc('font', family='Microsoft JhengHei')

def generate_mood_trend_plot(user_id, user_entries):
    output_dir = "static/moodtrend"
    os.makedirs(output_dir, exist_ok=True)

    # 轉換日期格式並排序
    user_entries["日期"] = pd.to_datetime(user_entries["日期"])
    user_entries = user_entries.sort_values("日期")
    # 轉換心情指數為數字
    user_entries["心情指數"] = pd.to_numeric(user_entries["心情指數"], errors="coerce")
    # 用 snownlp 對心情小語進行情緒分析，映射至 1~10
    user_entries["心情小語分析"] = user_entries["心情小語"].apply(lambda text: SnowNLP(text).sentiments * 9 + 1)
    
    # 計算兩者平均
    avg_recorded = user_entries["心情指數"].mean()
    avg_snownlp = user_entries["心情小語分析"].mean()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x="日期", y="心情指數", data=user_entries, marker="o", label="用戶心情紀錄", color="blue", errorbar=None)
    sns.lineplot(x="日期", y="心情小語分析", data=user_entries, marker="o", label="SnowNLP 心情分析", color="red", errorbar=None)
    plt.axhline(y=avg_recorded, color='orange', linestyle='--', label=f"記錄平均 ({avg_recorded:.2f})")
    plt.axhline(y=avg_snownlp, color='green', linestyle='--', label=f"分析平均 ({avg_snownlp:.2f})")
    plt.xlabel("日期")
    plt.ylabel("心情指數")
    plt.title(f"用戶 {user_id} 的心情趨勢圖")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(1, 10)

    output_path = os.path.join(output_dir, f"mood_trend_{user_id}.png")
    plt.savefig(output_path)
    plt.close()

    return output_path
