import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="M7 Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 M7 Chatbot")
st.caption("🚀 نموذج شات بوت تفاعلي جاهز")

# تهيئة سجل المحادثة في الـ Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "أهلاً بك! كيف يمكنني مساعدتك اليوم؟"}
    ]

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# استقبال مدخلات المستخدم
if user_input := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم للسجل وعرضها
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # رد تجريبي تلقائي من البوت
    bot_response = f"أهلاً بك! استلمت رسالتك: '{user_input}'"
    
    # إضافة رد البوت للسجل وعرضه
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)
