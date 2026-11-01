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
    # --- 일반 팩 및 기본 카드군 ---
    {"id": "cm1", "name": "루나톤 (일반)", "rarity": "C", "type": "🔮 초", "hp": 90, "img": "Screenshot_20261101_182203_NAVER.jpg", "desc": "달빛을 모아 에너지를 발산하는 포켓몬."},
    {"id": "cm2", "name": "솔록 (일반)", "rarity": "C", "type": "🔥 불꽃", "hp": 90, "img": "Screenshot_20261101_182236_NAVER.jpg", "desc": "태양의 열기를 담아 주변을 따뜻하게 만드는 포켓몬."},
    
    {"id": "rm1", "name": "블래키", "rarity": "R", "type": "🌑 악", "hp": 110, "img": "Screenshot_20261101_183128_NAVER.jpg", "desc": "달빛을 받으면 온몸의 노란 고리 문양이 빛난다."},
    {"id": "rm2", "name": "불카모스", "rarity": "R", "type": "🔥 불꽃", "hp": 130, "img": "Screenshot_20261101_183155_NAVER.jpg", "desc": "불타는 날개에서 수많은 화염 가루를 흩뿌린다."},
    {"id": "rm3", "name": "루나아라", "rarity": "R", "type": "🔮 초", "hp": 150, "img": "Screenshot_20261101_183235_NAVER.jpg", "desc": "밤하늘의 빛을 흡수하여 날개를 펼치는 전설의 포켓몬."},
    {"id": "rm4", "name": "솔가레오", "rarity": "R", "type": "⚔️ 강철", "hp": 150, "img": "Screenshot_20261101_183241_NAVER.jpg", "desc": "태양의 에너지를 품고 당당하게 달리는 전설의 포켓몬."},

    {"id": "rrm1", "name": "불카모스 V", "rarity": "RR", "type": "🔥 불꽃", "hp": 220, "img": "Screenshot_20261101_183206_NAVER.jpg", "desc": "강렬한 화염의 힘을 두른 강력한 모습의 불카모스 V."},

    {"id": "urm1", "name": "솔가레오 V (울트라레어)", "rarity": "UR", "type": "⚔️ 강철", "hp": 240, "img": "Screenshot_20261101_183221_NAVER.jpg", "desc": "태양의 빛을 극한으로 끌어올린 초희귀 솔가레오."},

    {"id": "sm13", "name": "솔록 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "file_00000000ad388206a3a6a269b5b4726d.png", "desc": "상대의 포켓몬 전원에게 각각 10데미지를 준다. (Illus. Siu)"},
    {"id": "sm14", "name": "루나톤 V (특일)", "rarity": "SPECIAL", "type": "🔮 초", "hp": 210, "img": "Screenshot_20261101_144113_ChatGPT.jpg", "desc": "상대의 배틀 포켓몬을 혼란시킨다. (Illus. Siu)"},

    # --- 프로모 팩 전용 신규 카드군 (AR / GX) ---
    {
        "id": "promo_ar_sol", 
        "name": "솔록 (AR)", 
        "rarity": "AR", 
        "type": "🔥 불꽃", 
        "hp": 120, 
        "img": "Screenshot_20261101_193947_NAVER.jpg", 
        "desc": "프로모 팩 전용 아트페어 솔록."
    },
    {
        "id": "promo_ar_luna", 
        "name": "루나톤 (AR)", 
        "rarity": "AR", 
        "type": "🔮 초", 
        "hp": 120, 
        "img": "Screenshot_20261101_193934_NAVER.jpg", 
        "desc": "프로모 팩 전용 아트페어 루나톤."
    },
    {
        "id": "promo_gx_espeon", 
        "name": "에스페온 GX", 
        "rarity": "GX", 
        "type": "🔮 초", 
        "hp": 200, 
        "img": "Screenshot_20261101_194118_NAVER.jpg", 
        "desc": "프로모 팩 전용 초희귀 에스페온 GX."
    }
]

