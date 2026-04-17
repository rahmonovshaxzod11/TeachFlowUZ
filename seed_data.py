"""
TeachFlowUZ — Seed Data
Namuna modullar, darslar, testlar va topshiriqlar
"""

from models import db, Module, Lesson, Test, Assignment, User


def seed_database():
    """Ma'lumotlar bazasini namuna ma'lumotlar bilan to'ldirish"""

    # Admin foydalanuvchi yaratish
    admin_user = User.query.filter_by(username='Aziza').first()
    if not admin_user:
        admin_user = User(username='Aziza', role='admin')
        admin_user.set_password('Aziza750')
        db.session.add(admin_user)
        db.session.commit()
    
    # Agar ma'lumot mavjud bo'lsa, qaytadan qo'shmaymiz
    if Module.query.first():
        print("Ma'lumotlar allaqachon mavjud. Seed o'tkazib yuborildi.")
        return

    # ═══════════════════════════════════════════════════════
    # MODUL 1: Pedagogika Asoslari
    # ═══════════════════════════════════════════════════════
    module1 = Module(
        title="Pedagogika Asoslari",
        description="Pedagogika fanining nazariy asoslari, ta'lim-tarbiya jarayonining mohiyati, pedagogik faoliyatning asosiy tamoyillari va qonuniyatlari bilan tanishish.",
        icon="📖",
        order=1
    )
    db.session.add(module1)
    db.session.flush()

    # Modul 1 — Darslar
    lessons_m1 = [
        Lesson(
            title="Pedagogikaga Kirish",
            description="Pedagogika fani haqida umumiy tushuncha, uning predmeti, ob'ekti va vazifalari. Pedagogikaning boshqa fanlar bilan aloqasi va o'rni.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="25:00",
            order=1,
            module_id=module1.id
        ),
        Lesson(
            title="Ta'lim Nazariyalari",
            description="Bixeviorizm, konstruktivizm, kognitivizm va gumanistik yondashuvlar. Har bir nazariyaning asosiy g'oyalari va amaliy qo'llanilishi.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="35:00",
            order=2,
            module_id=module1.id
        ),
        Lesson(
            title="O'qitish Tamoyillari",
            description="Didaktik tamoyillar: ilmiylik, tushunarlilik, ko'rgazmalilik, tizimlilik, mustahkamlik. Ularning amaliy qo'llanilishi.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="30:00",
            order=3,
            module_id=module1.id
        ),
    ]
    db.session.add_all(lessons_m1)

    # Modul 1 — Testlar
    tests_m1 = [
        Test(
            question="Pedagogika so'zi qaysi tildan olingan?",
            option_a="Lotin tilidan",
            option_b="Yunon tilidan",
            option_c="Arab tilidan",
            option_d="Fors tilidan",
            correct_answer="b",
            explanation="'Pedagogika' so'zi yunon tilidan olingan bo'lib, 'paidagogos' — bola yetaklovchi degan ma'noni anglatadi.",
            module_id=module1.id
        ),
        Test(
            question="Konstruktivizm nazariyasining asoschilaridan biri kim?",
            option_a="B.F. Skinner",
            option_b="Jan Piaje",
            option_c="Ivan Pavlov",
            option_d="Zigmund Freyd",
            correct_answer="b",
            explanation="Jan Piaje konstruktivizm nazariyasining asoschilaridan biri bo'lib, bolalar bilimni faol ravishda qurishlarini ta'kidlagan.",
            module_id=module1.id
        ),
        Test(
            question="Ko'rgazmalilik tamoyili nimani anglatadi?",
            option_a="O'quvchilarga mustaqil ishlash imkoniyatini berish",
            option_b="O'quv jarayonida barcha sezgi organlarini jalb etish",
            option_c="Darsni aniq rejaga asosan o'tkazish",
            option_d="O'quvchilarni guruhga bo'lib o'qitish",
            correct_answer="b",
            explanation="Ko'rgazmalilik tamoyili o'quv jarayonida ko'rgazmali qurollar yordamida barcha sezgi organlarini jalb etishni nazarda tutadi.",
            module_id=module1.id
        ),
        Test(
            question="Pedagogikaning predmeti nima?",
            option_a="Jamiyatdagi ijtimoiy munosabatlar",
            option_b="Ta'lim-tarbiya jarayoni",
            option_c="Inson psixologiyasi",
            option_d="Madaniyat va san'at",
            correct_answer="b",
            explanation="Pedagogikaning predmeti — ta'lim-tarbiya jarayoni va uning qonuniyatlarini o'rganishdir.",
            module_id=module1.id
        ),
        Test(
            question="Bixeviorizm nazariyasi bo'yicha o'qish bu —",
            option_a="Ichki tafakkur jarayoni",
            option_b="Xulq-atvor o'zgarishi",
            option_c="Ijodiy faoliyat",
            option_d="Ijtimoiy o'zaro ta'sir",
            correct_answer="b",
            explanation="Bixeviorizm nazariyasiga ko'ra, o'qish — bu tashqi stimullar ta'sirida xulq-atvorning o'zgarishidir.",
            module_id=module1.id
        ),
    ]
    db.session.add_all(tests_m1)

    # Modul 1 — Topshiriqlar
    assignments_m1 = [
        Assignment(
            title="Pedagogika Tarixi — Taqdimot",
            description="Pedagogika fanining rivojlanish tarixi haqida taqdimot (PPTX) tayyorlang. Kamida 10 ta slayd bo'lishi kerak. Slaydlarda quyidagilar aks ettirilishi lozim:\n\n1. Qadimgi davrda ta'lim\n2. O'rta asrlarda pedagogik fikrlar\n3. Yangi davr pedagoglari (Komensky, Pestalozzi, Ushinsky)\n4. Zamonaviy pedagogika yo'nalishlari\n5. O'zbekistonda pedagogika fanining rivojlanishi\n\nHar bir slaydda tegishli rasmlar, jadvallar va sxemalar bo'lishi kerak.",
            assignment_type="presentation",
            accepted_formats="pptx,pdf",
            module_id=module1.id
        ),
        Assignment(
            title="Ta'lim Nazariyasi — Esse",
            description="O'zingiz tanlagan bir ta'lim nazariyasi (bixeviorizm, konstruktivizm, kognitivizm yoki gumanistik yondashuv) haqida ilmiy esse yozing (DOCX yoki PDF formatda).\n\nEsseda quyidagilar bo'lishi kerak:\n1. Nazariyaning paydo bo'lish tarixi\n2. Asosiy g'oyalari va tamoyillari\n3. Amaliy qo'llanilishi\n4. Afzalliklari va kamchiliklari\n5. O'zbekiston ta'lim tizimida qo'llanilishi\n\nKamida 1500 so'z. Ilmiy manbalar ko'rsatilishi shart.",
            assignment_type="document",
            accepted_formats="docx,pdf",
            module_id=module1.id
        ),
    ]
    db.session.add_all(assignments_m1)

    # ═══════════════════════════════════════════════════════
    # MODUL 2: Zamonaviy Ta'lim Metodlari
    # ═══════════════════════════════════════════════════════
    module2 = Module(
        title="Zamonaviy Ta'lim Metodlari",
        description="Interfaol, innovatsion va raqamli ta'lim metodlari. Loyiha metodi, muammoli o'qitish, kollaborativ ta'lim va boshqa zamonaviy yondashuvlar.",
        icon="🚀",
        order=2
    )
    db.session.add(module2)
    db.session.flush()

    # Modul 2 — Darslar
    lessons_m2 = [
        Lesson(
            title="Interfaol Ta'lim Metodlari",
            description="Aqliy hujum, klaster, insert, keys, BBB strategiyalari va boshqa interfaol usullar. Ularning darsda qo'llanilishi.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="40:00",
            order=1,
            module_id=module2.id
        ),
        Lesson(
            title="Loyiha Metodi",
            description="Loyihaga asoslangan o'qitish (PBL). Loyiha bosqichlari, o'quvchi va o'qituvchi roli, baholash usullari.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="35:00",
            order=2,
            module_id=module2.id
        ),
        Lesson(
            title="Raqamli Ta'lim Texnologiyalari",
            description="Onlayn ta'lim platformalari, multimedia vositalari, interaktiv doskalar, mobil ilovalar va sun'iy intellektning ta'limdagi o'rni.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="45:00",
            order=3,
            module_id=module2.id
        ),
    ]
    db.session.add_all(lessons_m2)

    # Modul 2 — Testlar
    tests_m2 = [
        Test(
            question="'Aqliy hujum' (brainstorming) metodining asosiy maqsadi nima?",
            option_a="O'quvchilarni tanqidiy baholash",
            option_b="Imkon qadar ko'p g'oyalar generatsiya qilish",
            option_c="O'qituvchi nazoratini kuchaytirish",
            option_d="Yod olish samaradorligini oshirish",
            correct_answer="b",
            explanation="Aqliy hujum metodida asosiy maqsad — tanqidsiz, erkin muhitda imkon qadar ko'p g'oyalar ishlab chiqish.",
            module_id=module2.id
        ),
        Test(
            question="Loyihaga asoslangan o'qitish (PBL) da o'qituvchining asosiy roli qanday?",
            option_a="Ma'ruza o'qish",
            option_b="Fasilitator (yo'naltiruvchi)",
            option_c="Nazoratchi",
            option_d="Baholovchi",
            correct_answer="b",
            explanation="PBL da o'qituvchi fasilitator rolini bajaradi — o'quvchilarni yo'naltiradi, qo'llab-quvvatlaydi, lekin to'g'ridan-to'g'ri javob bermaydi.",
            module_id=module2.id
        ),
        Test(
            question="INSERT strategiyasi nima uchun ishlatiladi?",
            option_a="Guruh ishini tashkil etish",
            option_b="Matn bilan ishlash va tanqidiy o'qish",
            option_c="Matematik masalalarni yechish",
            option_d="Jismoniy mashqlarni o'tkazish",
            correct_answer="b",
            explanation="INSERT — Interactive Noting System for Effective Reading and Thinking. Matnni belgilar bilan o'qib, tanqidiy fikrlashni rivojlantiradi.",
            module_id=module2.id
        ),
        Test(
            question="Flipped classroom (teskari sinf) metodida uy vazifasi sifatida nima beriladi?",
            option_a="Mashqlar va misollar",
            option_b="Yangi mavzuni video orqali o'rganish",
            option_c="Kitob o'qish",
            option_d="Referat yozish",
            correct_answer="b",
            explanation="Teskari sinf metodida o'quvchilar yangi mavzuni uyda video orqali o'rganib, sinfda amaliy mashqlarga vaqt ajratadi.",
            module_id=module2.id
        ),
        Test(
            question="Gamifikatsiya ta'limda nimani anglatadi?",
            option_a="Kompyuter o'yinlari yaratish",
            option_b="O'yin elementlarini ta'lim jarayoniga tatbiq etish",
            option_c="Faqat onlayn o'qitish",
            option_d="Sport mashg'ulotlari o'tkazish",
            correct_answer="b",
            explanation="Gamifikatsiya — o'yin elementlari (ballar, darajalar, mukofotlar)ni ta'lim jarayoniga olib kirish orqali motivatsiyani oshirish.",
            module_id=module2.id
        ),
    ]
    db.session.add_all(tests_m2)

    # Modul 2 — Topshiriqlar
    assignments_m2 = [
        Assignment(
            title="Interfaol Dars Rejasi",
            description="Ixtiyoriy fan bo'yicha interfaol dars rejasi tayyorlang (DOCX yoki PDF formatda).\n\nDars rejasida quyidagilar bo'lishi kerak:\n1. Fan, sinf, mavzu\n2. Dars maqsadlari (ta'limiy, tarbiyaviy, rivojlantiruvchi)\n3. Dars jihozlari\n4. Dars borishi (bosqichlar bo'yicha):\n   - Tashkiliy qism (5 daqiqa)\n   - O'tilgan mavzuni so'rash (10 daqiqa) — interfaol metod bilan\n   - Yangi mavzu bayoni (15 daqiqa) — interfaol metod bilan\n   - Mustahkamlash (10 daqiqa) — interfaol metod bilan\n   - Baholash va uy vazifasi (5 daqiqa)\n5. Kamida 3 ta turli interfaol metod qo'llanilgan bo'lishi kerak",
            assignment_type="document",
            accepted_formats="docx,pdf",
            module_id=module2.id
        ),
    ]
    db.session.add_all(assignments_m2)

    # ═══════════════════════════════════════════════════════
    # MODUL 3: Dars Rejalashtirish va Baholash
    # ═══════════════════════════════════════════════════════
    module3 = Module(
        title="Dars Rejalashtirish va Baholash",
        description="Dars tuzilmasi, maqsad qo'yish (Bloom taksonomiyasi), baholash usullari va mezonlari. Dars tahlili va refleksiya.",
        icon="📝",
        order=3
    )
    db.session.add(module3)
    db.session.flush()

    # Modul 3 — Darslar
    lessons_m3 = [
        Lesson(
            title="Dars Tuzilmasi va Bosqichlari",
            description="Zamonaviy darsning tuzilmasi: motivatsiya, yangi bilim berish, mustahkamlash, baholash. Har bir bosqichning maqsadi va mazmuni.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="30:00",
            order=1,
            module_id=module3.id
        ),
        Lesson(
            title="Bloom Taksonomiyasi",
            description="Bloom taksonomiyasi bo'yicha maqsadlarni qo'yish: bilish, tushunish, qo'llash, tahlil, sintez, baholash. Amaliy misollar.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="35:00",
            order=2,
            module_id=module3.id
        ),
        Lesson(
            title="Baholash Usullari va Mezonlari",
            description="Formativ va summativ baholash. Rubrika tuzish, o'z-o'zini baholash, hamkorlikda baholash usullari.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            duration="40:00",
            order=3,
            module_id=module3.id
        ),
    ]
    db.session.add_all(lessons_m3)

    # Modul 3 — Testlar
    tests_m3 = [
        Test(
            question="Bloom taksonomiyasining eng yuqori darajasi qaysi?",
            option_a="Qo'llash",
            option_b="Tahlil",
            option_c="Yaratish (Sintez)",
            option_d="Baholash",
            correct_answer="c",
            explanation="Yangilangan Bloom taksonomiyasida eng yuqori daraja — 'Yaratish' (Creating), avvalgi versiyada 'Sintez' deb nomlangan.",
            module_id=module3.id
        ),
        Test(
            question="Formativ baholash nima?",
            option_a="Yakuniy imtihon",
            option_b="O'quv jarayonida doimiy kuzatish va qayta aloqa",
            option_c="Attestatsiya bahosi",
            option_d="Yillik baho",
            correct_answer="b",
            explanation="Formativ baholash — bu o'quv jarayonida o'quvchi yutuqlarini doimiy kuzatib borish va qayta aloqa berish orqali ta'limni yaxshilash.",
            module_id=module3.id
        ),
        Test(
            question="Darsning motivatsiya bosqichida nima qilinadi?",
            option_a="Yangi mavzu tushuntiriladi",
            option_b="O'quvchilar qiziqishi uyg'otiladi va dars maqsadi e'lon qilinadi",
            option_c="Uy vazifasi tekshiriladi",
            option_d="Baholar e'lon qilinadi",
            correct_answer="b",
            explanation="Motivatsiya bosqichida o'quvchilarning qiziqishi uyg'otiladi, dars mavzusi va maqsadlari bilan tanishtriladi.",
            module_id=module3.id
        ),
        Test(
            question="Rubrika nima?",
            option_a="Dars rejasi",
            option_b="Baholash mezonlari va darajalari jadvali",
            option_c="O'quv dasturi",
            option_d="Sinf jurnali",
            correct_answer="b",
            explanation="Rubrika — aniq mezonlar va sifat darajalari ko'rsatilgan baholash jadvali bo'lib, ob'ektiv baholashga yordam beradi.",
            module_id=module3.id
        ),
        Test(
            question="SMART maqsad qo'yish texnikasida 'M' harfi nimani anglatadi?",
            option_a="Meaningful (mazmunli)",
            option_b="Measurable (o'lchanadigan)",
            option_c="Motivational (motivatsion)",
            option_d="Modern (zamonaviy)",
            correct_answer="b",
            explanation="SMART = Specific, Measurable, Achievable, Relevant, Time-bound. 'M' = Measurable — maqsad o'lchanadigan bo'lishi kerak.",
            module_id=module3.id
        ),
    ]
    db.session.add_all(tests_m3)

    # Modul 3 — Topshiriqlar
    assignments_m3 = [
        Assignment(
            title="Namuna Dars Ishlanmasi",
            description="O'zingiz tanlagan mavzu bo'yicha to'liq dars ishlanmasi tayyorlang (PPTX formatda taqdimot + DOCX yoki PDF formatda dars rejasi).\n\nDars ishlanmasida quyidagilar bo'lishi kerak:\n1. Bloom taksonomiyasiga asoslangan dars maqsadlari\n2. Darsning har bir bosqichi uchun batafsil faoliyatlar\n3. Qo'llaniladigan interfaol metodlar tavsifi\n4. Baholash rubrikasi\n5. Dars materiallari (slaydlar, tarqatma materiallar)\n\nTaqdimotda kamida 15 ta slayd bo'lishi kerak.",
            assignment_type="presentation",
            accepted_formats="pptx,pdf,docx",
            module_id=module3.id
        ),
        Assignment(
            title="Video Darslik Tayyorlash",
            description="O'zingiz tanlagan pedagogik mavzu bo'yicha 5-10 daqiqalik video darslik tayyorlang (MP4 formatda).\n\nVideo darslikda quyidagilar bo'lishi kerak:\n1. Mavzuning aniq va tushunarli bayoni\n2. Ko'rgazmali materiallar (slaydlar, sxemalar)\n3. Amaliy misollar\n4. Yakuniy xulosa va takrorlash savollari\n\nVideo sifati: kamida 720p. Ovoz aniq va tushunarli bo'lishi kerak.",
            assignment_type="video",
            accepted_formats="mp4,avi,mov",
            module_id=module3.id
        ),
    ]
    db.session.add_all(assignments_m3)

    db.session.commit()
    print("[OK] Namuna ma'lumotlar muvaffaqiyatli qo'shildi!")
    print("   Modullar: 3")
    print("   Darslar: 9")
    print("   Testlar: 15")
    print("   Topshiriqlar: 5")
