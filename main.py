import streamlit as st
import random
import time

# --------- 기본 설정 ----------
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

# --------- 게임 함수 ----------
def upgrade_cost(level):
    return 100 + level * 150

def get_weapon_name(level):
    return f"+{level} {weapon_names[level]}"

# --------- 세션 상태 초기화 ----------
if 'gold' not in st.session_state:
    st.session_state.gold = 50000
    st.session_state.inventory = []
    st.session_state.max_slots = 5
    st.session_state.win_streak = 0
    st.session_state.result_msg = ""
    st.session_state.selected_weapon_index = None

# --------- 게임 로직 ----------
def add_weapon():
    if len(st.session_state.inventory) >= st.session_state.max_slots:
        st.session_state.result_msg = "⚠️ 인벤토리가 가득 찼습니다."
        return
    st.session_state.inventory.append(0)
    st.session_state.result_msg = "🆕 +0 검이 추가되었습니다."

def expand_slot():
    cost = (st.session_state.max_slots + 1) * 10000
    if st.session_state.gold < cost:
        st.session_state.result_msg = f"❌ 슬롯 확장에 {cost:,}G 필요"
        return
    st.session_state.gold -= cost
    st.session_state.max_slots += 1
    st.session_state.result_msg = f"📦 슬롯이 {st.session_state.max_slots}개로 확장되었습니다! (-{cost:,}G)"

def enhance():
    if st.session_state.selected_weapon_index is None or not st.session_state.inventory:
        st.session_state.result_msg = "⚠️ 검을 선택하세요."
        return

    level = st.session_state.inventory[st.session_state.selected_weapon_index]
    cost = upgrade_cost(level)

    if st.session_state.gold < cost:
        st.session_state.result_msg = "❌ 골드 부족! 강화 실패."
        return

    st.session_state.gold -= cost
    roll = random.uniform(0, 100)
    success = roll <= success_rates[level]

    if success:
        st.session_state.inventory[st.session_state.selected_weapon_index] += 1
        st.session_state.result_msg = "✅ 강화 성공!"
    else:
        if level >= 25:
            st.session_state.inventory[st.session_state.selected_weapon_index] = 0
            st.session_state.gold = 500
            st.session_state.result_msg = "💥 검이 폭☆발했다! 모든 것이 사라졌다..."
        elif level >= 20:
            st.session_state.inventory[st.session_state.selected_weapon_index] = 0 if random.random() < 0.5 else max(level - 3, 0)
            st.session_state.result_msg = "⚠️ 대실패! 단계 초기화 or 대폭 하락!"
        elif level >= 10:
            st.session_state.inventory[st.session_state.selected_weapon_index] = max(level - 2, 0)
            st.session_state.result_msg = "📉 단계 하락!"
        elif level >= 5:
            st.session_state.inventory[st.session_state.selected_weapon_index] = max(level - 1, 0)
            st.session_state.result_msg = "📉 약간 하락!"
        else:
            st.session_state.result_msg = "😌 아무 일도 일어나지 않았습니다."

def sell_weapon():
    if st.session_state.selected_weapon_index is None or not st.session_state.inventory:
        st.session_state.result_msg = "⚠️ 검을 선택하세요."
        return

    level = st.session_state.inventory[st.session_state.selected_weapon_index]
    if level <= 3:
        st.session_state.result_msg = "🪓 +3 이하 검은 쓰레기입니다. 팔 수 없습니다."
        return

    price = int((level ** 2.3) * 100)
    st.session_state.gold += price
    st.session_state.result_msg = f"💰 {get_weapon_name(level)} 판매! +{price:,}G"

    del st.session_state.inventory[st.session_state.selected_weapon_index]
    st.session_state.selected_weapon_index = None

def gamble_bet(bet, mode):
    if st.session_state.gold < bet:
        st.session_state.result_msg = "❌ 골드 부족! 베팅할 수 없습니다."
        return

    win_chance = 0.8 if mode == '안전' else 0.4
    multiplier = 1.5 if mode == '안전' else 2

    if random.random() < win_chance:
        winnings = int(bet * multiplier)
        st.session_state.gold += winnings
        st.session_state.win_streak += 1
        st.session_state.result_msg = f"🎉 도박 성공! +{winnings:,}G (연승 {st.session_state.win_streak}회)"
    else:
        st.session_state.gold -= bet
        st.session_state.win_streak = 0
        st.session_state.result_msg = f"💥 도박 실패! -{bet:,}G"

