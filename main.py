import random
import time

# 단계별 검 이름
weapon_names = [
    "녹슨 검", "철검", "강철검", "강화 철검", "고대검",
    "마검", "화염검", "얼음검", "폭풍검", "천둥검",
    "전설의 검", "신의 검", "신화의 검", "엘프의 검", "드래곤 슬레이어",
    "용의 검", "초월검", "차원의 검", "운명의 검", "우주의 검",
    "시간의 검", "무한의 검", "절대자의 검", "혼돈의 검", "창세의 검",
    "🔥 지존검 🔥", "💥 궁극검 💥", "⚡ 갓검 ⚡", "🌌 멀티버스검 🌌", "💀 울트라 짱짱 센 검 💀"
]

# 강화 확률 테이블
success_rates = [100, 95, 90, 85, 80, 70, 65, 60, 55, 50,
                 50, 45, 40, 35, 30, 30, 25, 20, 15, 10,
                 10, 8, 6, 4, 3, 2, 1.5, 1.2, 1.1, 1]

# 강화 비용
def upgrade_cost(level):
    return 100 + level * 150

# 상태
weapon_level = 0
gold = 50000

def print_weapon():
    print(f"\n🗡️ 현재 검: +{weapon_level} [{weapon_names[weapon_level]}]")
    print(f"🪙 골드: {gold}G")
    print(f"📈 성공 확률: {success_rates[weapon_level]}%")
    print(f"💰 강화 비용: {upgrade_cost(weapon_level)}G")

def enhance():
    global weapon_level, gold
    cost = upgrade_cost(weapon_level)

    if gold < cost:
        print("❌ 골드 부족! 강화 실패.")
        return False

    gold -= cost
    print("🔨 강화 중...", end="")
    time.sleep(1)

    roll = random.uniform(0, 100)
    success = roll <= success_rates[weapon_level]

    if success:
        weapon_level += 1
        print("✅ 강화 성공!")
    else:
        print("❌ 강화 실패!")
        if weapon_level >= 25:
            print("💥 검이 폭☆발했다! 모든 것이 사라졌다...")
            weapon_level = 0
            gold = 500
        elif weapon_level >= 20:
            if random.random() < 0.5:
                print("⚠️ 검이 부서졌습니다. +0으로 초기화!")
                weapon_level = 0
            else:
                weapon_level = max(weapon_level - 3, 0)
                print("📉 단계 대폭 하락!")
        elif weapon_level >= 10:
            weapon_level = max(weapon_level - 2, 0)
            print("📉 단계 하락!")
        elif weapon_level >= 5:
            weapon_level = max(weapon_level - 1, 0)
            print("📉 약간 하락!")
        else:
            print("😌 다행히 아무 일도 일어나지 않았습니다.")
    return True

# 게임 시작
print("💀 [궁극의 검 강화 뇌절 에디션] 💀")
print("목표: +30 울트라 짱짱 센 검 만들기!\n")

while True:
    print_weapon()
    choice = input("강화하시겠습니까? (y/n): ").lower()
    if choice != 'y':
        print("게임 종료.")
        break

    enhanced = enhance()

    if weapon_level >= 30:
        print("🎉🎉🎉 축하합니다!! 당신은 우주의 균형을 깨트렸습니다. +30 울트라 짱짱 센 검 획득!!! 🎉🎉🎉")
        break

    if gold <= 0:
        print("💸 골드가 모두 사라졌습니다. 빈털터리...")
        break
