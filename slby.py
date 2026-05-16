import streamlit as st

# إعدادات الصفحة والمظهر
st.set_page_config(page_title="مساعد الإنجاز اليومي", page_icon="🚀", layout="centered")

# تغيير اتجاه الموقع ليدعم اللغة العربية من اليمين إلى اليسار
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 600px; }
    h1, h2, h3, p, div, span { direction: RTL; text-align: right; }
    div.stButton > button { width: 100%; background-color: #2e7d32; color: white; }
    </style>
""", unsafe_allow_name=True)

st.title("🚀 مساعد الإنجاز الذكي")
st.write("موقع بسيط لمساعدة الناس على تنظيم يومهم وإنجاز مهامهم بدون تشتيت.")

# استخدام الجلسة (Session State) لحفظ البيانات أثناء تصفح الموقع
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "done_count" not in st.session_state:
    st.session_state.done_count = 0

# --- قسم إضافة مهمة جديدة ---
st.subheader("➕ أضف مهمة جديدة الآن")
new_task = st.text_input("ماذا تريد أن تنجز اليوم؟", placeholder="مثال: مراجعة درس الرياضيات...")
col1, col2 = st.columns([3, 1])

with col2:
    if st.button("حفظ المهمة") and new_task:
        if new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)
            st.rerun()

# --- قسم عرض المهام والإنجاز ---
st.subheader("📋 قائمة المهام الحالية")

if not st.session_state.tasks:
    st.success("✨ رائعة! كل المهام منجزة حالياً. أنت شخص منتج!")
else:
    # عرض كل مهمة مع زر لإلغائها وإنجازها فوراً
    for index, task in enumerate(st.session_state.tasks):
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.info(f"🎯 {task}")
        with col_btn:
            if st.button("تم ✔️", key=f"btn_{index}"):
                st.session_state.done_count += 1
                st.session_state.tasks.pop(index)
                st.rerun()

st.write("---")
# عداد الإنجاز اليومي
st.metric(label="🏆 إجمالي المهام المنجزة اليوم", value=st.session_state.done_count)