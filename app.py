import streamlit as st
import random
import json

# --- 페이지 설정 ---
st.set_page_config(
    page_title="포켓몬 카드팩 - 태양의 순환",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 카드 데이터베이스 ---
CARD_DATABASE = [
    # C (일반 카드)
    {"id": "cm1", "name": "루나톤 (일반)", "rarity": "C", "type": "🔮 초", "hp": 90, "img": "Screenshot_20261101_182203_NAVER.jpg", "desc": "달빛을 모아 에너지를 발산하는 포켓몬."},
    {"id": "cm2", "name": "솔록 (일반)", "rarity": "C", "type": "🔥 불꽃", "hp": 90, "img": "Screenshot_20261101_182236_NAVER.jpg", "desc": "태양의 열기를 담아 주변을 따뜻하게 만드는 포켓몬."},
    
    # R (레어 카드)
    {"id": "rm1", "name": "블래키", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "Screenshot_20261101_183128_NAVER.jpg", "desc": "달빛을 받으면 온몸의 노란 고리 문양이 빛난다."},
    {"id": "rm2", "name": "불카모스", "rarity": "R", "type": "🔥 불꽃", "hp": 130, "img": "Screenshot_20261101_183155_NAVER.jpg", "desc": "불타는 날개에서 수많은 화염 가루를 흩뿌린다."},
    {"id": "rm3", "name": "루나아라", "rarity": "R", "type": "🔮 초", "hp": 150, "img": "Screenshot_20261101_183235_NAVER.jpg", "desc": "밤하늘의 빛을 흡수하여 날개를 펼치는 전설의 포켓몬."},
    {"id": "rm4", "name": "솔가레오", "rarity": "R", "type": "⚔️ 강철", "hp": 150, "img": "Screenshot_20261101_183241_NAVER.jpg", "desc": "태양의 에너지를 품고 당당하게 달리는 전설의 포켓몬."},

    # RR (더블 레어 카드)
    {"id": "rrm1", "name": "불카모스 V", "rarity": "RR", "type": "🔥 불꽃", "hp": 220, "img": "Screenshot_20261101_183206_NAVER.jpg", "desc": "강렬한 화염의 힘을 두른 강력한 모습의 불카모스 V."},

    # UR (울트라 레어 카드 - 0.1%)
    {"id": "urm1", "name": "솔가레오 V (울트라레어)", "rarity": "UR", "type": "⚔️ 강철", "hp": 240, "img": "Screenshot_20261101_183221_NAVER.jpg", "desc": "태양의 빛을 극한으로 끌어올린 초희귀 솔가레오."},

    # SPECIAL ART (SAR - 특일 카드 - 0.001%)
    {"id": "sm13", "name": "솔록 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "file_00000000ad388206a3a6a269b5b4726d.png", "desc": "상대의 포켓몬 전원에게 각각 10데미지를 준다. (Illus. Siu)"},
    {"id": "sm14", "name": "루나톤 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "Screenshot_20261101_144113_ChatGPT.jpg", "desc": "상대의 배틀 포켓몬을 혼란시킨다. (Illus. Siu)"}
]

# --- 세션 상태 초기화 ---
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "stats" not in st.session_state:
    st.session_state.stats = {"packs": 0, "cards": 0, "special": 0}
if "current_pack" not in st.session_state:
    st.session_state.current_pack = []
if "current_pack_type" not in st.session_state:
    st.session_state.current_pack_type = None
if "flipped_status" not in st.session_state:
    st.session_state.flipped_status = [False, False, False, False, False]
if "opened_boxes" not in st.session_state:
    st.session_state.opened_boxes = [False, False, False]

# --- 가챠 확률 뽑기 로직 ---
def draw_single_card(is_promo=False):
    rand = random.random()
    
    # 프로모 팩일 때 희귀 카드 확률 상승
    special_rate = 0.0001 if is_promo else 0.00001
    ur_rate = 0.005 if is_promo else 0.001
    
    if rand < special_rate:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "SPECIAL"]
    elif rand < ur_rate:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "UR"]
    elif rand < (0.15 if is_promo else 0.075):
        pool = [c for c in CARD_DATABASE if c["rarity"] == "RR"]
    elif rand < (0.50 if is_promo else 0.345):
        pool = [c for c in CARD_DATABASE if c["rarity"] == "R"]
    else:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
    
    if not pool:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
        
    return random.choice(pool)

def open_selected_box(box_index):
    # 90% 확률로 태양의 순환(일반), 10% 확률로 프로모 팩 결정
    rand_pack = random.random()
    is_promo = (rand_pack >= 0.90)
    pack_name = "태양의 순환 프로모 팩" if is_promo else "태양의 순환 팩"
    
    new_cards = []
    has_special = False
    
    st.session_state.stats["packs"] += 1
    st.session_state.opened_boxes[box_index] = True
    st.session_state.current_pack_type = pack_name
    
    for _ in range(5):
        card = draw_single_card(is_promo=is_promo)
        new_cards.append(card)
        st.session_state.stats["cards"] += 1
        st.session_state.inventory[card["id"]] = st.session_state.inventory.get(card["id"], 0) + 1
        
        if card["rarity"] in ["SPECIAL", "UR"]:
            st.session_state.stats["special"] += 1
            has_special = True
            
    st.session_state.current_pack = new_cards
    st.session_state.flipped_status = [False, False, False, False, False]
    return is_promo, has_special

# --- 사이드바 ---
with st.sidebar:
    st.title("☀️ 태양의 순환")
    st.markdown("### 📊 수집 통계")
    st.write(f"📦 개봉한 팩 수: **{st.session_state.stats['packs']}**")
    st.write(f"🃏 전체 보유 카드: **{st.session_state.stats['cards']}**")
    st.write(f"✨ 특일/UR 획득: **{st.session_state.stats['special']}**")
    
    st.divider()
    st.markdown("### 💾 데이터 관리 (Save/Load)")
    save_data = {
        "inventory": st.session_state.inventory,
        "stats": st.session_state.stats
    }
    st.download_button(
        label="💾 JSON 데이터 저장하기",
        data=json.dumps(save_data, ensure_ascii=False, indent=2),
        file_name="pokemon_save.json",
        mime="application/json",
        use_container_width=True
    )
    
    uploaded_file = st.file_uploader("📂 JSON 파일 불러오기", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            st.session_state.inventory = loaded_data.get("inventory", {})
            st.session_state.stats = loaded_data.get("stats", {"packs": 0, "cards": 0, "special": 0})
            st.success("데이터를 성공적으로 불러왔습니다!")
            st.rerun()
        except Exception:
            st.error("파일 형식 오류!")

# --- 메인 화면 ---
st.title("🎴 포켓몬 카드팩 시뮬레이터")
tab1, tab2 = st.tabs(["🛒 상점 및 팩 개봉", "📖 수집 도감"])

with tab1:
    st.subheader("🏪 상점 - 미스터리 박스 3종")
    st.caption("🎁 상자 3개 중 하나를 선택하세요! (90% 일반 팩 / 10% 프로모 팩 등장)")
    
    # 3개 상자 배치
    box_cols = st.columns(3)
    
    for b_idx in range(3):
        with box_cols[b_idx]:
            st.markdown(f"### 📦 상자 #{b_idx + 1}")
            is_opened = st.session_state.opened_boxes[b_idx]
            
            if not is_opened:
                try:
                    st.image("file_0000000056108206b69dcbce0d79c3bb.png", use_container_width=True)
                except:
                    st.info("상자 커버 이미지")
                    
                if st.button(f"🎁 상자 #{b_idx + 1} 열기", key=f"box_btn_{b_idx}", type="primary", use_container_width=True):
                    is_promo, has_sp = open_selected_box(b_idx)
                    if is_promo:
                        st.balloons()
                        st.toast("✨ 당첨! 10% 확률의 프로모 팩을 찾았습니다!", icon="🎉")
                    if has_sp:
                        st.snow()
                    st.rerun()
            else:
                st.success("✅ 이미 개봉한 상자입니다")

    if st.button("🔄 상자 3개 모두 리셋 (새로고침)", use_container_width=True):
        st.session_state.opened_boxes = [False, False, False]
        st.session_state.current_pack = []
        st.session_state.current_pack_type = None
        st.rerun()

    st.divider()

    # 오픈된 카드 표시 영역
    if st.session_state.current_pack:
        st.markdown(f"### 🎴 개봉된 팩: **{st.session_state.current_pack_type}")
        st.caption("뒷면 이미지를 클릭하여 카드를 하나씩 뒤집어보세요!")
        
        cols = st.columns(5)
        for idx, card in enumerate(st.session_state.current_pack):
            with cols[idx]:
                is_flipped = st.session_state.flipped_status[idx]
                
                if not is_flipped:
                    try:
                        st.image("Screenshot_20261101_181901_NAVER.jpg", use_container_width=True)
                    except:
                        st.write(f"카드 #{idx+1} [뒷면]")
                    
                    if st.button(f"뒤집기 #{idx+1}", key=f"card_btn_{idx}", use_container_width=True):
                        st.session_state.flipped_status[idx] = True
                        if card["rarity"] in ["SPECIAL", "UR"]:
                            st.balloons()
                        st.rerun()
                else:
                    rarity_color = {
                        "C": "gray", "R": "blue", "RR": "violet", 
                        "UR": "orange", "SPECIAL": "red"
                    }.get(card["rarity"], "gray")
                    
                    st.image(card["img"], use_container_width=True)
                    st.markdown(f"")
                    st.caption(f"{card['type']} | {card['hp']}HP")
                    st.markdown(f":{rarity_color}[**]")
        
        if not all(st.session_state.flipped_status):
            if st.button("👀 전체 카드 한 번에 뒤집기", use_container_width=True):
                st.session_state.flipped_status = [True, True, True, True, True]
                st.rerun()

with tab2:
    st.subheader("📖 카드 수집 앨범")
    cols = st.columns(4)
    for idx, c in enumerate(CARD_DATABASE):
        count = st.session_state.inventory.get(c["id"], 0)
        with cols[idx % 4]:
            if count > 0:
                st.image(c["img"], use_container_width=True)
                st.markdown(f"**{c['name']}** (x{count})")
                st.caption(f"등급: {c['rarity']}")
            else:
                st.markdown("### ❓ 미획득 카드")
                st.markdown("~~???~~")
                st.caption("🔒 상자에서 획득하세요")
