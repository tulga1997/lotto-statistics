import streamlit as st
import pandas as pd
from itertools import combinations
import random
import matplotlib.pyplot as plt

st.title("🎯 Lotto Хослол Генератор + Статистик Анализ")

uploaded_history = st.file_uploader("📂 Өмнөх тохирлын CSV файл оруулна уу", type="csv")

n_generate = st.number_input("📌 Хэдэн шинэ хослол үүсгэх вэ?", min_value=1, max_value=1000, value=50)

if uploaded_history:
    # Өнгөний бүлэглэл
    color_groups = {
        "yellow": list(range(1, 11)),
        "blue": list(range(11, 21)),
        "red": list(range(21, 31)),
        "black": list(range(31, 41)),
        "green": list(range(41, 46))
    }

    def color_balance(combo):
        counts = {color: 0 for color in color_groups}
        for num in combo:
            for color, group in color_groups.items():
                if num in group:
                    counts[color] += 1
        return counts

    def count_even_odd(combo):
        even = sum(1 for n in combo if n % 2 == 0)
        odd = 6 - even
        return even, odd

    # 1. Түүхэн өгөгдлийг унших
    df = pd.read_csv(uploaded_history, header=None)
    previous_draws = set(tuple(sorted(map(int, row[1:7]))) for row in df.values)
    previous_bonus = set(int(row[7]) for row in df.values if len(row) > 7)

    # 2. Сүүлийн тохирлыг авч, давхардал шалгахын тулд
    last_draw = set(map(int, df.values[-1][1:7]))

    # 3. Шинэ хослол үүсгэх
    numbers = list(range(1, 46))
    all_combos = list(combinations(numbers, 6))
    random.shuffle(all_combos)

    final_results = []
    for combo in all_combos:
        sorted_combo = tuple(sorted(combo))
        if sorted_combo in previous_draws:
            continue
        if any(b in sorted_combo for b in previous_bonus):
            continue
        match_last = len(last_draw.intersection(set(combo)))
        sum_total = sum(combo)
        even, odd = count_even_odd(combo)
        color_counts = color_balance(combo)

        final_results.append({
            "Combo": sorted_combo,
            "Sum": sum_total,
            "Even": even,
            "Odd": odd,
            "Yellow": color_counts["yellow"],
            "Blue": color_counts["blue"],
            "Red": color_counts["red"],
            "Black": color_counts["black"],
            "Green": color_counts["green"],
            "MatchFromLastDraw": match_last
        })
        if len(final_results) >= n_generate:
            break

    result_df = pd.DataFrame(final_results)
    st.success(f"✅ Шинэ {len(result_df)} хослол үүсгэгдлээ!")
    st.dataframe(result_df)

    # 📤 CSV татах
    csv = result_df.to_csv(index=False)
    st.download_button("⬇️ CSV татах", data=csv, file_name="lotto_new_combinations.csv", mime="text/csv")

    # 📊 Өнгөний бүлгийн дундаж статистик
    st.subheader("📊 Өнгөний бүлгийн дундаж тархалт")
    color_avg = result_df[["Yellow", "Blue", "Red", "Black", "Green"]].mean()
    fig, ax = plt.subplots()
    ax.bar(color_avg.index, color_avg.values)
    ax.set_ylabel("Дундаж тоо (per хослол)")
    ax.set_title("Өнгөний бүлэг дундаж тархалт")
    st.pyplot(fig)
