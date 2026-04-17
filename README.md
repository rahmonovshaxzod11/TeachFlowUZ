# 🎓 TeachFlowUZ
**Pedagogika bo'yicha Zamonaviy Ta'lim Platformasi**

TeachFlowUZ — o'zida sun'iy intellekt imkoniyatlarini mujassam etgan ilg'or ta'lim jarayonlarini boshqarish tizimi (LMS) bo'lib, o'quvchilarga interaktiv ta'lim berish, test ishlatish va ular yuborgan har qanday hujjat yoxud videolarni sun'iy intellekt orqali mustaqil baholash imkonini yaratadi.

![TeachFlowUZ Banner](https://img.shields.io/badge/Status-Beta-success) ![Python](https://img.shields.io/badge/Python-3.13-blue) ![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey) ![AI](https://img.shields.io/badge/AI-Gemma_4_&_DeepSeek_R1-orange)

---

## 🌟 Asosiy Imkoniyatlar

- **📚 Modul va Darslar tizimi:** Pedagogik mavzular bo'yicha ketma-ketlikdagi video-darsliklar.
- **📝 Interfaol Testlar:** Har bir darslikdan so'ng bilimni mustahkamlash uchun mo'ljallangan sinovlar.
- **🤖 AI Assistent Baholashi:** Talabalar topshirgan Word, PDF, Powerpoint va hatto Video formatdagi materiallarni AI vositasida (DeepSeek-R1 va Gemma-4 AI) chuqur tahlil qilib, 0-100 ball shkalada baholash hamda to'liq feedback (kuchli, zaif tomonlari, maslahatlar) berish tizimi.
- **👥 Foydalanuvchi Rollari (User Management):** Tizimga odatiy o'quvchi sifatida ro'yxatdan o'tish yoki Admin huquqi orqali tizimni boshqarish.
- **⚙️ To'liq Admin Panel:** Yangi modullar qo'shish, darslik yuklash, testlar yozish va vazifalarni boshqarish.
- **🌙 Premium Dark Dizayn:** Ko'zni charchatmaslik uchun ishlab chiqilgan zamonaviy 'Dark Mode' va Glassmorphism detallari.

---

## 🚀 O'rnatish va Ishga Tushirish (Mahalliy - Local)

O'z kompyuteringizda platformani ishga tushirish uchun quyidagi qadamlarni bajaring:

### 1-qadam: Repozitoriyni nusxalash (Clone)
```bash
git clone https://github.com/rahmonovshaxzod11/TeachFlowUZ.git
cd TeachFlowUZ
```

### 2-qadam: Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3-qadam: AI uchun Token kiritish
Platforma AI bilan ishlashi uchun Hugging Face API Token kerak. Atrof-muhit o'zgaruvchisiga (Environment Variable) kalitni qo'shing:
- **Windows (CMD):** `set HUGGINGFACE_API_KEY=sizning_tokeningiz`
- **Linux/Mac/PowerShell:** `export HUGGINGFACE_API_KEY=sizning_tokeningiz`

### 4-qadam: Dasturni ishga tushirish
```bash
python app.py
```
Dastur ishga tushgach brauzerda **[http://127.0.0.1:5000](http://127.0.0.1:5000)** web-sahifasiga kiring.

---

## ☁️ Internetga Joylash (Deployment - Railway orqali)

Ushbu dastur to'liq PaaS (Platform as a Service) platformalar, jumladan [Railway](https://railway.app) ga joylashga moslashtirilgan.
Undagi `Procfile` fayl va tayyor muhit o'zgaruvchilari avtomatik tushuniladi. 

Railway'da ishga tushirish uchun maxsus ko'rsatma:
1. Railway portalidan **Deploy from GitHub repository** qiling.
2. TeachFlowUZ reposini tanlang.
3. Loyiha yaralib ishga tushgunga qadar ichki menudan `Variables` menyusiga kirib, **HUGGINGFACE_API_KEY** tokenini qo'shib saqlang. Server qayta ishga tushadi.
4. Settings menyusidan bepul Domain Generate qilib oling!

---

## 🔐 Avtorizatsiya

Platformada Namuna (Seed) fayllari asosida tayyor tizim yaratiladi. Default administrator akkaunti:
> **Login:** `Aziza`
> **Parol:** `Aziza750`

(Tizim orqali qolgan foydalanuvchilar o'zlari erkin ro'yxatdan o'tishlari mumkin).

---

## 🛠 Texnologiyalar Steki (Tech Stack)

- **Backend:** Python, Flask, Flask-Login, SQLAlchemy
- **Ma'lumotlar Bazasi:** SQLite
- **Frontend Tizimi:** HTML5, CSS3 (Custom Dark Mode), JavaScript (AJAX va Animatsiyalar uchun)
- **Fayl prosesing (Data Extract):** PyPDF2, python-docx, python-pptx, OpenCV(cv2), Pillow
- **AI Integratsiya:** Hugging Face Inference API (`google/gemma-4-31B-it` va `deepseek-ai/DeepSeek-R1`)

---
📝 *Loyiha O'quv maqsadida va innovatsion Pedagogika uchun tayyorlangan.*
