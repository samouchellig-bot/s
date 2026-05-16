import streamlit as st
import time

# إعدادات الصفحة والمظهر
st.set_page_config(page_title="مساعد الإنجاز اليومي", page_icon="✔", layout="centered")

# تعديل التصميم لضمان الاتجاه العربي بالكامل ومظهر مريح
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 600px; }
    h1, h2, h3, p, div, span, label { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stTextInput input, .stNumberInput input { text-align: right; direction: RTL; }
    .timer-box { background-color: #fff3cd; padding: 10px; border-radius: 5px; border-right: 5px solid #ffc107; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("مساعد الإنجاز الذكي مع المؤقت")
st.write("نظم يومك، حدد وقتاً لمهامك، وأنجزها بدون تسويف.")

# استخدام الجلسة (Session State) لحفظ البيانات
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "done_count" not in st.session_state:
    st.session_state.done_count = 0

# --- قسم إضافة مهمة جديدة مع وقتها ---
st.subheader("[+] أضف مهمة جديدة ووقتها")

col_name, col_time = st.columns([2, 1])
with col_name:
    new_task = st.text_input("ماذا تريد أن تنجز؟", placeholder="مثال: مراجعة درس الرياضيات...")
with col_time:
    task_minutes = st.number_input("المدّة (بالدقائق):", min_value=1, max_value=180, value=25)

if st.button("حفظ المهمة في الجدول") and new_task:
    # حفظ المهمة كقاموس يحتوي الاسم والوقت
    st.session_state.tasks.append({"name": new_task, "minutes": int(task_minutes)})
    st.rerun()

# --- قسم عرض المهام والمؤقت ---
st.subheader("[-] قائمة المهام والمؤقت الذكي")

if not st.session_state.tasks:
    st.success("تم إنجاز كل المهام الحالية بنجاح! أنت شخص رائع.")
else:
    for index, task in enumerate(st.session_state.tasks):
        # إنشاء حاوية لكل مهمة
        with st.container():
            col_txt, col_tmr, col_btn = st.columns([2, 1, 1])
            
            with col_txt:
                # الحل الجذري: استخراج البيانات أولاً في متغيرات بسيطة ونقية
                t_name = task["name"]
                t_mins = task["minutes"]
                # دمجها بشكل نصي كلاسيكي لا يسبب أي خطأ في الترميز أو الصياغة
                text_to_print = "{} | {} دقيقة".format(t_name, t_mins)
                st.info(text_to_print)
            
            with col_tmr:
                # زر لتشغيل مؤقت خاص بهذه المهمة
                if st.button(f"⏱ بدء {task['minutes']}د", key=f"tmr_{index}"):
                    with st.empty():
                        for t in range(int(task['minutes']), -1, -1):
                            st.markdown(f"<div class='timer-box'>⏳ متبقي: {t} دقيقة</div>", unsafe_allow_html=True)
                            time.sleep(1) 
                        st.markdown("<div class='timer-box'>🔔 انتهى الوقت! أنجزها الآن!</div>", unsafe_allow_html=True)
            
            with col_btn:
                if st.button("تم ✔", key=f"btn_{index}"):
                    st.session_state.done_count += 1
                    st.session_state.tasks.pop(index)
                    st.rerun()

st.write("---")
# عداد الإنجاز اليومي
st.metric(label="إجمالي المهام المنجزة اليوم", value=st.session_state.done_count)
