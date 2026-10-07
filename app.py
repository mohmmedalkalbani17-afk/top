import os
from google import genai
from google.genai import types

# إعداد العميل
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# تعليمات النظام لضمان حل المسائل الرياضية باللغة العربية
system_instruction = """
أنت خبير ومتخصص في حل جميع المسائل الرياضية بمختلف مستوياتها (جبر، هندسة، تفاضل وتكامل، إحصاء).
اتبع القواعد التالية:
1. اشرك المستخدم بالشرح باللغة العربية الفصحى الواضحة.
2. حدد المعطيات والمطلوب أولاً.
3. حل المسألة خطوة بخطوة مع توضيح القوانين المستخدمة.
4. استخدم رموز LaTeX للمعادلات الرياضية.
5. ضع النتيجة النهائية في السطر الأخير بشكل واضح.
"""

# إنشاء جلسة المحادثة (Chat Session)
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2, # قيمة منخفضة لضمان الدقة الرياضية
    )
)

print("مرحباً بك! أنا مساعدك الرياضي. اكتب مسألتك أو اكتب 'خروج' للإنهاء.\n")

# حلقة التفاعل المستمرة
while True:
    user_input = input("أنت: ")
    
    if user_input.strip().lower() in ["خروج", "exit", "quit"]:
        print("تم إغلاق المحادثة. بالتوفيق!")
        break
        
    if not user_input.strip():
        continue

    # إرسال الرسالة والحصول على الرد ضمن نفس الجلسة
    response = chat.send_message(user_input)
    print(f"\nالبوت:\n{response.text}\n")
    print("-" * 50)
