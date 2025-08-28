import tkinter as tk
import random
from tkinter import simpledialog, messagebox

# --------- 기본 게임 설정 ----------
weapon_names = [
    "녹슨 검", "철검", "강철검", "강화 철검", "고대검",
    "마검", "화염검", "얼음검", "폭풍검", "천둥검",
    "전설의 검", "신의 검", "신화의 검", "엘프의 검", "드래곤 슬레이어",
    "용의 검", "초월검", "차원의 검", "운명의 검", "우주의 검",
    "시간의 검", "무한의 검", "절대자의 검", "혼돈의 검", "창세의 검",
    "🔥 지존검 🔥", "💥 궁극검 💥", "⚡ 갓검 ⚡", "🌌 멀티버스검 🌌", "💀 울트라 짱짱 센 검 💀"
]
success_rates = [100, 95, 90, 85, 80, 70, 65, 60, 55, 50,
                 50, 45, 40, 35, 30, 30, 25, 20, 15, 10,
                 10, 8, 6, 4, 3, 2, 1.5, 1.2, 1.1, 1]

def upgrade_cost(level):
    return 100 + level * 150

weapon_level = 0
gold = 50000
win_streak = 0  # 도박 연승

# --------- 함수들 ----------

def update_ui():
    weapon_label.config(text=f"🗡️ +{weapon_level} {weapon_names[weapon_level]}")
    gold_label.config(text=f"🪙 골드: {gold}G")
    cost_label.config(text=f"💰 강화 비용: {upgrade_cost(weapon_level)}G")
    rate_label.config(text=f"📈 확률: {success_rates[weapon_level]}%")

def game_over():
    messagebox.showerror("💀 게임 오버", "당신은 골드를 모두 잃고 죽었습니다...")
    enhance_button.config(state=tk.DISABLED)
    gamble_button.config(state=tk.DISABLED)
    sell_button.config(state=tk.DISABLED)
    retry_gamble_button.config(state=tk.DISABLED)

def enhance():
    global weapon_level, gold
    cost = upgrade_cost(weapon_level)

    if gold < cost:
        result_label.config(text="❌ 골드 부족! 강화 실패.")
        return

    gold -= cost
    roll = random.uniform(0, 100)
    success = roll <= success_rates[weapon_level]

    if success:
        weapon_level += 1
        result = "✅ 강화 성공!"
    else:
        if weapon_level >= 25:
            weapon_level = 0
            gold = 500
            result = "💥 검이 폭☆발했다! 모든 것이 사라졌다..."
        elif weapon_level >= 20:
            if random.random() < 0.5:
                weapon_level = 0
                result = "⚠️ 검이 부서졌습니다. +0으로 초기화!"
            else:
                weapon_level = max(weapon_level - 3, 0)
                result = "📉 단계 대폭 하락!"
        elif weapon_level >= 10:
            weapon_level = max(weapon_level - 2, 0)
            result = "📉 단계 하락!"
        elif weapon_level >= 5:
            weapon_level = max(weapon_level - 1, 0)
            result = "📉 약간 하락!"
        else:
            result = "😌 다행히 아무 일도 일어나지 않았습니다."

    update_ui()
    result_label.config(text=result)

    if weapon_level >= 30:
        result_label.config(text="🎉🎉🎉 +30 울트라 짱짱 센 검 완성!!! 🎉🎉🎉")
        disable_buttons()

    if gold <= 0:
        game_over()

def sell_weapon():
    global weapon_level, gold

    if weapon_level <= 3:
        result_label.config(text="🪓 +3 이하 검은 쓰레기입니다. 팔 수 없습니다.")
        return

    sell_price = int((weapon_level ** 2.3) * 100)
    gold += sell_price
    result_label.config(text=f"💰 +{weapon_level} 검 판매! +{sell_price:,}G 획득!")

    weapon_level = 0
    update_ui()

def disable_buttons():
    enhance_button.config(state=tk.DISABLED)
    gamble_button.config(state=tk.DISABLED)
    sell_button.config(state=tk.DISABLED)
    retry_gamble_button.config(state=tk.DISABLED)

# 중독 도박 로직
def gamble():
    global gold, win_streak
    if gold <= 0:
        game_over()
        return

    # 위험도 선택
    choice = simpledialog.askstring("🎰 도박장", "도박 종류를 선택하세요:\n1. 안전 (80% 확률, 1.5배)\n2. 고위험 (40% 확률, 2배)\n입력: 1 or 2")
    if not choice or choice not in ['1', '2']:
        return

    mode = int(choice)
    bet = simpledialog.askinteger("💸 베팅", f"얼마를 걸겠습니까? (1 ~ {gold})", minvalue=1, maxvalue=gold)
    if bet is None:
        return

    if mode == 1:
        win_chance = 0.8
        multiplier = 1.5
    else:
        win_chance = 0.4
        multiplier = 2

    if random.random() < win_chance:
        winnings = int(bet * multiplier)
        gold += winnings
        win_streak += 1
        result_label.config(text=f"🎉 도박 성공! +{winnings}G (연승 {win_streak}회)")
    else:
        gold -= bet
        win_streak = 0
        result_label.config(text=f"💥 도박 실패! -{bet}G")

    update_ui()
    retry_gamble_button.config(state=tk.NORMAL)

    if gold <= 0:
        game_over()

def retry_gamble():
    gamble()

# --------- UI 구성 ----------
root = tk.Tk()
root.title("강화 뇌절 게임 - 중독 도박장 포함")
root.geometry("420x450")
root.resizable(False, False)

weapon_label = tk.Label(root, text="", font=("Arial", 16))
weapon_label.pack(pady=10)

gold_label = tk.Label(root, text="", font=("Arial", 12))
gold_label.pack()

cost_label = tk.Label(root, text="", font=("Arial", 12))
cost_label.pack()

rate_label = tk.Label(root, text="", font=("Arial", 12))
rate_label.pack()

enhance_button = tk.Button(root, text="🔨 강화하기", font=("Arial", 14), command=enhance)
enhance_button.pack(pady=8)

gamble_button = tk.Button(root, text="🎲 도박장 가기", font=("Arial", 14), command=gamble)
gamble_button.pack(pady=5)

retry_gamble_button = tk.Button(root, text="🔁 다시 도박하기", font=("Arial", 12), command=retry_gamble, state=tk.DISABLED)
retry_gamble_button.pack(pady=5)

sell_button = tk.Button(root, text="💰 검 판매하기", font=("Arial", 14), command=sell_weapon)
sell_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
result_label.pack(pady=15)

update_ui()
root.mainloop()
