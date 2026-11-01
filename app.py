import streamlit as st
import random
import json
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="포켓몬 카드팩 - 태양의 순환",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 카드 데이터베이스 ---
CARD_DATABASE = [
    # 새로 교체된 일반 카드 2종
    {
        "id": "cm1", 
        "name": "루나톤 (일반)", 
        "rarity": "C", 
        "type": "🔮 초", 
        "hp": 90, 
        "img": "Screenshot_20261101_182203_NAVER.jpg", 
        "desc": "달빛을 모아 에너지를 발산하는 포켓몬."
    },
    {
        "id": "cm2", 
        "name": "솔록 (일반)", 
        "rarity": "C", 
        "type": "🔥 불꽃", 
        "hp": 90, 
        "img": "Screenshot_20261101_182236_NAVER.jpg", 
        "desc": "태양의 열기를 담아 주변을 따뜻하게 만드는 포켓몬."
    },
    
    # SPECIAL ART (SAR) - 특일 카드
    {
        "id": "sm13", 
        "name": "솔록 V (특일)", 
        "rarity": "SPECIAL", 
        "type": "🔮 초", 
        "hp": 210, 
        "img": "file_00000000ad388206a3a6a269b5b4726d.png", 
        "desc": "상대의 포켓몬 전원에게 각각 10데미지를 준다. (Illus. Siu)"
    },
    {
        "id": "sm14", 
        "name": "루나톤 V (특일)", 
        "rarity": "SPECIAL", 
        "type": "🔮 초", 
        "hp": 210, 
        "img": "Screenshot_20261101_144113_ChatGPT.jpg", 
        "desc": "상대의 배틀 포켓몬을 혼란시킨다. (Illus. Siu)"
    }
]

# --- 세션 상태 초기화 ---
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "stats" not in st.session_state:
    st.session_state.stats = {"packs": 0, "cards": 0, "ur": 0, "special": 0}
if "current_pack" not in st.session_state:
    st.session_state.current_pack = []
if "flipped_status" not in st.session_state:
    st.session_state.flipped_status = [False, False, False, False, False]

# --- 가챠 확률 뽑기 로직 ---
def draw_single_card():
    rand = random.random()
    if rand < 0.01:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "SPECIAL"]
    else:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
    
    if not pool:
        pool = CARD_DATABASE
        
    return random.choice(pool)

def open_one_pack():
    new_cards = []
    has_special = False
    
    st.session_state.stats["packs"] += 1
    for _ in range(5):
        card = draw_single_card()
        new_cards.append(card)
        st.session_state.stats["cards"] += 1
        st.session_state.inventory[card["id"]] = st.session_state.inventory.get(card["id"], 0) + 1
        
        if card["rarity"] == "SPECIAL":
            st.session_state.stats["special"] += 1
            has_special = True
            
    st.session_state.current_pack = new_cards
    st.session_state.flipped_status = [False, False, False, False, False]
    return has_special

# --- 사이드바 (통계 및 JSON 저장/불러오기) ---
with st.sidebar:
    st.title("☀️ 태양의 순환")
    st.markdown("### 📊 수집 통계")
    st.write(f"📦 개봉한 팩 수: **{st.session_state.stats['packs']}**")
    st.write(f"🃏 전체 보유 카드: **{st.session_state.stats['cards']}**")
    st.write(f"✨ 특일(SAR) 획득: **{st.session_state.stats['special']}")
    
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
            st.session_state.stats = loaded_data.get("stats", {"packs": 0, "cards": 0, "ur": 0, "special": 0})
            st.success("데이터를 성공적으로 불러왔습니다!")
            st.rerun()
        except Exception as e:
            st.error("파일 형식 오류!")

# --- 메인 화면 ---
st.title("🎴 포켓몬 카드팩 시뮬레이터")
tab1, tab2 = st.tabs(["📦 팩 개봉하기", "📖 수집 도감"])

with tab1:
    st.subheader("✂️ 태양과 달의 교차 - 부스터 팩")
    st.caption("👇 아래 팩 이미지를 터치(클릭)하면 카드가 개봉됩니다!")
    
    col_img1, col_img2, col_img3 = st.columns([1, 1.5, 1])
    with col_img2:
        try:
            st.image("file_0000000056108206b69dcbce0d79c3bb.png", use_column_width=True)
        except:
            st.info("팩 이미지를 업로드해 주세요.")
            
        if st.button("🎁 부스터 팩 개봉하기!", type="primary", use_container_width=True):
            has_sp = open_one_pack()
            if has_sp:
                st.balloons()
                st.snow()
            st.rerun()

    st.divider()
    
    if st.session_state.current_pack:
        st.markdown("### 🎴 카드를 클릭하여 하나씩 뒤집어보세요!")
        cols = st.columns(5)
        
        for idx, card in enumerate(st.session_state.current_pack):
            with cols[idx]:
                is_flipped = st.session_state.flipped_status[idx]
                
                if not is_flipped:
                    if st.button(f"카드 #{idx+1}\n[뒷면]", key=f"card_btn_{idx}", use_container_width=True):
                        st.session_state.flipped_status[idx] = True
                        if card["rarity"] == "SPECIAL":
                            st.balloons()
                        st.rerun()
                else:
                    rarity_color = "red" if card["rarity"] == "SPECIAL" else "gray"
                    
                    st.image(card["img"], use_column_width=True)
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
                # 보유 중인 카드: 정상적으로 이미지와 이름 표시
                st.image(c["img"], use_column_width=True)
                st.markdown(f"**{c['name']}** (x{count})")
                st.caption(f"등급: {c['rarity']}")
            else:
                # 미보유 카드: 이미지를 숨기고 물음표로 대체
                st.markdown("### ❓ 미획득 카드")
                st.markdown("~~???~~")
                st.caption("🔒 팩에서 획득하세요")
