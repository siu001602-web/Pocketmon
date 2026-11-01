import streamlit as st
import random
import json
import time

# --- 페이지 기본 설정 (태블릿 반응형 모드) ---
st.set_page_config(
    page_title="포켓몬 카드팩 - 태양의 순환",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 카드 데이터베이스 정의 ---
CARD_DATABASE = [
    # C (Common)
    {"id": "sm1", "name": "캐스풍 (태양)", "rarity": "C", "type": "🔥 불꽃", "hp": 70, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/351-sunny.png"},
    {"id": "sm2", "name": "캐스풍 (빗물)", "rarity": "C", "type": "💧 물", "hp": 70, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/351-rainy.png"},
    {"id": "sm3", "name": "해루미", "rarity": "C", "type": "🌿 풀", "hp": 80, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/192.png"},
    {"id": "sm4", "name": "별가사리", "rarity": "C", "type": "💧 물", "hp": 60, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/120.png"},
    {"id": "sm5", "name": "삐삐", "rarity": "C", "type": "✨ 페어리", "hp": 60, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/35.png"},
    
    # R (Rare)
    {"id": "sm6", "name": "에스페온", "rarity": "R", "type": "🔮 초", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/196.png"},
    {"id": "sm7", "name": "블래키", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/197.png"},
    {"id": "sm8", "name": "나인테일", "rarity": "R", "type": "🔥 불꽃", "hp": 120, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/38.png"},
    {"id": "sm9", "name": "헬가", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/229.png"},
    
    # SR (Super Rare)
    {"id": "sm10", "name": "솔가레오", "rarity": "SR", "type": "⚔️ 강철", "hp": 170, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/791.png"},
    {"id": "sm11", "name": "루나아라", "rarity": "SR", "type": "🔮 초", "hp": 170, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/792.png"},
    {"id": "sm12", "name": "크레세리아", "rarity": "SR", "type": "🔮 초", "hp": 130, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/488.png"},
    
    # UR (Ultra Rare - 0.1%)
    {"id": "sm-ur1", "name": "네크로즈마 (황혼의 갈기)", "rarity": "UR", "type": "⚔️ 강철", "hp": 220, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/800-dusk-mane.png"},
    {"id": "sm-ur2", "name": "네크로즈마 (새벽의 날개)", "rarity": "UR", "type": "🔮 초", "hp": 220, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/800-dawn-wings.png"},
    {"id": "sm-ur3", "name": "칠색조 V", "rarity": "UR", "type": "🔥 불꽃", "hp": 230, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/250.png"},
    
    # SPECIAL ART (SAR - 0.0001%)
    {"id": "sm13", "name": "솔록 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/338.png"},
    {"id": "sm14", "name": "루나톤 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/337.png"}
]

# --- 세션 상태 초기화 ---
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "stats" not in st.session_state:
    st.session_state.stats = {"packs": 0, "cards": 0, "ur": 0, "special": 0}
if "last_opened" not in st.session_state:
    st.session_state.last_opened = []

# --- 가챠 확률 뽑기 로직 ---
def draw_single_card():
    rand = random.random()
    # Special Art (0.0001%)
    if rand < 0.000001:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "SPECIAL"]
    # UR (0.1%)
    elif rand < 0.0011:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "UR"]
    else:
        rand_sub = random.random() * 100
        if rand_sub < 14.889:
            target = "SR"
        elif rand_sub < 39.889:
            target = "R"
        else:
            target = "C"
        pool = [c for c in CARD_DATABASE if c["rarity"] == target]
    
    if not pool:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
        
    return random.choice(pool)

def open_packs(num_packs):
    new_cards = []
    has_special = False
    
    for _ in range(num_packs):
        st.session_state.stats["packs"] += 1
        for _ in range(5):
            card = draw_single_card()
            new_cards.append(card)
            st.session_state.stats["cards"] += 1
            st.session_state.inventory[card["id"]] = st.session_state.inventory.get(card["id"], 0) + 1
            
            if card["rarity"] == "UR":
                st.session_state.stats["ur"] += 1
            elif card["rarity"] == "SPECIAL":
                st.session_state.stats["special"] += 1
                has_special = True
                
    st.session_state.last_opened = new_cards
    return has_special

# --- 사이드바 (통계 및 JSON 저장/불러오기) ---
with st.sidebar:
    st.title("☀️ 태양의 순환")
    st.markdown("### 📊 수집 통계")
    st.write(f"📦 개봉한 팩 수: **{st.session_state.stats['packs']}**")
    st.write(f"🃏 전체 보유 카드: **{st.session_state.stats['cards']}**")
    st.write(f"🌟 UR 획득: **{st.session_state.stats['ur']}**")
    st.write(f"✨ 특일(SAR) 획득: **{st.session_state.stats['special']}**")
    
    st.divider()
    st.markdown("### 💾 데이터 관리 (Save/Load)")
    
    # JSON 파일 내보내기 (다운로드)
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
    
    # JSON 파일 불러오기 (업로드)
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

# --- 메인 탭 화면 ---
st.title("🎴 포켓몬 카드팩 시뮬레이터")
tab1, tab2 = st.tabs(["📦 팩 개봉하기", "📖 수집 도감"])

# TAB 1: 팩 개봉
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✂️ 1팩 개봉하기 (5장)", use_container_width=True, type="primary"):
            has_sp = open_packs(1)
            if has_sp:
                st.balloons()
                st.snow()
                with st.spinner("✨ 0.0001% 특일(SAR) 카드가 등장했습니다! (10초 연출)"):
                    time.sleep(10)
    with col2:
        if st.button("📦 30팩(1박스) 한 번에 개봉하기", use_container_width=True):
            has_sp = open_packs(30)
            if has_sp:
                st.balloons()
                st.snow()
                with st.spinner("✨ 0.0001% 특일(SAR) 카드가 등장했습니다! (10초 연출)"):
                    time.sleep(10)

    st.divider()
    
    # 개봉 결과 표시
    if st.session_state.last_opened:
        st.subheader("🎉 최신 개봉 결과")
        cards = st.session_state.last_opened
        
        # 5개씩 줄바꿈하여 카드 표시
        for i in range(0, len(cards), 5):
            cols = st.columns(5)
            chunk = cards[i:i+5]
            for idx, c in enumerate(chunk):
                with cols[idx]:
                    rarity_color = {
                        "C": "gray", "R": "blue", "SR": "purple", 
                        "UR": "orange", "SPECIAL": "red"
                    }.get(c["rarity"], "gray")
                    
                    st.image(c["img"], use_column_width=True)
                    st.markdown(f"**{c['name']}**")
                    st.caption(f"{c['type']} | {c['hp']} HP")
                    st.markdown(f":{rarity_color}[[{c['rarity']}]]")

# TAB 2: 수집 도감
with tab2:
    st.subheader("📖 카드 수집 앨범")
    cols = st.columns(4)
    for idx, c in enumerate(CARD_DATABASE):
        count = st.session_state.inventory.get(c["id"], 0)
        with cols[idx % 4]:
            if count > 0:
                st.image(c["img"], use_column_width=True)
                st.markdown(f"**{c['name']}** (x{count})")
                st.caption(f"등급: {c['rarity']}")
            else:
                st.image(c["img"], use_column_width=True, channels="BGR")
                st.markdown(f"~~{c['name']}~~ (미보유)")
                st.caption("🔒 획득 필요")
