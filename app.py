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

# --- 카드 데이터베이스 (캐스풍 이미지 및 특일 카드 포함) ---
CARD_DATABASE = [
    # C (Common) - 캐스풍 이미지 추가 반영
    {"id": "sm1", "name": "캐스풍 (태양)", "rarity": "C", "type": "🔥 불꽃", "hp": 70, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/351-sunny.png", "desc": "강렬한 햇빛을 받아 불꽃 타입으로 형태가 변한 포켓몬."},
    {"id": "sm2", "name": "캐스풍 (빗물)", "rarity": "C", "type": "💧 물", "hp": 70, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/351-rainy.png", "desc": "강한 비를 받아 몸의 구조가 물 타입으로 변화한다."},
    {"id": "sm3", "name": "해루미", "rarity": "C", "type": "🌿 풀", "hp": 80, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/192.png", "desc": "태양 빛 에너지를 받아 몸에서 광채를 뿜어낸다."},
    {"id": "sm4", "name": "별가사리", "rarity": "C", "type": "💧 물", "hp": 60, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/120.png", "desc": "밤이 되면 중심의 코어가 붉게 뿜어 나오며 별빛과 교신한다."},
    {"id": "sm5", "name": "삐삐", "rarity": "C", "type": "✨ 페어리", "hp": 60, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/35.png", "desc": "보름달 밤에 모여 춤을 추며 달의 에너지를 모은다."},
    
    # R (Rare)
    {"id": "sm6", "name": "에스페온", "rarity": "R", "type": "🔮 초", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/196.png", "desc": "이마의 붉은 구슬로 낮의 햇빛 에너지를 흡수해 예지 능력을 얻는다."},
    {"id": "sm7", "name": "블래키", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/197.png", "desc": "달빛을 받으면 온몸의 노란 고리 문양이 노랗게 빛난다."},
    {"id": "sm8", "name": "나인테일", "rarity": "R", "type": "🔥 불꽃", "hp": 120, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/38.png", "desc": "아홉 개의 꼬리에 신통한 신비의 힘이 깃들어 있다."},
    {"id": "sm9", "name": "헬가", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/229.png", "desc": "어두운 밤 달빛 아래에서 무시무시한 울음소리를 낸다."},
    
    # SR (Super Rare)
    {"id": "sm10", "name": "솔가레오", "rarity": "SR", "type": "⚔️ 강철", "hp": 170, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/791.png", "desc": "태양을 삼킨 전설의 포켓몬으로 밤을 낮처럼 밝게 비춘다."},
    {"id": "sm11", "name": "루나아라", "rarity": "SR", "type": "🔮 초", "hp": 170, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/792.png", "desc": "달을 사로잡은 전설의 포켓몬으로 밤하늘의 빛을 흡수한다."},
    {"id": "sm12", "name": "크레세리아", "rarity": "SR", "type": "🔮 초", "hp": 130, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/488.png", "desc": "초승달을 닮은 날개에서 오로라 빛 알갱이를 흩뿌린다."},
    
    # UR (Ultra Rare - 0.1%)
    {"id": "sm-ur1", "name": "네크로즈마 (황혼의 갈기)", "rarity": "UR", "type": "⚔️ 강철", "hp": 220, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/800-dusk-mane.png", "desc": "솔가레오의 햇빛 에너지를 정복한 전설의 울트라 비스트"},
    {"id": "sm-ur2", "name": "네크로즈마 (새벽의 날개)", "rarity": "UR", "type": "🔮 초", "hp": 220, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/800-dawn-wings.png", "desc": "루나아라의 달빛 에너지를 집어삼킨 울트라 비스트"},
    {"id": "sm-ur3", "name": "칠색조 V", "rarity": "UR", "type": "🔥 불꽃", "hp": 230, "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/250.png", "desc": "무지갯빛 날개로 하늘을 가르며 일곱 빛깔을 뿌린다"},
    
    # SPECIAL ART (SAR - 0.0001% / 솔록 V, 루나톤 V 실제 이미지 적용)
    {
        "id": "sm13", 
        "name": "솔록 V (특일)", 
        "rarity": "SPECIAL", 
        "type": "🔮 초", 
        "hp": 210, 
        "img": "https://i.ibb.co/6R3vZJ3/1000000840.png",
        "desc": "상대의 포켓몬 전원에게 각각 10데미지를 준다. (Illus. Siu)"
    },
    {
        "id": "sm14", 
        "name": "루나톤 V (특일)", 
        "rarity": "SPECIAL", 
        "type": "🔮 초", 
        "hp": 210, 
        "img": "https://i.ibb.co/7X1vZJ4/1000000841.jpg",
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
    if rand < 0.000001:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "SPECIAL"]
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

def open_one_pack():
    new_cards = []
    has_special = False
    
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
            
    st.session_state.current_pack = new_cards
    st.session_state.flipped_status = [False, False, False, False, False]
    return has_special

# --- 사이드바 (통계 및 JSON 저장/불러오기) ---
with st.sidebar:
    st.title("☀️ 태양의 순환")
    st.markdown("### 📊 수집 통계")
    st.write(f"📦 개봉한 팩 수: **{st.session_state.stats['packs']}**")
    st.write(f"🃏 전체 보유 카드: **{st.session_state.stats['cards']}**")
    st.write(f"🌟 UR 획득: **{st.session_state.stats['ur']}**")
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
    
    # 팩 까기 버튼 (1팩씩만 개봉)
    if st.button("✂️ 카드팩 개봉하기 (5장)", type="primary", use_container_width=True):
        has_sp = open_one_pack()
        if has_sp:
            st.balloons()
            st.snow()

    st.divider()
    
    # 카드가 생성된 경우: 직접 뒤집는 인터페이스 제공
    if st.session_state.current_pack:
        st.markdown("### 🎴 카드를 클릭하여 하나씩 뒤집어보세요!")
        cols = st.columns(5)
        
        for idx, card in enumerate(st.session_state.current_pack):
            with cols[idx]:
                is_flipped = st.session_state.flipped_status[idx]
                
                if not is_flipped:
                    # 뒷면 상태 (클릭하면 뒤집힘)
                    if st.button(f"카드 #{idx+1}\n[뒷면]", key=f"card_btn_{idx}", use_container_width=True):
                        st.session_state.flipped_status[idx] = True
                        if card["rarity"] == "SPECIAL":
                            st.balloons()
                        st.rerun()
                else:
                    # 앞면 상태 (뒤집힌 후)
                    rarity_color = {
                        "C": "gray", "R": "blue", "SR": "purple", 
                        "UR": "orange", "SPECIAL": "red"
                    }.get(card["rarity"], "gray")
                    
                    st.image(card["img"], use_column_width=True)
                    st.markdown(f"**")
                    st.caption(f"{card['type']} | {card['hp']} HP")
                    st.markdown(f":{rarity_color}[[{card['rarity']}]]")
        
        # 전체 한 번에 뒤집기 버튼
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
                st.image(c["img"], use_column_width=True)
                st.markdown(f"**{c['name']}** (x{count})")
                st.caption(f"등급: {c['rarity']}")
            else:
                st.image(c["img"], use_column_width=True)
                st.markdown(f"~~{c['name']}~~ (미보유)")
                st.caption("🔒 획득 필요")