# --- 세션 상태 안전 초기화 ---
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "pack_inventory" not in st.session_state:
    st.session_state.pack_inventory = {"normal": 0, "promo": 0}
if "stats" not in st.session_state:
    st.session_state.stats = {"packs": 0, "cards": 0, "special": 0}
if "shop_boxes" not in st.session_state:
    st.session_state.shop_boxes = None
if "current_pack" not in st.session_state:
    st.session_state.current_pack = []
if "current_pack_type" not in st.session_state:
    st.session_state.current_pack_type = None
if "flipped_status" not in st.session_state:
    st.session_state.flipped_status = []
if "active_cutscene" not in st.session_state:
    st.session_state.active_cutscene = None
if "card_best_grades" not in st.session_state:
    st.session_state.card_best_grades = {}
if "last_grading_result" not in st.session_state:
    st.session_state.last_grading_result = None

# --- 등급 순위 매기기용 함수 ---
def get_grade_priority(result_str):
    if "Black Label" in result_str:
        return 5
    elif "Gem Mint" in result_str:
        return 4
    elif "PSA 9" in result_str:
        return 3
    elif "PSA 8" in result_str:
        return 2
    elif "Standard" in result_str:
        return 1
    return 0

# --- 카드 뽑기 로직 ---
def draw_single_card(is_promo=False):
    rand = random.random()
    if is_promo:
        if rand < 0.02:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "GX"]
        else:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "AR"]
    else:
        special_rate = 0.00001
        ur_rate = 0.001
        
        if rand < special_rate:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "SPECIAL"]
        elif rand < ur_rate:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "UR"]
        elif rand < 0.075:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "RR"]
        elif rand < 0.345:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "R"]
        else:
            pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
            
    if not pool:
        pool = [c for c in CARD_DATABASE if c["rarity"] == "C"]
        
    return random.choice(pool)

def open_pack_from_bag(pack_type="normal"):
    if st.session_state.pack_inventory[pack_type] <= 0:
        return False
        
    is_promo = (pack_type == "promo")
    st.session_state.pack_inventory[pack_type] -= 1
    st.session_state.stats["packs"] += 1
    st.session_state.current_pack_type = "태양의 순환 프로모 팩" if is_promo else "태양의 순환 일반 팩"
    
    card_count = 1 if is_promo else 7
    new_cards = []
    
    for _ in range(card_count):
        card = draw_single_card(is_promo=is_promo)
        new_cards.append(card)
        st.session_state.stats["cards"] += 1
        st.session_state.inventory[card["id"]] = st.session_state.inventory.get(card["id"], 0) + 1
        
        if card["rarity"] in ["SPECIAL", "UR", "GX", "AR"]:
            st.session_state.stats["special"] += 1
            
    st.session_state.current_pack = new_cards
    st.session_state.flipped_status = [False] * card_count
    st.session_state.active_cutscene = None

