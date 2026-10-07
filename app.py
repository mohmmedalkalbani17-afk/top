import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(page_title="حلول الرياضيات الذكية 🧮", page_icon="🧮", layout="centered")

st.title("🧮 المعلم الذكي لحل المسائل والمعادلات الرياضية")
st.write("أدخل المعادلة أو المسألة الرياضية باللغة العربية وسأقوم بحلها مع شرح الخطوات بالتفصيل!")

# قراءة مفتاح الـ API من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ لم يتم العثور على مفتاح GEMINI_API_KEY. يرجى إضافته في إعدادات Secrets على Streamlit Cloud.")
    st.stop()

# إنشاء العميل
client = genai.Client(api_key=api_key)

# تعليمات توجيه البوت (System Instructions)
SYSTEM_INSTRUCTION = """
أنت معلم رياضيات خبير ومساعد ذكي.
مهمتك:
1. حل المعادلة أو المسألة الرياضية المطلوبة بدقة متناهية.
2. تقديم الشرح والخطوات باللغة العربية الواضحة وبشكل منظم ومبسط.
3. استخدام تنسيق LaTeX للرموز والمعادلات الرياضية (مثل $x^2 + 5x + 6 = 0$) لتظهر بشكل منسق وواضح.
4. إذا كانت المسألة تحتوي على أكثر من خطوة، قم بتقديم الحل على شكل خطوات ترقيمية متسلسلة.
"""

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال المسألة الرياضية من المستخدم
if prompt := st.chat_input("اكتب المعادلة هنا (مثال: احسب سين: 2x + 5 = 15)..."):
    # عرض سؤال المستخدم
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # إرسال الطلب إلى Gemini مع التوجيهات
    with st.spinner("جاري حل المسألة وكتابة الخطوات... ⏳"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{SYSTEM_INSTRUCTION}\n\nالمسألة المطلوبة:\n{prompt}",
            )
            
            answer = response.text

            # عرض رد البوت
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")

