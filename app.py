import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io
import database as db

db.init_db()

# إعداد الصفحة
st.set_page_config(
    page_title="قياس أثر التعلّم",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# JavaScript لتعيين اتجاه RTL على مستوى الصفحة
st.markdown("""
<script>
    document.documentElement.setAttribute('dir', 'rtl');
    document.documentElement.setAttribute('lang', 'ar');
    document.body.setAttribute('dir', 'rtl');
</script>
""", unsafe_allow_html=True)

# CSS للتصميم العربي الفخم
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
    
    html, body, .main, .stApp {
        direction: rtl !important;
        text-align: right !important;
    }
    
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    .main .block-container {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* ترتيب الأعمدة من اليمين لليسار */
    [data-testid="column"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        direction: rtl !important;
        flex-direction: row-reverse !important;
    }
    
    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stSidebar"] label {
        direction: rtl !important;
        text-align: right !important;
        display: block !important;
    }
    
    /* عناصر الإدخال */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stSelectbox > div > div {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* القوائم */
    ul, ol {
        direction: rtl !important;
        text-align: right !important;
        padding-right: 20px !important;
        padding-left: 0 !important;
        margin-right: 0 !important;
    }
    
    li {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* الجداول */
    .stDataFrame, table, th, td {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* العناوين والفقرات */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        direction: rtl !important;
    }
    
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 3px solid #d4af37;
    }
    
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo-container {
        width: 100px;
        height: 100px;
    }
    
    .logo-container img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    
    .header-text {
        text-align: center;
        flex-grow: 1;
    }
    
    .header-text h1 {
        color: #d4af37 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-text h2 {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 500 !important;
        margin: 5px 0 !important;
    }
    
    .header-text h3 {
        color: #87CEEB !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        margin: 5px 0 !important;
    }
    
    .platform-title {
        background: linear-gradient(135deg, #d4af37, #f4e4bc, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin: 20px 0;
        text-shadow: none;
    }
    
    .domain-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-right: 5px solid;
        border-left: none !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .domain-card p, .domain-card ul, .domain-card li {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .domain-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .domain-cognitive {
        border-right-color: #2196F3 !important;
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
    }
    
    .domain-educational {
        border-right-color: #4CAF50 !important;
        background: linear-gradient(145deg, #e8f5e9, #c8e6c9);
    }
    
    .domain-behavioral {
        border-right-color: #FF9800 !important;
        background: linear-gradient(145deg, #fff3e0, #ffe0b2);
    }
    
    .domain-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        flex-direction: row-reverse;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .rating-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        margin: 5px;
    }
    
    .rating-excellent {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
    }
    
    .rating-average {
        background: linear-gradient(135deg, #FF9800, #FFB74D);
        color: white;
    }
    
    .rating-below {
        background: linear-gradient(135deg, #f44336, #ef5350);
        color: white;
    }
    
    .teacher-panel {
        background: linear-gradient(135deg, #1a237e, #283593);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2) !important;
    }
    
    .success-button > button {
        background: linear-gradient(135deg, #4CAF50, #66BB6A) !important;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stSelectbox, .stTextInput, .stNumberInput {
        direction: rtl;
    }
    
    .stDataFrame {
        direction: rtl;
    }
    
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .self-assessment-card {
        background: linear-gradient(145deg, #e1f5fe, #b3e5fc);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-right: 4px solid #0288d1;
    }
    
    .report-section {
        background: linear-gradient(145deg, #fafafa, #eeeeee);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #1e3c72;
    }
    
    /* ============================================
       التصميم المتجاوب - الجوال والآيباد والويب
       ============================================ */
    
    /* الشاشات الصغيرة - الجوال (أقل من 768px) */
    @media screen and (max-width: 767px) {
        .header-container {
            padding: 15px !important;
            margin: 10px !important;
            border-radius: 10px !important;
        }
        
        .header-container h1 {
            font-size: 1.3rem !important;
        }
        
        .header-container h2 {
            font-size: 1.1rem !important;
        }
        
        .header-container h3, .header-container h4 {
            font-size: 0.95rem !important;
        }
        
        /* شعار الوزارة على الجوال */
        .header-container > div:first-child {
            position: relative !important;
            top: 0 !important;
            right: 0 !important;
            text-align: center !important;
            margin-bottom: 15px !important;
        }
        
        .header-container > div:first-child img {
            width: 80px !important;
            height: 80px !important;
        }
        
        /* عنوان المنصة */
        .header-container h1[style*="3.5rem"] {
            font-size: 1.8rem !important;
        }
        
        /* البطاقات على الجوال */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        
        .domain-card {
            padding: 15px !important;
            margin: 10px 0 !important;
            border-radius: 12px !important;
        }
        
        .domain-title {
            font-size: 1.2rem !important;
        }
        
        .domain-card p, .domain-card li {
            font-size: 0.9rem !important;
        }
        
        .metric-card {
            padding: 15px !important;
            margin: 8px 0 !important;
        }
        
        .metric-card h3 {
            font-size: 1.5rem !important;
        }
        
        .metric-card h4 {
            font-size: 1rem !important;
        }
        
        /* الأزرار على الجوال */
        .stButton > button {
            width: 100% !important;
            padding: 12px 15px !important;
            font-size: 1rem !important;
        }
        
        /* الشريط الجانبي */
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* حقول الإدخال */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            font-size: 16px !important; /* يمنع التكبير التلقائي على iOS */
            padding: 12px !important;
        }
        
        /* التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap !important;
            gap: 5px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
        }
    }
    
    /* الشاشات المتوسطة - الآيباد (768px - 1024px) */
    @media screen and (min-width: 768px) and (max-width: 1024px) {
        .header-container {
            padding: 20px !important;
        }
        
        .header-container h1 {
            font-size: 1.8rem !important;
        }
        
        .header-container h2 {
            font-size: 1.4rem !important;
        }
        
        .header-container > div:first-child img {
            width: 100px !important;
            height: 100px !important;
        }
        
        .header-container h1[style*="3.5rem"] {
            font-size: 2.5rem !important;
        }
        
        .domain-card {
            padding: 20px !important;
        }
        
        .domain-title {
            font-size: 1.3rem !important;
        }
        
        /* تعديل عدد الأعمدة للآيباد */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        
        [data-testid="column"] {
            min-width: 45% !important;
            margin-bottom: 15px !important;
        }
    }
    
    /* الشاشات الكبيرة - الكمبيوتر (أكثر من 1024px) */
    @media screen and (min-width: 1025px) {
        .header-container {
            max-width: 1200px;
            margin: 0 auto 30px auto !important;
        }
        
        .domain-card {
            min-height: 280px;
        }
    }
    
    /* تحسينات عامة للتفاعل باللمس */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 48px !important;
        }
        
        .stSelectbox > div, .stTextInput > div {
            min-height: 48px !important;
        }
        
        .domain-card:hover {
            transform: none !important;
        }
        
        a, button, [role="button"] {
            min-height: 44px !important;
            min-width: 44px !important;
        }
    }
    
    /* منع التمرير الأفقي */
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* تحسين قراءة النص */
    @media screen and (max-width: 767px) {
        p, li, span {
            line-height: 1.6 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# تهيئة الجلسة
def init_session_state():
    if 'students' not in st.session_state:
        st.session_state.students = {}
    if 'cognitive_criteria' not in st.session_state:
        st.session_state.cognitive_criteria = {
            'الواجبات': 15,
            'التفاعل والمشاركة': 15,
            'المهام الأدائية': 10,
            'درجة الاختبارات': 60
        }
    if 'educational_criteria' not in st.session_state:
        st.session_state.educational_criteria = ['المهارات الحياتية', 'القيم', 'العمل الجماعي', 'المبادرات']
    if 'behavioral_criteria' not in st.session_state:
        st.session_state.behavioral_criteria = ['الانضباط', 'الصدق', 'الاحترام', 'المشاركة الفعالة', 'المسؤولية', 'التعاطف']
    if 'grades' not in st.session_state:
        st.session_state.grades = {}
    if 'self_assessments' not in st.session_state:
        st.session_state.self_assessments = {}
    if 'current_class' not in st.session_state:
        st.session_state.current_class = 1

init_session_state()

# دالة عرض الهيدر الرئيسي
def show_header():
    import base64
    
    def get_base64_image(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    
    logo_base64 = get_base64_image("attached_assets/الشعار_بخلفية_التدرج_1768496730314.png")
    
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="شعار وزارة التعليم" style="width: 80px; height: 80px; object-fit: contain; border-radius: 8px;">'
    else:
        logo_html = '<div style="width: 80px; height: 80px; background: rgba(255,255,255,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem;">الشعار</div>'
    
    st.markdown(f"""
    <div class="header-container" style="position: relative;">
        <div style="position: absolute; top: 15px; right: 15px; z-index: 10;">
            {logo_html}
        </div>
        <div class="header-text" style="text-align: center; padding: 0 100px;">
            <h1 style="color: #ffffff !important; font-size: 2rem !important; font-weight: 800 !important; margin-bottom: 8px !important; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4);">
                المملكة العربية السعودية
            </h1>
            <h2 style="color: #d4af37 !important; font-size: 1.8rem !important; font-weight: 700 !important; margin: 8px 0 !important; letter-spacing: 1px;">
                وزارة التعليم
            </h2>
            <h3 style="color: #87CEEB !important; font-size: 1.4rem !important; font-weight: 600 !important; margin: 8px 0 !important;">
                إدارة تعليم جدة
            </h3>
            <h3 style="color: #ffffff !important; font-size: 1.3rem !important; font-weight: 500 !important; margin: 8px 0 !important;">
                مدرسة معن بن عدي الابتدائية
            </h3>
        </div>
        <div style="margin: 30px 0; text-align: center;">
            <h1 style="background: linear-gradient(135deg, #d4af37, #f4e4bc, #d4af37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3.5rem !important; font-weight: 900 !important; letter-spacing: 3px; text-shadow: none; margin: 0;">
                منصة قياس أثر التعلّم
            </h1>
        </div>
        <div class="header-text" style="text-align: center; margin-top: 20px;">
            <h3 style="color: #ffffff !important; font-size: 1.5rem !important; font-weight: 700 !important; margin: 10px 0 !important; background: rgba(255,255,255,0.1); padding: 10px 25px; border-radius: 25px; display: inline-block;">
                مادة القرآن الكريم والدراسات الإسلامية
            </h3>
            <h4 style="color: #87CEEB !important; font-size: 1.2rem !important; font-weight: 500 !important; margin: 15px 0 !important;">
                الصف السادس الابتدائي
            </h4>
            <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(212, 175, 55, 0.3);">
                <h4 style="color: #d4af37 !important; font-size: 1.3rem !important; font-weight: 700 !important; margin: 0 !important;">
                    إعداد وتصميم
                </h4>
                <h3 style="color: #ffffff !important; font-size: 1.6rem !important; font-weight: 800 !important; margin: 10px 0 0 0 !important; letter-spacing: 1px;">
                    الأستاذ / محمد حسين جابر القحطاني
                </h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# الشريط الجانبي
def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #1e3c72;">🎓 لوحة التحكم</h2>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "اختر القسم:",
            ["🏠 الصفحة الرئيسية", "👨‍🏫 لوحة تحكم المعلم", "📊 المجال المعرفي والعلمي", 
             "🌱 المجال التربوي", "⭐ المجال السلوكي", "✍️ التقييم الذاتي للطالب",
             "📋 التقارير والإرسال"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # اختيار الفصل
        st.markdown("### 📝 اختيار الفصل")
        selected_class = st.selectbox(
            "رقم الفصل:",
            options=list(range(1, 11)),
            format_func=lambda x: f"الفصل {x}",
            key="class_selector"
        )
        st.session_state.current_class = selected_class
        
        st.markdown(f"**الصف:** السادس الابتدائي")
        st.markdown(f"**الفصل المختار:** {selected_class}")
        
        # عدد الطلاب في الفصل الحالي
        students_count = len(db.get_students_by_class(selected_class))
        st.markdown(f"**عدد الطلاب:** {students_count}")
        
        return page

# لوحة تحكم المعلم
def teacher_panel():
    st.markdown("""
    <div class="teacher-panel">
        <h2 style="text-align: center;">👨‍🏫 لوحة تحكم المعلم المتقدمة</h2>
    </div>
    """, unsafe_allow_html=True)
    
    class_key = f"class_{st.session_state.current_class}"
    
    tabs = st.tabs(["📝 إدارة الطلاب", "⚙️ إعدادات المعايير", "📊 استيراد/تصدير البيانات"])
    
    with tabs[0]:
        st.markdown("### إضافة الطلاب")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### إضافة طالب فردي")
            student_name = st.text_input("اسم الطالب:", key="single_student")
            if st.button("➕ إضافة الطالب", key="add_single"):
                if student_name:
                    result = db.add_student(student_name, st.session_state.current_class)
                    if result:
                        st.success(f"تمت إضافة الطالب: {student_name}")
                        st.rerun()
                    else:
                        st.warning("الطالب موجود مسبقاً")
        
        with col2:
            st.markdown("#### إضافة طلاب دفعة واحدة")
            students_bulk = st.text_area("أدخل أسماء الطلاب (كل اسم في سطر):", height=150, key="bulk_students")
            if st.button("➕ إضافة الجميع", key="add_bulk"):
                if students_bulk:
                    names = [name.strip() for name in students_bulk.split('\n') if name.strip()]
                    added = db.add_students_bulk(names, st.session_state.current_class)
                    st.success(f"تمت إضافة {len(added)} طالب")
                    if added:
                        st.rerun()
        
        # عرض قائمة الطلاب
        st.markdown("---")
        st.markdown("### 📋 قائمة طلاب الفصل الحالي")
        
        students_list = db.get_students_by_class(st.session_state.current_class)
        if students_list:
            for i, student in enumerate(students_list):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i+1}. {student}")
                with col2:
                    if st.button("🗑️", key=f"delete_{student}_{i}"):
                        db.delete_student(student, st.session_state.current_class)
                        st.rerun()
        else:
            st.info("لا يوجد طلاب في هذا الفصل بعد")
    
    with tabs[1]:
        st.markdown("### ⚙️ إعدادات معايير المجال المعرفي")
        st.markdown("##### (المجموع الكلي يجب أن يساوي 100 درجة)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### المعايير الحالية")
            total = 0
            for criterion, score in st.session_state.cognitive_criteria.items():
                new_score = st.number_input(
                    f"{criterion}:",
                    min_value=0,
                    max_value=100,
                    value=score,
                    key=f"criterion_{criterion}"
                )
                st.session_state.cognitive_criteria[criterion] = new_score
                total += new_score
            
            st.markdown(f"**المجموع الحالي: {total}/100**")
            if total != 100:
                st.warning("⚠️ المجموع يجب أن يساوي 100")
        
        with col2:
            st.markdown("#### إضافة معيار جديد")
            new_criterion = st.text_input("اسم المعيار الجديد:")
            new_score = st.number_input("الدرجة:", min_value=0, max_value=100, value=10)
            if st.button("➕ إضافة المعيار"):
                if new_criterion and new_criterion not in st.session_state.cognitive_criteria:
                    st.session_state.cognitive_criteria[new_criterion] = new_score
                    st.success(f"تمت إضافة: {new_criterion}")
                    st.rerun()
            
            st.markdown("#### حذف معيار")
            criterion_to_delete = st.selectbox(
                "اختر المعيار للحذف:",
                options=list(st.session_state.cognitive_criteria.keys())
            )
            if st.button("🗑️ حذف المعيار"):
                if criterion_to_delete:
                    del st.session_state.cognitive_criteria[criterion_to_delete]
                    st.success(f"تم حذف: {criterion_to_delete}")
                    st.rerun()
    
    with tabs[2]:
        st.markdown("### 📊 استيراد/تصدير البيانات")
        
        import_tabs = st.tabs(["📤 استيراد الأسماء", "📤 استيراد الأسماء والدرجات", "📥 تصدير البيانات"])
        
        with import_tabs[0]:
            st.markdown("#### رفع ملف Excel للأسماء فقط")
            uploaded_file = st.file_uploader("اختر ملف Excel:", type=['xlsx', 'xls'], key="names_upload")
            
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.write("معاينة البيانات:")
                    st.dataframe(df.head())
                    
                    if st.button("✅ استيراد الأسماء", key="import_names"):
                        if 'الاسم' in df.columns or 'اسم الطالب' in df.columns:
                            col_name = 'الاسم' if 'الاسم' in df.columns else 'اسم الطالب'
                            names = df[col_name].dropna().tolist()
                            if class_key not in st.session_state.students:
                                st.session_state.students[class_key] = []
                            for name in names:
                                if str(name) not in st.session_state.students[class_key]:
                                    st.session_state.students[class_key].append(str(name))
                            st.success(f"تم استيراد {len(names)} طالب")
                        else:
                            st.error("يجب أن يحتوي الملف على عمود 'الاسم' أو 'اسم الطالب'")
                except Exception as e:
                    st.error(f"خطأ في قراءة الملف: {str(e)}")
        
        with import_tabs[1]:
            st.markdown("#### رفع ملف Excel للأسماء والدرجات")
            st.info("يجب أن يحتوي الملف على الأعمدة: اسم الطالب، الواجبات، التفاعل والمشاركة، المهام الأدائية، درجة الاختبارات")
            
            uploaded_grades = st.file_uploader("اختر ملف Excel:", type=['xlsx', 'xls'], key="grades_upload")
            
            if uploaded_grades:
                try:
                    df = pd.read_excel(uploaded_grades)
                    st.write("معاينة البيانات:")
                    st.dataframe(df.head())
                    
                    if st.button("✅ استيراد الأسماء والدرجات", key="import_grades"):
                        name_col = None
                        if 'الاسم' in df.columns:
                            name_col = 'الاسم'
                        elif 'اسم الطالب' in df.columns:
                            name_col = 'اسم الطالب'
                        
                        if name_col:
                            if class_key not in st.session_state.students:
                                st.session_state.students[class_key] = []
                            
                            imported = 0
                            for _, row in df.iterrows():
                                name = str(row[name_col])
                                if name and name not in st.session_state.students[class_key]:
                                    st.session_state.students[class_key].append(name)
                                
                                grade_key = f"{class_key}_{name}_cognitive"
                                if grade_key not in st.session_state.grades:
                                    st.session_state.grades[grade_key] = {}
                                
                                for criterion in st.session_state.cognitive_criteria.keys():
                                    if criterion in df.columns:
                                        try:
                                            value = int(row[criterion])
                                            st.session_state.grades[grade_key][criterion] = value
                                        except:
                                            pass
                                imported += 1
                            
                            st.success(f"تم استيراد بيانات {imported} طالب")
                        else:
                            st.error("يجب أن يحتوي الملف على عمود 'الاسم' أو 'اسم الطالب'")
                except Exception as e:
                    st.error(f"خطأ في قراءة الملف: {str(e)}")
            
            st.markdown("---")
            st.markdown("#### 📥 تحميل قالب Excel")
            template_data = {
                'اسم الطالب': ['طالب 1', 'طالب 2', 'طالب 3']
            }
            for criterion, max_score in st.session_state.cognitive_criteria.items():
                template_data[criterion] = [0, 0, 0]
            
            template_df = pd.DataFrame(template_data)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                template_df.to_excel(writer, index=False, sheet_name='قالب الدرجات')
            st.download_button(
                label="⬇️ تحميل قالب Excel",
                data=buffer.getvalue(),
                file_name="قالب_الدرجات.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_template"
            )
        
        with import_tabs[2]:
            st.markdown("#### 📥 تصدير البيانات")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("تصدير قائمة الطلاب فقط", key="export_names"):
                    if class_key in st.session_state.students and st.session_state.students[class_key]:
                        df = pd.DataFrame({'اسم الطالب': st.session_state.students[class_key]})
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False, sheet_name='الطلاب')
                        st.download_button(
                            label="⬇️ تحميل الملف",
                            data=buffer.getvalue(),
                            file_name=f"طلاب_الفصل_{st.session_state.current_class}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_names"
                        )
                    else:
                        st.warning("لا يوجد طلاب للتصدير")
            
            with col2:
                if st.button("تصدير التقرير الشامل", key="export_full"):
                    if class_key in st.session_state.students and st.session_state.students[class_key]:
                        report_data = []
                        for student in st.session_state.students[class_key]:
                            row = {'اسم الطالب': student}
                            
                            cog_key = f"{class_key}_{student}_cognitive"
                            if cog_key in st.session_state.grades:
                                for criterion in st.session_state.cognitive_criteria.keys():
                                    row[criterion] = st.session_state.grades[cog_key].get(criterion, 0)
                                row['مجموع المعرفي'] = sum(st.session_state.grades[cog_key].values())
                            else:
                                for criterion in st.session_state.cognitive_criteria.keys():
                                    row[criterion] = 0
                                row['مجموع المعرفي'] = 0
                            
                            edu_key = f"{class_key}_{student}_educational"
                            if edu_key in st.session_state.grades:
                                ratings = list(st.session_state.grades[edu_key].values())
                                if ratings.count("متميز") > len(ratings) / 2:
                                    row['المجال التربوي'] = 'متميز'
                                elif ratings.count("دون المتوسط") > len(ratings) / 2:
                                    row['المجال التربوي'] = 'دون المتوسط'
                                else:
                                    row['المجال التربوي'] = 'متوسط'
                            else:
                                row['المجال التربوي'] = '-'
                            
                            behav_key = f"{class_key}_{student}_behavioral"
                            if behav_key in st.session_state.grades:
                                ratings = list(st.session_state.grades[behav_key].values())
                                if ratings.count("متميز") > len(ratings) / 2:
                                    row['المجال السلوكي'] = 'متميز'
                                elif ratings.count("دون المتوسط") > len(ratings) / 2:
                                    row['المجال السلوكي'] = 'دون المتوسط'
                                else:
                                    row['المجال السلوكي'] = 'متوسط'
                            else:
                                row['المجال السلوكي'] = '-'
                            
                            report_data.append(row)
                        
                        df = pd.DataFrame(report_data)
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False, sheet_name='التقرير الشامل')
                        st.download_button(
                            label="⬇️ تحميل التقرير الشامل",
                            data=buffer.getvalue(),
                            file_name=f"تقرير_الفصل_{st.session_state.current_class}_شامل.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_full_report"
                        )
                    else:
                        st.warning("لا يوجد طلاب للتصدير")

# المجال المعرفي والعلمي
def cognitive_domain():
    st.markdown("""
    <div class="domain-card domain-cognitive">
        <div class="domain-title">📊 المجال المعرفي والعلمي</div>
        <p>تقييم الجانب المعرفي والعلمي للطالب (المجموع الكلي: 100 درجة)</p>
    </div>
    """, unsafe_allow_html=True)
    
    students_list = db.get_students_by_class(st.session_state.current_class)
    
    if not students_list:
        st.warning("الرجاء إضافة طلاب أولاً من لوحة تحكم المعلم")
        return
    
    selected_student = st.selectbox(
        "اختر الطالب:",
        options=students_list,
        key="cognitive_student"
    )
    
    st.markdown("---")
    st.markdown("### إدخال الدرجات")
    
    saved_grades = db.get_cognitive_grades(selected_student, st.session_state.current_class)
    
    total_score = 0
    cols = st.columns(2)
    current_grades = {}
    
    for i, (criterion, max_score) in enumerate(st.session_state.cognitive_criteria.items()):
        with cols[i % 2]:
            current_value = saved_grades.get(criterion, 0)
            score = st.number_input(
                f"{criterion} (من {max_score}):",
                min_value=0,
                max_value=max_score,
                value=current_value,
                key=f"cog_{criterion}_{selected_student}"
            )
            current_grades[criterion] = score
            total_score += score
    
    st.markdown("---")
    
    # عرض النتيجة
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("المجموع الكلي", f"{total_score}/100")
    with col2:
        percentage = (total_score / 100) * 100
        st.metric("النسبة المئوية", f"{percentage:.1f}%")
    with col3:
        if percentage >= 85:
            rating = "متميز"
            color = "rating-excellent"
        elif percentage >= 65:
            rating = "متوسط"
            color = "rating-average"
        else:
            rating = "دون المتوسط"
            color = "rating-below"
        st.markdown(f'<span class="rating-badge {color}">{rating}</span>', unsafe_allow_html=True)
    
    if st.button("💾 حفظ الدرجات", key="save_cognitive"):
        db.save_cognitive_grades(selected_student, st.session_state.current_class, current_grades)
        st.success("تم حفظ الدرجات في قاعدة البيانات بنجاح!")

# المجال التربوي
def educational_domain():
    st.markdown("""
    <div class="domain-card domain-educational">
        <div class="domain-title">🌱 المجال التربوي</div>
        <p>تقييم الجانب التربوي والقيمي للطالب</p>
    </div>
    """, unsafe_allow_html=True)
    
    students_list = db.get_students_by_class(st.session_state.current_class)
    
    if not students_list:
        st.warning("الرجاء إضافة طلاب أولاً من لوحة تحكم المعلم")
        return
    
    selected_student = st.selectbox(
        "اختر الطالب:",
        options=students_list,
        key="edu_student"
    )
    
    st.markdown("---")
    st.markdown("### التقييم التربوي")
    
    saved_grades = db.get_educational_grades(selected_student, st.session_state.current_class)
    
    rating_options = ["متميز", "متوسط", "دون المتوسط"]
    current_ratings = {}
    
    cols = st.columns(2)
    for i, criterion in enumerate(st.session_state.educational_criteria):
        with cols[i % 2]:
            current_value = saved_grades.get(criterion, "متوسط")
            rating = st.selectbox(
                f"{criterion}:",
                options=rating_options,
                index=rating_options.index(current_value) if current_value in rating_options else 1,
                key=f"edu_{criterion}_{selected_student}"
            )
            current_ratings[criterion] = rating
    
    st.markdown("---")
    
    # حساب التقييم العام
    ratings = list(current_ratings.values())
    excellent = ratings.count("متميز")
    average = ratings.count("متوسط")
    below = ratings.count("دون المتوسط")
    
    if excellent > average and excellent > below:
        overall = "متميز"
        color = "rating-excellent"
    elif below > excellent and below > average:
        overall = "دون المتوسط"
        color = "rating-below"
    else:
        overall = "متوسط"
        color = "rating-average"
    
    st.markdown("### التقييم العام للمجال التربوي")
    st.markdown(f'<span class="rating-badge {color}" style="font-size: 1.2rem;">{overall}</span>', unsafe_allow_html=True)
    
    if st.button("💾 حفظ التقييم", key="save_educational"):
        db.save_educational_grades(selected_student, st.session_state.current_class, current_ratings)
        st.success("تم حفظ التقييم في قاعدة البيانات بنجاح!")

# المجال السلوكي
def behavioral_domain():
    st.markdown("""
    <div class="domain-card domain-behavioral">
        <div class="domain-title">⭐ المجال السلوكي</div>
        <p>تقييم الجانب السلوكي والأخلاقي للطالب</p>
    </div>
    """, unsafe_allow_html=True)
    
    students_list = db.get_students_by_class(st.session_state.current_class)
    
    if not students_list:
        st.warning("الرجاء إضافة طلاب أولاً من لوحة تحكم المعلم")
        return
    
    selected_student = st.selectbox(
        "اختر الطالب:",
        options=students_list,
        key="behav_student"
    )
    
    st.markdown("---")
    st.markdown("### التقييم السلوكي")
    
    saved_grades = db.get_behavioral_grades(selected_student, st.session_state.current_class)
    
    rating_options = ["متميز", "متوسط", "دون المتوسط"]
    current_ratings = {}
    
    cols = st.columns(2)
    for i, criterion in enumerate(st.session_state.behavioral_criteria):
        with cols[i % 2]:
            current_value = saved_grades.get(criterion, "متوسط")
            rating = st.selectbox(
                f"{criterion}:",
                options=rating_options,
                index=rating_options.index(current_value) if current_value in rating_options else 1,
                key=f"behav_{criterion}_{selected_student}"
            )
            current_ratings[criterion] = rating
    
    st.markdown("---")
    
    # حساب التقييم العام
    ratings = list(current_ratings.values())
    excellent = ratings.count("متميز")
    average = ratings.count("متوسط")
    below = ratings.count("دون المتوسط")
    
    if excellent > average and excellent > below:
        overall = "متميز"
        color = "rating-excellent"
    elif below > excellent and below > average:
        overall = "دون المتوسط"
        color = "rating-below"
    else:
        overall = "متوسط"
        color = "rating-average"
    
    st.markdown("### التقييم العام للمجال السلوكي")
    st.markdown(f'<span class="rating-badge {color}" style="font-size: 1.2rem;">{overall}</span>', unsafe_allow_html=True)
    
    if st.button("💾 حفظ التقييم", key="save_behavioral"):
        db.save_behavioral_grades(selected_student, st.session_state.current_class, current_ratings)
        st.success("تم حفظ التقييم في قاعدة البيانات بنجاح!")

# التقييم الذاتي للطالب
def self_assessment():
    st.markdown("""
    <div class="self-assessment-card">
        <h2 style="color: #0288d1;">✍️ التقييم الذاتي للطالب</h2>
        <p>أجب عن الأسئلة التالية بصدق لتقييم نفسك</p>
    </div>
    """, unsafe_allow_html=True)
    
    students_list = db.get_students_by_class(st.session_state.current_class)
    
    if not students_list:
        st.warning("الرجاء إضافة طلاب أولاً من لوحة تحكم المعلم")
        return
    
    selected_student = st.selectbox(
        "اختر اسمك:",
        options=students_list,
        key="self_student"
    )
    
    st.markdown("---")
    
    saved_assessment = db.get_self_assessment(selected_student, st.session_state.current_class)
    
    # أسئلة التقييم الذاتي
    questions = [
        ("quran", "هل حفظت الجزء المقرر عليك هذا الأسبوع؟", "القرآن الكريم"),
        ("tilawa", "هل أتقنت التلاوة بأحكام التجويد؟", "التلاوة"),
        ("tawheed", "هل فهمت دروس التوحيد هذا الأسبوع؟", "التوحيد"),
        ("hadith", "هل حفظت الأحاديث المقررة؟", "الحديث"),
        ("fiqh", "هل استوعبت أحكام الفقه المطلوبة؟", "الفقه"),
        ("homework", "هل أنجزت جميع واجباتي في الوقت المحدد؟", "الواجبات"),
        ("participation", "هل شاركت بفعالية في الحصة؟", "المشاركة"),
        ("behavior", "هل التزمت بالسلوك الحسن داخل المدرسة؟", "السلوك")
    ]
    
    answers_options = ["نعم، بشكل كامل", "نعم، إلى حد ما", "أحتاج للتحسين"]
    current_answers = {}
    
    cols = st.columns(2)
    for i, (key, question, subject) in enumerate(questions):
        with cols[i % 2]:
            st.markdown(f"**{subject}:**")
            current_value = saved_assessment.get(key, "نعم، إلى حد ما")
            answer = st.radio(
                question,
                options=answers_options,
                index=answers_options.index(current_value) if current_value in answers_options else 1,
                key=f"self_{key}_{selected_student}"
            )
            current_answers[key] = answer
            st.markdown("---")
    
    if st.button("💾 حفظ التقييم الذاتي", key="save_self"):
        db.save_self_assessment(selected_student, st.session_state.current_class, current_answers)
        st.success("تم حفظ تقييمك الذاتي في قاعدة البيانات بنجاح!")
        
        # عرض ملخص
        full = sum(1 for v in current_answers.values() if v == "نعم، بشكل كامل")
        partial = sum(1 for v in current_answers.values() if v == "نعم، إلى حد ما")
        needs = sum(1 for v in current_answers.values() if v == "أحتاج للتحسين")
        
        st.markdown("### ملخص تقييمك:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إتمام كامل", full)
        with col2:
            st.metric("إتمام جزئي", partial)
        with col3:
            st.metric("تحتاج تحسين", needs)

# التقارير والإرسال
def reports_section():
    st.markdown("""
    <div class="report-section">
        <h2 style="color: #1e3c72; text-align: center;">📋 التقارير والإرسال</h2>
    </div>
    """, unsafe_allow_html=True)
    
    students_list = db.get_students_by_class(st.session_state.current_class)
    
    if not students_list:
        st.warning("الرجاء إضافة طلاب أولاً من لوحة تحكم المعلم")
        return
    
    tabs = st.tabs(["📊 تقرير فردي", "📈 تقرير الفصل", "📤 الإرسال والنشر"])
    
    with tabs[0]:
        selected_student = st.selectbox(
            "اختر الطالب:",
            options=students_list,
            key="report_student"
        )
        
        st.markdown(f"### تقرير الطالب: {selected_student}")
        st.markdown(f"**الصف:** السادس الابتدائي | **الفصل:** {st.session_state.current_class}")
        st.markdown("---")
        
        # المجال المعرفي
        cog_grades = db.get_cognitive_grades(selected_student, st.session_state.current_class)
        if cog_grades:
            st.markdown("#### 📊 المجال المعرفي والعلمي")
            total = sum(cog_grades.values())
            for criterion, score in cog_grades.items():
                st.write(f"• {criterion}: {score}")
            percentage = (total / 100) * 100
            if percentage >= 85:
                rating = "متميز"
            elif percentage >= 65:
                rating = "متوسط"
            else:
                rating = "دون المتوسط"
            st.markdown(f"**المجموع:** {total}/100 | **التقدير:** {rating}")
        else:
            st.info("لم يتم إدخال درجات المجال المعرفي بعد")
        
        st.markdown("---")
        
        # المجال التربوي
        edu_grades = db.get_educational_grades(selected_student, st.session_state.current_class)
        if edu_grades:
            st.markdown("#### 🌱 المجال التربوي")
            for criterion, rating in edu_grades.items():
                st.write(f"• {criterion}: {rating}")
        else:
            st.info("لم يتم إدخال تقييم المجال التربوي بعد")
        
        st.markdown("---")
        
        # المجال السلوكي
        behav_grades = db.get_behavioral_grades(selected_student, st.session_state.current_class)
        if behav_grades:
            st.markdown("#### ⭐ المجال السلوكي")
            for criterion, rating in behav_grades.items():
                st.write(f"• {criterion}: {rating}")
        else:
            st.info("لم يتم إدخال تقييم المجال السلوكي بعد")
        
        # التقييم النهائي
        st.markdown("---")
        st.markdown("### 🏆 التقييم النهائي الشامل")
        
        # حساب التقييم النهائي
        final_ratings = []
        
        if cog_grades:
            total = sum(cog_grades.values())
            percentage = (total / 100) * 100
            if percentage >= 85:
                final_ratings.append("متميز")
            elif percentage >= 65:
                final_ratings.append("متوسط")
            else:
                final_ratings.append("دون المتوسط")
        
        if edu_grades:
            ratings = list(edu_grades.values())
            if ratings.count("متميز") > len(ratings) / 2:
                final_ratings.append("متميز")
            elif ratings.count("دون المتوسط") > len(ratings) / 2:
                final_ratings.append("دون المتوسط")
            else:
                final_ratings.append("متوسط")
        
        if behav_grades:
            ratings = list(behav_grades.values())
            if ratings.count("متميز") > len(ratings) / 2:
                final_ratings.append("متميز")
            elif ratings.count("دون المتوسط") > len(ratings) / 2:
                final_ratings.append("دون المتوسط")
            else:
                final_ratings.append("متوسط")
        
        if final_ratings:
            if final_ratings.count("متميز") > len(final_ratings) / 2:
                final = "متميز"
                color = "rating-excellent"
            elif final_ratings.count("دون المتوسط") > len(final_ratings) / 2:
                final = "دون المتوسط"
                color = "rating-below"
            else:
                final = "متوسط"
                color = "rating-average"
            
            st.markdown(f'<div style="text-align: center;"><span class="rating-badge {color}" style="font-size: 1.5rem;">{final}</span></div>', unsafe_allow_html=True)
        else:
            st.info("لم يتم إدخال أي تقييمات بعد")
    
    with tabs[1]:
        st.markdown("### 📈 تقرير الفصل الشامل")
        
        if students_list:
            report_data = []
            for student in students_list:
                row = {'اسم الطالب': student}
                
                # المجال المعرفي
                cog_grades = db.get_cognitive_grades(student, st.session_state.current_class)
                if cog_grades:
                    row['المجال المعرفي'] = sum(cog_grades.values())
                else:
                    row['المجال المعرفي'] = '-'
                
                # المجال التربوي
                edu_grades = db.get_educational_grades(student, st.session_state.current_class)
                if edu_grades:
                    ratings = list(edu_grades.values())
                    if ratings.count("متميز") > len(ratings) / 2:
                        row['المجال التربوي'] = 'متميز'
                    elif ratings.count("دون المتوسط") > len(ratings) / 2:
                        row['المجال التربوي'] = 'دون المتوسط'
                    else:
                        row['المجال التربوي'] = 'متوسط'
                else:
                    row['المجال التربوي'] = '-'
                
                # المجال السلوكي
                behav_grades = db.get_behavioral_grades(student, st.session_state.current_class)
                if behav_grades:
                    ratings = list(behav_grades.values())
                    if ratings.count("متميز") > len(ratings) / 2:
                        row['المجال السلوكي'] = 'متميز'
                    elif ratings.count("دون المتوسط") > len(ratings) / 2:
                        row['المجال السلوكي'] = 'دون المتوسط'
                    else:
                        row['المجال السلوكي'] = 'متوسط'
                else:
                    row['المجال السلوكي'] = '-'
                
                report_data.append(row)
            
            df = pd.DataFrame(report_data)
            st.dataframe(df, use_container_width=True)
            
            # تصدير التقرير
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='تقرير الفصل')
            st.download_button(
                label="⬇️ تحميل تقرير الفصل",
                data=buffer.getvalue(),
                file_name=f"تقرير_الفصل_{st.session_state.current_class}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("لا يوجد طلاب في هذا الفصل")
    
    with tabs[2]:
        st.markdown("### 📤 الإرسال والنشر")
        
        selected_student_send = st.selectbox(
            "اختر الطالب للإرسال:",
            options=students_list,
            key="send_student"
        )
        
        st.markdown("#### اختر المستلمين:")
        col1, col2, col3 = st.columns(3)
        with col1:
            parent = st.checkbox("ولي الأمر", value=True)
        with col2:
            principal = st.checkbox("مدير المدرسة")
        with col3:
            counselor = st.checkbox("المرشد الطلابي")
        
        st.markdown("#### اختر المجالات للإرسال:")
        col1, col2, col3 = st.columns(3)
        with col1:
            send_cognitive = st.checkbox("المجال المعرفي", value=True)
        with col2:
            send_educational = st.checkbox("المجال التربوي", value=True)
        with col3:
            send_behavioral = st.checkbox("المجال السلوكي", value=True)
        
        notes = st.text_area("ملاحظات إضافية:", height=100)
        
        if st.button("📤 إرسال التقرير", key="send_report"):
            recipients = []
            if parent:
                recipients.append("ولي الأمر")
            if principal:
                recipients.append("مدير المدرسة")
            if counselor:
                recipients.append("المرشد الطلابي")
            
            if recipients:
                st.success(f"تم إرسال تقرير الطالب {selected_student_send} إلى: {', '.join(recipients)}")
                st.info("ملاحظة: يمكنك تصدير التقرير كملف PDF أو Excel ومشاركته عبر البريد الإلكتروني أو الواتساب")
            else:
                st.warning("الرجاء اختيار مستلم واحد على الأقل")

# الصفحة الرئيسية
def home_page():
    show_header()
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #1e3c72;">مرحباً بكم في منصة قياس أثر التعلّم</h2>
        <p style="font-size: 1.2rem; color: #555;">منصة متكاملة لقياس الأثر التعليمي والتربوي والسلوكي لطلاب الصف السادس الابتدائي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # البطاقات الثلاث
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="domain-card domain-cognitive">
            <div class="domain-title">📊 المجال المعرفي والعلمي</div>
            <p>قياس التحصيل العلمي والمعرفي من خلال:</p>
            <ul>
                <li>الواجبات والتكليفات</li>
                <li>التفاعل والمشاركة</li>
                <li>المهام الأدائية</li>
                <li>الاختبارات</li>
            </ul>
            <p><strong>المجموع: 100 درجة</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="domain-card domain-educational">
            <div class="domain-title">🌱 المجال التربوي</div>
            <p>تقييم الجوانب التربوية والقيمية:</p>
            <ul>
                <li>المهارات الحياتية</li>
                <li>القيم والمبادئ</li>
                <li>العمل الجماعي</li>
                <li>المبادرات</li>
            </ul>
            <p><strong>التقييم: متميز / متوسط / دون المتوسط</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="domain-card domain-behavioral">
            <div class="domain-title">⭐ المجال السلوكي</div>
            <p>متابعة السلوكيات والأخلاق:</p>
            <ul>
                <li>الانضباط والالتزام</li>
                <li>الصدق والأمانة</li>
                <li>الاحترام والتعاون</li>
                <li>المسؤولية والتعاطف</li>
            </ul>
            <p><strong>التقييم: متميز / متوسط / دون المتوسط</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ميزات المنصة
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h3 style="color: #1e3c72;">✨ مميزات المنصة</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>👨‍🏫</h3>
            <h4>لوحة تحكم متقدمة</h4>
            <p>إدارة شاملة للمعلم</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊</h3>
            <h4>تقارير شاملة</h4>
            <p>تقارير فردية وجماعية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>✍️</h3>
            <h4>تقييم ذاتي</h4>
            <p>نظام للتقييم الذاتي</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📤</h3>
            <h4>مشاركة التقارير</h4>
            <p>إرسال لأولياء الأمور</p>
        </div>
        """, unsafe_allow_html=True)

# التطبيق الرئيسي
def main():
    page = show_sidebar()
    
    if page == "🏠 الصفحة الرئيسية":
        home_page()
    elif page == "👨‍🏫 لوحة تحكم المعلم":
        show_header()
        teacher_panel()
    elif page == "📊 المجال المعرفي والعلمي":
        show_header()
        cognitive_domain()
    elif page == "🌱 المجال التربوي":
        show_header()
        educational_domain()
    elif page == "⭐ المجال السلوكي":
        show_header()
        behavioral_domain()
    elif page == "✍️ التقييم الذاتي للطالب":
        show_header()
        self_assessment()
    elif page == "📋 التقارير والإرسال":
        show_header()
        reports_section()

if __name__ == "__main__":
    main()
