# منصة قياس أثر التعلّم

## طريقة النشر على Streamlit Cloud

### الخطوة 1: إنشاء حساب GitHub
1. اذهب إلى https://github.com
2. أنشئ حساب جديد

### الخطوة 2: رفع الملفات
1. أنشئ مستودع جديد (New repository)
2. ارفع جميع ملفات هذا المجلد

### الخطوة 3: إعداد قاعدة البيانات
**مهم جداً:** يجب إنشاء قاعدة بيانات PostgreSQL مجانية

#### خيار 1: Neon (مجاني)
1. اذهب إلى https://neon.tech
2. أنشئ مشروع جديد
3. انسخ رابط الاتصال (DATABASE_URL)

#### خيار 2: Supabase (مجاني)
1. اذهب إلى https://supabase.com
2. أنشئ مشروع جديد
3. من Settings > Database انسخ URI

### الخطوة 4: النشر على Streamlit Cloud
1. اذهب إلى https://share.streamlit.io
2. سجل دخول بحساب GitHub
3. اضغط "New app"
4. اختر المستودع
5. **مهم:** اضغط "Advanced settings"
6. أضف السر التالي:
   - Key: `DATABASE_URL`
   - Value: رابط قاعدة البيانات من الخطوة 3
7. اضغط Deploy

## الملفات المطلوبة
- app.py (التطبيق)
- database.py (قاعدة البيانات)
- requirements.txt (المتطلبات)
- .streamlit/config.toml (الإعدادات)
- attached_assets/ (الشعار)

## مدرسة معن بن عدي الابتدائية
إعداد: الأستاذ محمد حسين جابر القحطاني
