import streamlit as st
import time

# إعدادات الصفحة والمظهر
st.set_page_config(page_title="مساعد الإنجاز اليومي", page_icon="✔", layout="centered")

# تعديل التصميم لضمان الاتجاه العربي بالكامل ومظهر مريح ومحفز
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 600px; }
    h1, h2, h3, p, div, span, label { direction: RTL !important; text-align: right !important; }
    div.stButton > button { width: 100%; background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stTextInput input, .stNumberInput input { text-align: right; direction: RTL; }
    .timer-box { background-color: #fff3cd; padding: 10px; border-radius: 5px; border-right: 5px solid #ffc107; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("مساعد الإنجاز الذكي الحماسي")
st.write("نظم يومك، أشعل حماسك بالموسيقى، وأنجز مهامك قبل انتهاء المنبه!")

# استخدام الجلسة (Session State) لحفظ البيانات بنقاء
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "done_count" not in st.session_state:
    st.session_state.done_count = 0

# --- روابط الصوت والموسيقى المجانية أونلاين ---
# موسيقى حماسية للخلفية (تشتغل أثناء الموقت)
BGM_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
# صوت جرس منبه قوي (يشتغل عند انتهاء الوقت)
ALARM_URL = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"

# --- قسم إضافة مهمة جديدة مع وقتها ---
st.subheader("[+] أضف مهمة جديدة ووقتها")

col_name, col_time = st.columns([2, 1])
with col_name:
    new_task = st.text_input("ماذا تريد أن تنجز؟", placeholder="مثال: مراجعة درس الرياضيات...")
with col_time:
    task_minutes = st.number_input("المدّة (بالدقائق):", min_value=1, max_value=180, value=25)

if st.button("حفظ المهمة في الجدول") and new_task:
    st.session_state.tasks.append({"name": str(new_task), "minutes": int(task_minutes)})
    st.rerun()

# --- قسم عرض المهام والمؤقت ---
st.subheader("[-] قائمة المهام والمؤقت الذكي")

if not st.session_state.tasks:
    st.success("تم إنجاز كل المهام الحالية بنجاح! أنت شخص رائع.")
else:
    for index, task in enumerate(st.session_state.tasks):
        if isinstance(task, dict) and "name" in task and "minutes" in task:
            with st.container():
                col_txt, col_tmr, col_btn = st.columns([2, 1, 1])
                
                with col_txt:
                    st.info(f"{task['name']} | {task['minutes']} دقيقة")
                
                with col_tmr:
                    if st.button(f"⏱ بدء {task['minutes']}د", key=f"tmr_{index}"):
                        # 1. تشغيل الموسيقى الحماسية في الخلفية تلقائياً فور بدء العداد
                        st.markdown(f'<audio src="{BGM_URL}" autoplay loop hidden></audio>', unsafe_allow_html=True)
                        
                        with st.empty():
                            for t in range(int(task['minutes']), -1, -1):
                                st.markdown(f"<div class='timer-box'>⏳ متبقي: {t} دقيقة (الموسيقى تعمل...)</div>", unsafe_allow_html=True)
                                time.sleep(1) 
                            
                            # 2. عند انتهاء الوقت: إيقاف الموسيقى وإصدار صوت منبه قوي وتلقائي
                            st.markdown(f'<audio src="{ALARM_URL}" autoplay></audio>', unsafe_allow_html=True)
                            st.markdown("<div class='timer-box' style='background-color: #f8d7da; border-right: 5px solid #dc3545;'>🔔 انتهى الوقت! أصدرنا تنبيهاً صوتاً، أنجزها الآن!</div>", unsafe_allow_html=True)
                
                with col_btn:
                    if st.button("تم ✔", key=f"btn_{index}"):
                        st.session_state.done_count += 1
                        st.session_state.tasks.pop(index)
                        st.rerun()
        else:
            st.session_state.tasks.pop(index)
            st.rerun()

st.write("---")
st.metric(label="إجمالي المهام المنجزة اليوم", value=st.session_state.done_count)