# --------- UI 구성 ----------
st.set_page_config(layout="wide")

st.title("강화 지옥 🔥")

# 게임 오버 상태 체크
if st.session_state.gold <= 0:
    st.error("💀 게임 오버: 당신은 골드를 모두 잃고 죽었습니다...")
    if st.button("재시작"):
        st.session_state.clear()
        st.experimental_rerun()
    st.stop()

# 메인 레이아웃: 두 개의 열
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.header("인벤토리 및 강화")
    st.write(f"🪙 **골드:** {st.session_state.gold:,}G")
    st.write(f"🔒 **슬롯:** {len(st.session_state.inventory)}/{st.session_state.max_slots}")

    # 인벤토리 표시
    inventory_options = [get_weapon_name(lvl) for lvl in st.session_state.inventory]
    if not inventory_options:
        st.session_state.selected_weapon_index = None
        st.write("인벤토리에 검이 없습니다. 새 검을 추가하세요!")
    else:
        selected_weapon = st.selectbox(
            "강화할 검을 선택하세요:",
            options=inventory_options,
            index=st.session_state.selected_weapon_index if st.session_state.selected_weapon_index is not None and st.session_state.selected_weapon_index < len(inventory_options) else 0
        )
        if selected_weapon:
            st.session_state.selected_weapon_index = inventory_options.index(selected_weapon)
            level = st.session_state.inventory[st.session_state.selected_weapon_index]
            st.write(f"💰 **강화 비용:** {upgrade_cost(level):,}G")
            st.write(f"📈 **성공 확률:** {success_rates[level]}%")
        
    st.button("🔨 강화하기", on_click=enhance, use_container_width=True)
    st.button("💰 검 판매", on_click=sell_weapon, use_container_width=True)
    st.button("➕ 새 검 추가", on_click=add_weapon, use_container_width=True)
    st.button("📦 슬롯 확장 구매", on_click=expand_slot, use_container_width=True)
    
    st.divider()

    st.subheader("🎲 도박장")
    with st.form("gamble_form"):
        mode = st.radio("도박 종류", ["안전 (80%, 1.5배)", "고위험 (40%, 2배)"])
        bet = st.number_input(f"베팅 금액 (1 ~ {st.session_state.gold:,})", min_value=1, max_value=st.session_state.gold, step=100)
        submitted = st.form_submit_button("베팅하기", use_container_width=True)
        if submitted:
            gamble_bet(bet, mode.split()[0])
            if st.session_state.result_msg.startswith("🎉"):
                st.balloons()
            
    st.info(st.session_state.result_msg)

with right_col:
    st.header("게임 설명")
    game_explanation = """
    🎮 **게임 목표**
    - 검을 강화하여 최고의 무기를 만드세요.
    - 강화 단계가 높아질수록 성공 확률이 낮아지고 강화 비용은 증가합니다.
    - 골드를 모두 잃으면 게임이 종료됩니다.

    ---

    📜 **강화 실패 시 효과**
    - **레벨 0~4:** 아무 일도 일어나지 않습니다.
    - **레벨 5~9:** 단계가 1 하락합니다.
    - **레벨 10~19:** 단계가 2 하락합니다.
    - **레벨 20~24:** 단계가 대폭 하락하거나 (3 하락) 초기화됩니다 (50% 확률).
    - **레벨 25 이상:** 폭☆발하여 골드가 500G으로 초기화되고 검이 사라집니다.

    ---

    💰 **가격 및 확률 정보**
    - **슬롯 확장 비용:** (현재 슬롯 + 1) × 10,000G
    - **검 판매 가격:** 강화 단계에 따라 다름 (+3 이하 검은 판매 불가)
    - **강화 비용:** 100 + 강화 단계 × 150 G
    - **도박장 정보:**
        - **안전 도박:** 성공 확률 80%, 보상 1.5배
        - **고위험 도박:** 성공 확률 40%, 보상 2배
    """
    st.markdown(game_explanation)