# --- 사이드바 ---
with st.sidebar:
    st.title("☀️ 태양의 순환")
    st.markdown("### 🎒 내 가방 (보유 팩)")
    st.write(f"📦 일반 팩: **{st.session_state.pack_inventory['normal']}개**")
    st.write(f"✨ 프로모 팩: **{st.session_state.pack_inventory['promo']}개**")
    
    st.divider()
    st.markdown("### 📊 수집 통계")
    st.write(f"📦 개봉한 팩 수: **{st.session_state.stats['packs']}**")
    st.write(f"🃏 전체 보유 카드: **{st.session_state.stats['cards']}**")
    st.write(f"✨ 희귀 카드 획득: **{st.session_state.stats['special']}**")
    
    st.divider()
    st.markdown("### 💾 데이터 관리 (Save/Load)")
    save_data = {
        "inventory": st.session_state.inventory,
        "pack_inventory": st.session_state.pack_inventory,
        "stats": st.session_state.stats,
        "card_best_grades": st.session_state.card_best_grades
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
            st.session_state.pack_inventory = loaded_data.get("pack_inventory", {"normal": 0, "promo": 0})
            st.session_state.stats = loaded_data.get("stats", {"packs": 0, "cards": 0, "special": 0})
            st.session_state.card_best_grades = loaded_data.get("card_best_grades", {})
            st.success("데이터를 성공적으로 불러왔습니다!")
            st.rerun()
        except Exception:
            st.error("파일 형식 오류!")

# --- 메인 화면 ---
st.title("🎴 포켓몬 카드팩 시뮬레이터")
tab1, tab2, tab3, tab4 = st.tabs(["🛒 상점 (상자 뽑기)", "🎒 가방 및 팩 개봉", "📖 수집 도감", "🔍 카드 등급 감정소"])

# --- 탭 1: 상점 ---
with tab1:
    st.subheader("🏪 상점")
    st.caption("버튼을 누르면 3개의 미스터리 구역 상자가 나타납니다. (90% 일반 팩 / 10% 프로모 팩)")
    
    if st.button("🎲 상점 열기 (상자 3개 불러오기)", type="primary", use_container_width=True):
        boxes = []
        for _ in range(3):
            is_promo = (random.random() >= 0.90)
            boxes.append({"type": "promo" if is_promo else "normal", "bought": False})
        st.session_state.shop_boxes = boxes
        st.rerun()

    st.divider()
    
    if st.session_state.shop_boxes is not None:
        st.markdown("### 🎁 3개의 상자 구역 중 원하는 것을 선택하세요!")
        cols = st.columns(3)
        
        for idx, box in enumerate(st.session_state.shop_boxes):
            with cols[idx]:
                p_type = box["type"]
                is_promo = (p_type == "promo")
                
                st.markdown(f"#### 📍 구역 #{idx + 1}")
                if not box["bought"]:
                    try:
                        img_file = "file_00000000de388206bbea5cdf416bbe01.png" if is_promo else "file_0000000056108206b69dcbce0d79c3bb.png"
                        st.image(img_file, use_container_width=True)
                    except:
                        st.info("상자 이미지")
                    
                    if st.button(f"🛒 구역 #{idx + 1} 구매하여 가방에 넣기", key=f"buy_box_{idx}", use_container_width=True):
                        st.session_state.pack_inventory[p_type] += 1
                        box["bought"] = True
                        
                        if is_promo:
                            st.toast("✨ 대박! 프로모 팩을 획득하여 가방에 담았습니다!", icon="🎉")
                        else:
                            st.toast("☀️ 일반 팩을 획득하여 가방에 담았습니다!", icon="📦")
                        st.rerun()
                else:
                    st.success("✅ 구매 완료 (가방에 지급됨)")
    else:
        st.info("💡 상점 열기 버튼을 눌러 상자 3개를 불러오세요.")

# --- 탭 2: 가방 및 팩 개봉 ---
with tab2:
    st.subheader("🎒 가방에서 팩 개봉하기")
    st.caption("가방에 보유 중인 팩을 선택하여 카드를 뜯어보세요!")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### ☀️ 태양의 순환 (일반 팩 - 7장)")
        try:
            st.image("file_0000000056108206b69dcbce0d79c3bb.png", use_container_width=True)
        except:
            st.info("일반 팩 이미지")
        st.write(f"보유 수량: **{st.session_state.pack_inventory['normal']}개**")
        
        if st.button("✂️ 일반 팩 개봉하기 (7장)", disabled=(st.session_state.pack_inventory['normal'] <= 0), use_container_width=True):
            open_pack_from_bag("normal")
            st.rerun()

    with col_p2:
        st.markdown("### ✨ 태양의 순환 (프로모 팩 - 1장)")
        try:
            st.image("file_00000000de388206bbea5cdf416bbe01.png", use_container_width=True)
        except:
            st.info("프로모 팩 이미지")
        st.write(f"보유 수량: **{st.session_state.pack_inventory['promo']}개**")
        
        if st.button("✂️ 프로모 팩 개봉하기 (1장)", disabled=(st.session_state.pack_inventory['promo'] <= 0), use_container_width=True):
            open_pack_from_bag("promo")
            st.rerun()

    st.divider()

    if st.session_state.active_cutscene == "sol":
        st.markdown("### 🎬 ✨ **SOLROCK CUTSCENE (솔록 컷씬)** ✨")
        try:
            st.video("20261101_195631209.mp4", autoplay=True)
        except:
            st.info("📹 솔록 컷씬 파일(20261101_195631209.mp4)을 찾을 수 없습니다.")
    elif st.session_state.active_cutscene == "luna":
        st.markdown("### 🎬 ✨ **LUNATONE CUTSCENE (루나톤 컷씬)** ✨")
        try:
            st.video("2026-11-01-201120.mp4", autoplay=True)
        except:
            st.info("📹 루나톤 컷씬 파일(2026-11-01-201120.mp4)을 찾을 수 없습니다.")

    if st.session_state.current_pack:
        st.markdown(f"### 🎴 개봉된 팩: **{st.session_state.current_pack_type} ({len(st.session_state.current_pack)}장)")
        st.caption("뒷면 이미지를 클릭하여 카드를 하나씩 뒤집어보세요!")
        
        cols = st.columns(len(st.session_state.current_pack))
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
                            if "솔록" in card["name"]:
                                st.session_state.active_cutscene = "sol"
                            elif "루나톤" in card["name"]:
                                st.session_state.active_cutscene = "luna"
                            else:
                                st.session_state.active_cutscene = "sol"
                        st.rerun()
                else:
                    rarity_color = {
                        "C": "gray", "R": "blue", "RR": "violet", 
                        "UR": "orange", "SPECIAL": "red", 
                        "AR": "green", "GX": "gold"
                    }.get(card["rarity"], "gray")
                    
                    st.image(card["img"], use_container_width=True)
                    st.markdown(f"")
                    st.caption(f"{card['type']} | {card['hp']}HP")
                    st.markdown(f":{rarity_color}[**]")
        
        if not all(st.session_state.flipped_status):
            if st.button("👀 전체 카드 한 번에 뒤집기", use_container_width=True):
                st.session_state.flipped_status = [True] * len(st.session_state.current_pack)
                for card in st.session_state.current_pack:
                    if card["rarity"] in ["SPECIAL", "UR"]:
                        if "솔록" in card["name"]:
                            st.session_state.active_cutscene = "sol"
                        elif "루나톤" in card["name"]:
                            st.session_state.active_cutscene = "luna"
                st.rerun()

# --- 탭 3: 수집 도감 ---
with tab3:
    st.subheader("📖 카드 수집 앨범")
    st.caption("각 카드의 최고 등급(티어)과 정밀 평균 점수가 도감에 표시됩니다.")
    
    cols = st.columns(4)
    for idx, c in enumerate(CARD_DATABASE):
        count = st.session_state.inventory.get(c["id"], 0)
        best_grade_info = st.session_state.card_best_grades.get(c["id"], None)
        
        with cols[idx % 4]:
            if count > 0:
                st.image(c["img"], use_container_width=True)
                st.markdown(f"**{c['name']}** (x{count})")
                st.caption(f"등급: {c['rarity']}")
                
                if best_grade_info:
                    st.markdown(f"🏆 최고 등급: **{best_grade_info['result']}**")
                    st.caption(f"📊 정밀 평균: **{best_grade_info['avg']:.1f}점**")
                else:
                    st.markdown("⭐ 최고 등급: **미감정 (Raw)**")
            else:
                st.markdown("### ❓ 미획득 카드")
                st.markdown("~~???~~")
                st.caption("🔒 팩에서 획득하세요")

# --- 탭 4: 카드 등급 감정소 ---
with tab4:
    st.subheader("🔍 프로페셔널 카드 등급 감정소")
    st.caption("보유 중인 카드를 감정에 맡겨 더 높은 등급에 도전해보세요! (감정 시 중복 카드는 자동 정리되어 1장만 남습니다)")
    
    available_cards = [c for c in CARD_DATABASE if st.session_state.inventory.get(c["id"], 0) > 0]
    
    if not available_cards:
        st.info("💡 감정할 수 있는 카드가 없습니다. 상점에서 팩을 까서 카드를 먼저 모아주세요!")
    else:
        card_options = {
            f"{c['name']} (보유: {st.session_state.inventory.get(c['id'], 0)}장)": c 
            for c in available_cards
        }
        selected_label = st.selectbox("감정 의뢰할 카드를 선택하세요", list(card_options.keys()))
        target_card = card_options[selected_label]
        
        col_prev, col_desc = st.columns([1, 2])
        with col_prev:
            st.image(target_card["img"], use_container_width=True)
        with col_desc:
            st.markdown(f"### **{target_card['name']}**")
            st.caption(f"등급: {target_card['rarity']} | 속성: {target_card['type']}")
            st.write(target_card["desc"])
            
            if st.button("🛡️ 정밀 등급 감정 시작하기", type="primary", use_container_width=True):
                cid = target_card["id"]
                
                centering = random.randint(1, 10)
                quality = random.randint(1, 10)
                coating = random.randint(1, 10)
                scratch = random.randint(1, 10)
                avg_score = (centering + quality + coating + scratch) / 4.0
                
                if centering == 10 and quality == 10 and coating == 10 and scratch == 10:
                    grade_result = "🖤 BGS Black Label (10 Grade)"
                elif avg_score >= 9.9:
                    grade_result = "🌟 Gem Mint (9.9 Grade)"
                elif avg_score >= 8.5:
                    grade_result = "💎 PSA 9 (Mint)"
                elif avg_score >= 7.0:
                    grade_result = "⭐ PSA 8 (Near Mint-Mint)"
                else:
                    grade_result = "📦 일반 등급 (Standard)"
                
                new_grade_info = {
                    "centering": centering,
                    "quality": quality,
                    "coating": coating,
                    "scratch": scratch,
                    "avg": avg_score,
                    "result": grade_result,
                    "priority": get_grade_priority(grade_result)
                }
                
                st.session_state.last_grading_result = {
                    "card_name": target_card["name"],
                    "img": target_card["img"],
                    **new_grade_info
                }
                
                # 최고 등급 갱신 로직
                current_best = st.session_state.card_best_grades.get(cid, None)
                if current_best is None or new_grade_info["priority"] >= current_best["priority"]:
                    st.session_state.card_best_grades[cid] = new_grade_info
                
                # 🔥 핵심 수정: 감정 직후 해당 카드의 보유 수량을 무조건 1장으로 강제 고정하여 중복 카드 즉시 정리
                st.session_state.inventory[cid] = 1
                
                st.rerun()

    if st.session_state.last_grading_result:
        res = st.session_state.last_grading_result
        st.divider()
        st.markdown("### 🏆 **방금 완료된 감정 결과**")
        
        res_col1, res_col2 = st.columns([1, 3])
        with res_col1:
            st.image(res["img"], use_container_width=True)
        with res_col2:
            st.markdown(f"#### **{res['card_name']}**")
            st.markdown(f"✨ 판정 등급: **{res['result']}** (평균: `{res['avg']:.1f}점`)")
            st.markdown(
                f"• 🎯 센터링: **{res['centering']}점** | "
                f"• 💎 화질: **{res['quality']}점** | "
                f"• 🛡️ 코팅: **{res['coating']}점** | "
                f"• 🔍 자국: **{res['scratch']}점**"
            )
            st.success("✅ 감정이 완료되었으며, 중복 카드가 깔끔하게 정리되어 1장만 남았습니다!")
