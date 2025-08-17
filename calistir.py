# calistir.py (TÜM KODLAR BURADA)

import sys
import os
import sqlite3
import hashlib
import qtawesome as qta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QFormLayout, 
    QMessageBox, QScrollArea, QGridLayout, QStackedWidget, QTextBrowser,
    QToolBar, QLineEdit, QCompleter, QDialog, QSizePolicy, QListWidget,
    QListWidgetItem, QSplitter, QFileDialog, QInputDialog, QComboBox, QTextEdit
)
from PyQt6.QtGui import (
    QFont, QPixmap, QCursor, QPalette, QBrush, QColor, QTextCursor, QIcon
)
from PyQt6.QtCore import (
    Qt, QSize, QPoint, QPropertyAnimation, QEasingCurve, QRect, 
    QStringListModel, pyqtSignal
)

#==============================================================================
# STIL KODLARI (STYLES)
#==============================================================================
LIGHT_THEME_QSS = """
    QDialog, QWidget { 
        background-color: #f3f3f3; 
        color: #202020; 
        border: none; 
        font-family: "Segoe UI";
        font-size: 15px; 
    }
    #MainWindow, #YoneticiPaneli, QTextBrowser { 
        background-color: #ffffff; 
    }
    #LeftPanel, #RightPanel { 
        background-color: #f8f8f8; 
    }
    #LeftPanel { border-right: 1px solid #e1e1e1; }
    #RightPanel { border-left: 1px solid #e1e1e1; }
    QTreeView { background-color: #f8f8f8; border: none; }
    QTreeView::item { padding: 12px; border-radius: 5px; }
    QTreeView::item:hover { background-color: #e1e1e1; }
    QTreeView::item:selected { background-color: #0078d7; color: #ffffff; }
    QLineEdit, QTextEdit, QPushButton, QComboBox { 
        border: 1px solid #cccccc; border-radius: 8px; padding: 12px; 
        background-color: #ffffff; color: #202020;
    }
    QPushButton { font-weight: bold; background-color: #e8e8f8; }
    QPushButton:hover { background-color: #dcdcdc; border-color: #bbbbbb; }
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus { 
        border: 2px solid #0078d7; padding: 11px; 
    }
    QToolBar { background-color: #ffffff; border-bottom: 1px solid #e1e1e1; padding: 5px; }
    QToolBar QLineEdit { padding: 8px 12px; }
    QCompleter QAbstractItemView { font-family: "Segoe UI"; font-size: 15px; background-color: #ffffff; border: 1px solid #e1e1e1; border-radius: 6px; padding: 5px; }
    QCompleter QAbstractItemView::item { padding: 10px; border-radius: 4px; }
    QCompleter QAbstractItemView::item:selected, QCompleter QAbstractItemView::item:hover { background-color: #0078d7; color: #ffffff; }
    #TitleBar { background-color: #f0f0f0; }
    #TitleBar QLabel { font-weight: bold; }
    #TitleBar QPushButton { border: none; background-color: transparent; padding: 8px; }
    #TitleBar QPushButton:hover { background-color: #dcdcdc; }
    #CloseButton:hover { background-color: #e81123; color: white; }
"""
DARK_THEME_QSS = ""

#==============================================================================
# YARDIMCI FONKSİYON
#==============================================================================
def sifre_hashle(sifre): 
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()

#==============================================================================
# ÖZEL ARAYÜZ BİLEŞENLERİ (WIDGETS)
#==============================================================================
class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("TitleBar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.book-dead').pixmap(QSize(16, 16)))
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addSpacing(10)
        self.title_label = QLabel("Tarih Arşivi")
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()
        minimize_button = QPushButton()
        minimize_button.setIcon(qta.icon('fa5s.window-minimize'))
        minimize_button.clicked.connect(self.parent.showMinimized)
        maximize_button = QPushButton()
        maximize_button.setIcon(qta.icon('fa5s.window-maximize'))
        maximize_button.clicked.connect(self.toggle_maximize)
        close_button = QPushButton()
        close_button.setObjectName("CloseButton")
        close_button.setIcon(qta.icon('fa5s.times'))
        close_button.clicked.connect(self.parent.close)
        layout.addWidget(minimize_button)
        layout.addWidget(maximize_button)
        layout.addWidget(close_button)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.parent.old_pos)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.old_pos = event.globalPosition().toPoint()

class DergiKarti(QWidget):
    def __init__(self, dergi_id, ad, kapak_yolu, parent=None):
        super().__init__(parent)
        self.dergi_id = dergi_id
        self.setFixedSize(180, 280)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout = QVBoxLayout(self)
        self.kapak_label = QLabel()
        self.kapak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if kapak_yolu and os.path.exists(kapak_yolu):
            pixmap = QPixmap(kapak_yolu)
        else:
            pixmap = QPixmap()
            self.kapak_label.setText("Kapak\nResmi\nYok")
        self.kapak_label.setPixmap(pixmap.scaled(160, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.ad_label = QLabel(ad)
        self.ad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ad_label.setWordWrap(True)
        font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self.ad_label.setFont(font)
        layout.addWidget(self.kapak_label)
        layout.addWidget(self.ad_label)
        self.setup_animations()

    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def enterEvent(self, event):
        self.animation.stop()
        start_rect = self.geometry()
        end_rect = QRect(start_rect.x() - 5, start_rect.y() - 5, start_rect.width() + 10, start_rect.height() + 10)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        start_rect = self.geometry()
        end_rect = QRect(start_rect.x() + 5, start_rect.y() + 5, start_rect.width() - 10, start_rect.height() - 10)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        super().leaveEvent(event)

#==============================================================================
# KAYIT PENCERESİ
#==============================================================================
class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Üye Kaydı")
        self.setFixedSize(350, 250)
        self.setFont(QFont("Segoe UI", 11))
        self.setModal(True)
        layout = QVBoxLayout(self)
        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.sifre_tekrar_input = QLineEdit()
        self.sifre_tekrar_input.setPlaceholderText("Şifre (Tekrar)")
        self.sifre_tekrar_input.setEchoMode(QLineEdit.EchoMode.Password)
        register_button = QPushButton("Kayıt Ol")
        register_button.clicked.connect(self.kayit_olmayi_dene)
        layout.addWidget(QLabel("Yeni Hesap Oluştur:"))
        layout.addWidget(self.kullanici_adi_input)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.sifre_tekrar_input)
        layout.addWidget(register_button)

    def kayit_olmayi_dene(self):
        k_adi = self.kullanici_adi_input.text()
        sifre1 = self.sifre_input.text()
        sifre2 = self.sifre_tekrar_input.text()
        if not k_adi or not sifre1 or not sifre2:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        if sifre1 != sifre2:
            QMessageBox.warning(self, "Hata", "Girdiğiniz şifreler uyuşmuyor.")
            return
        try:
            baglanti = sqlite3.connect('tarih_makaleleri.db')
            cursor = baglanti.cursor()
            cursor.execute("SELECT id FROM kullanicilar WHERE kullanici_adi = ?", (k_adi,))
            if cursor.fetchone() is not None:
                QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten alınmış.")
                baglanti.close()
                return
            hashlenmis_sifre = sifre_hashle(sifre1)
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre_hash, rol) VALUES (?, ?, ?)", (k_adi, hashlenmis_sifre, 'okuyucu'))
            baglanti.commit()
            baglanti.close()
            QMessageBox.information(self, "Başarılı", f"'{k_adi}' adlı kullanıcı oluşturuldu. Şimdi giriş yapabilirsiniz.")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Bir hata oluştu: {e}")

#==============================================================================
# GİRİŞ PANELİ
#==============================================================================
class GirisPaneli(QWidget):
    login_basarili = pyqtSignal(str)
    misafir_girisi = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setObjectName("GirisPaneli")
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            QLineEdit { background-color: white; color: #202020; border: 1px solid #cccccc; border-radius: 8px; padding: 12px; font-size: 16px; }
            QLineEdit:focus { border: 2px solid #0078d7; }
            QPushButton { padding: 12px; border-radius: 8px; font-size: 16px; font-weight: bold; }
            #LoginButton { background-color: #0078d7; color: white; border:none; } #LoginButton:hover { background-color: #005a9e; }
            #GuestButton, #RegisterButton { background-color: white; color: #202020; border: 1px solid #cccccc; }
            #GuestButton:hover, #RegisterButton:hover { background-color: #f0f0f0; }
        """)
        main_layout = QVBoxLayout(self)
        form_layout = QVBoxLayout()
        form_layout.addStretch(2)
        title = QLabel("Tarih Arşivi")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #444444; background: transparent;")
        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.EchoMode.Password)
        login_button = QPushButton("Giriş Yap")
        login_button.setObjectName("LoginButton")
        register_button = QPushButton("Üye Ol")
        register_button.setObjectName("RegisterButton")
        misafir_button = QPushButton("Misafir Olarak Devam Et")
        misafir_button.setObjectName("GuestButton")
        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.kullanici_adi_input)
        form_layout.addWidget(self.sifre_input)
        form_layout.addSpacing(20)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button)
        form_layout.addWidget(misafir_button)
        form_layout.addStretch(3)
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        container_widget = QWidget()
        container_widget.setLayout(form_layout)
        container_widget.setMaximumWidth(400)
        h_layout.addWidget(container_widget)
        h_layout.addStretch(1)
        main_layout.addLayout(h_layout, 1)
        login_button.clicked.connect(self.giris_yapmayi_dene)
        misafir_button.clicked.connect(self.misafir_olarak_gir)
        register_button.clicked.connect(self.uye_ol_penceresi_ac)
        self.kullanici_adi_input.returnPressed.connect(self.giris_yapmayi_dene)
        self.sifre_input.returnPressed.connect(self.giris_yapmayi_dene)

    def update_background(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        logo_path = os.path.join(script_dir, 'logo.png')
        palette = self.palette()
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            brush = QBrush(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            palette.setBrush(QPalette.ColorRole.Window, brush)
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    def showEvent(self, event):
        self.update_background()
        super().showEvent(event)

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def uye_ol_penceresi_ac(self):
        dialog = RegisterDialog(self)
        dialog.setStyleSheet(LIGHT_THEME_QSS)
        dialog.exec()

    def misafir_olarak_gir(self):
        self.misafir_girisi.emit()

    def giris_yapmayi_dene(self):
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        if not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Hata", "Alanlar boş bırakılamaz.")
            return
        try:
            baglanti = sqlite3.connect('tarih_makaleleri.db')
            cursor = baglanti.cursor()
            cursor.execute("SELECT sifre_hash, rol FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
            sonuc = cursor.fetchone()
            baglanti.close()
            if sonuc and sonuc[0] == sifre_hashle(sifre):
                self.login_basarili.emit(sonuc[1])
            elif sonuc:
                QMessageBox.warning(self, "Hata", "Hatalı şifre.")
            else:
                QMessageBox.warning(self, "Hata", "Böyle bir kullanıcı bulunamadı.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Bir hata oluştu: {e}")

#==============================================================================
# YÖNETİCİ PANELİ
#==============================================================================
class YoneticiPaneli(QWidget):
    girise_don_istegi = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setObjectName("YoneticiPaneli")
        self.db_baglantisi = None
        self.init_db()
        self.init_ui()
        self.dergileri_listele()
    def init_db(self):
        try:
            self.db_baglantisi = sqlite3.connect('tarih_makaleleri.db')
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"DB Hatası: {e}")
    def init_ui(self):
        self.setWindowTitle('Yönetici Paneli')
        main_layout = QVBoxLayout(self)
        top_bar_layout = QHBoxLayout()
        btn_girise_don = QPushButton(qta.icon('fa5s.sign-out-alt'), " Giriş Ekranına Dön")
        btn_girise_don.clicked.connect(self.girise_don_sinyali_gonder)
        top_bar_layout.addWidget(btn_girise_don)
        top_bar_layout.addStretch()
        main_layout.addLayout(top_bar_layout)
        secim_alani = QWidget()
        secim_layout = QHBoxLayout(secim_alani)
        dergi_group_layout = QHBoxLayout()
        self.dergi_combo = QComboBox()
        self.dergi_combo.currentIndexChanged.connect(self.dergi_secildi)
        btn_yeni_dergi = QPushButton("Yeni Dergi")
        btn_yeni_dergi.clicked.connect(self.yeni_dergi_ekle)
        btn_dergi_adlandir = QPushButton("Yeniden Adlandır")
        btn_dergi_adlandir.clicked.connect(self.dergi_yeniden_adlandir)
        btn_dergi_sil = QPushButton(qta.icon('fa5s.trash-alt'), "")
        btn_dergi_sil.setToolTip("Seçili Dergiyi Sil")
        btn_dergi_sil.clicked.connect(self.dergi_sil)
        btn_kapak_sec = QPushButton(qta.icon('fa5s.image'), " Kapak Seç")
        btn_kapak_sec.clicked.connect(self.kapak_resmi_sec)
        self.kapak_resmi_label = QLabel("Kapak\nResmi")
        self.kapak_resmi_label.setFixedSize(100, 100)
        self.kapak_resmi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kapak_resmi_label.setStyleSheet("border: 1px solid #cccccc; color: #aaaaaa;")
        dergi_combo_layout = QVBoxLayout()
        dergi_combo_layout.addWidget(QLabel("Dergi/Sayı:"))
        dergi_combo_layout.addWidget(self.dergi_combo)
        dergi_buton_grid = QGridLayout()
        dergi_buton_grid.addWidget(btn_yeni_dergi, 0, 0)
        dergi_buton_grid.addWidget(btn_dergi_adlandir, 0, 1)
        dergi_buton_grid.addWidget(btn_dergi_sil, 1, 0, 1, 2)
        dergi_combo_layout.addLayout(dergi_buton_grid)
        dergi_group_layout.addLayout(dergi_combo_layout)
        dergi_group_layout.addSpacing(10)
        kapak_layout = QVBoxLayout()
        kapak_layout.addWidget(self.kapak_resmi_label)
        kapak_layout.addWidget(btn_kapak_sec)
        dergi_group_layout.addLayout(kapak_layout)
        secim_layout.addLayout(dergi_group_layout)
        secim_layout.addSpacing(20)
        makale_group_layout = QVBoxLayout()
        makale_group_layout.addWidget(QLabel("Makale:"))
        makale_combo_line = QHBoxLayout()
        self.makale_combo = QComboBox()
        self.makale_combo.currentIndexChanged.connect(self.makale_secildi)
        btn_makale_sil = QPushButton(qta.icon('fa5s.trash-alt'), "")
        btn_makale_sil.setToolTip("Seçili Makaleyi Sil")
        btn_makale_sil.clicked.connect(self.makale_sil)
        makale_combo_line.addWidget(self.makale_combo, 1)
        makale_combo_line.addWidget(btn_makale_sil)
        makale_group_layout.addLayout(makale_combo_line)
        makale_group_layout.addStretch()
        secim_layout.addLayout(makale_group_layout, 2)
        main_layout.addWidget(secim_alani)
        editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.addWidget(QLabel('Başlık:'))
        self.baslik_input = QLineEdit()
        editor_layout.addWidget(self.baslik_input)
        editor_layout.addWidget(QLabel('Yazar:'))
        self.yazar_input = QLineEdit()
        editor_layout.addWidget(self.yazar_input)
        editor_layout.addWidget(QLabel('Makale Metni (HTML):'))
        self.setup_editor_toolbar()
        editor_layout.addWidget(self.editor_toolbar)
        self.metin_input = QTextEdit()
        self.metin_input.textChanged.connect(self.onizlemeyi_guncelle)
        editor_layout.addWidget(self.metin_input)
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.addWidget(QLabel("Canlı Önizleme:"))
        self.onizleme_alani = QTextBrowser()
        preview_layout.addWidget(self.onizleme_alani)
        editor_splitter.addWidget(editor_widget)
        editor_splitter.addWidget(preview_widget)
        editor_splitter.setSizes([600, 400])
        main_layout.addWidget(editor_splitter, 1)
        alt_buton_layout = QHBoxLayout()
        self.temizle_button = QPushButton('Formu Temizle')
        self.temizle_button.clicked.connect(self.formu_temizle)
        self.kaydet_button = QPushButton('Yeni Makale Olarak Kaydet')
        self.kaydet_button.clicked.connect(self.makale_kaydet)
        self.guncelle_button = QPushButton('Değişiklikleri Güncelle')
        self.guncelle_button.clicked.connect(self.makale_guncelle)
        alt_buton_layout.addStretch()
        alt_buton_layout.addWidget(self.temizle_button)
        alt_buton_layout.addWidget(self.kaydet_button)
        alt_buton_layout.addWidget(self.guncelle_button)
        main_layout.addLayout(alt_buton_layout)
    def girise_don_sinyali_gonder(self):
        self.girise_don_istegi.emit()
    def dergi_yeniden_adlandir(self):
        secili_id = self.dergi_combo.currentData()
        mevcut_ad = self.dergi_combo.currentText()
        if secili_id is None or secili_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen yeniden adlandırmak için bir dergi seçin.")
            return
        yeni_ad, ok = QInputDialog.getText(self, "Yeniden Adlandır", "Yeni dergi/sayı adı:", text=mevcut_ad)
        if ok and yeni_ad and yeni_ad.strip() and yeni_ad != mevcut_ad:
            try:
                cursor = self.db_baglantisi.cursor()
                cursor.execute("UPDATE dergiler SET ad = ? WHERE id = ?", (yeni_ad, secili_id))
                self.db_baglantisi.commit()
                self.dergileri_listele(secili_id)
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu isimde bir dergi zaten mevcut.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Güncellenirken hata oluştu: {e}")
    def dergi_secildi(self, index):
        secili_id = self.dergi_combo.currentData()
        self.makaleleri_listele(secili_id)
        self.formu_temizle()
        if secili_id is None or secili_id == -1:
            self.kapak_resmi_label.setText("Kapak\nResmi")
            return
        cursor = self.db_baglantisi.cursor()
        cursor.execute("SELECT kapak_yolu FROM dergiler WHERE id = ?", (secili_id,))
        sonuc = cursor.fetchone()
        if sonuc and sonuc[0] and os.path.exists(sonuc[0]):
            pixmap = QPixmap(sonuc[0])
            self.kapak_resmi_label.setPixmap(pixmap.scaled(self.kapak_resmi_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.kapak_resmi_label.setText("Kapak resmi yok.")
    def kapak_resmi_sec(self):
        secili_id = self.dergi_combo.currentData()
        if secili_id is None or secili_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir dergi seçin.")
            return
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Kapak Resmi Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        if dosya_yolu:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("UPDATE dergiler SET kapak_yolu = ? WHERE id = ?", (dosya_yolu, secili_id))
            self.db_baglantisi.commit()
            self.dergi_secildi(self.dergi_combo.currentIndex())
    def makale_secildi(self, index):
        makale_id = self.makale_combo.currentData()
        if makale_id is None or makale_id == -1:
            self.formu_temizle()
            return
        cursor = self.db_baglantisi.cursor()
        cursor.execute("SELECT baslik, yazar, metin FROM makaleler WHERE id = ?", (makale_id,))
        makale = cursor.fetchone()
        if makale:
            self.baslik_input.setText(makale[0])
            self.yazar_input.setText(makale[1])
            self.metin_input.setHtml(makale[2])
    def onizlemeyi_guncelle(self):
        base_font_size = 16
        style_html = f"<style>body{{font-family:'Segoe UI';color:#202020;}}p{{line-height:1.6;font-size:{base_font_size}px;}}h1{{font-size:{base_font_size+16}px;}}h2{{font-size:{base_font_size+8}px;}}</style>"
        self.onizleme_alani.setHtml(style_html + self.metin_input.toHtml())
    def wrap_text(self, tag, is_line_tag=False):
        cursor = self.metin_input.textCursor()
        selected_text = cursor.selectedText()
        if not selected_text and is_line_tag:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            selected_text = cursor.selectedText().strip()
        new_html = f"<{tag}>{selected_text}</{tag}>"
        if is_line_tag:
            new_html += "<p></p>"
        cursor.insertHtml(new_html)
    def dergileri_listele(self, secilecek_id=None):
        mevcut_id = secilecek_id if secilecek_id is not None else self.dergi_combo.currentData()
        self.dergi_combo.blockSignals(True)
        self.dergi_combo.clear()
        self.dergi_combo.addItem("Lütfen bir dergi seçin...", -1)
        cursor = self.db_baglantisi.cursor()
        cursor.execute("SELECT id, ad FROM dergiler ORDER BY ad ASC")
        for dergi_id, ad in cursor.fetchall():
            self.dergi_combo.addItem(ad, dergi_id)
        idx = self.dergi_combo.findData(mevcut_id)
        self.dergi_combo.setCurrentIndex(idx if idx != -1 else 0)
        self.dergi_combo.blockSignals(False)
        if self.dergi_combo.currentIndex() > 0:
            self.dergi_secildi(self.dergi_combo.currentIndex())
        else:
            self.makaleleri_listele(None)
    def yeni_dergi_ekle(self):
        dergi_adi, ok = QInputDialog.getText(self, "Yeni Dergi / Sayı", "Lütfen yeni dergi/sayı adını girin:")
        if ok and dergi_adi:
            try:
                cursor = self.db_baglantisi.cursor()
                cursor.execute("INSERT INTO dergiler (ad) VALUES (?)", (dergi_adi,))
                self.db_baglantisi.commit()
                self.dergileri_listele()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu isimde bir dergi zaten mevcut.")
    def dergi_sil(self):
        secili_id = self.dergi_combo.currentData()
        if secili_id is None or secili_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir dergi seçin.")
            return
        onay = QMessageBox.question(self, "Silme Onayı", f"'{self.dergi_combo.currentText()}' adlı dergiyi ve İÇİNDEKİ TÜM MAKALELERİ silmek istediğinizden emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if onay == QMessageBox.StandardButton.Yes:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("DELETE FROM makaleler WHERE dergi_id = ?", (secili_id,))
            cursor.execute("DELETE FROM dergiler WHERE id = ?", (secili_id,))
            self.db_baglantisi.commit()
            self.dergileri_listele()
            self.makale_combo.clear()
            self.formu_temizle()
    def makaleleri_listele(self, dergi_id):
        self.makale_combo.blockSignals(True)
        self.makale_combo.clear()
        if dergi_id is None or dergi_id == -1:
            self.makale_combo.blockSignals(False)
            return
        self.makale_combo.addItem("Yeni makale oluştur veya seç...", -1)
        cursor = self.db_baglantisi.cursor()
        cursor.execute("SELECT id, baslik FROM makaleler WHERE dergi_id = ? ORDER BY id DESC", (dergi_id,))
        for makale_id, makale_baslik in cursor.fetchall():
            self.makale_combo.addItem(makale_baslik, makale_id)
        self.makale_combo.blockSignals(False)
    def makale_kaydet(self):
        dergi_id = self.dergi_combo.currentData()
        if dergi_id is None or dergi_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir dergi seçin.")
            return
        baslik = self.baslik_input.text()
        yazar = self.yazar_input.text()
        metin = self.metin_input.toHtml()
        if not baslik:
            QMessageBox.warning(self, "Eksik Bilgi", "Başlık boş bırakılamaz.")
            return
        cursor = self.db_baglantisi.cursor()
        cursor.execute("INSERT INTO makaleler (baslik, yazar, metin, dergi_id) VALUES (?, ?, ?, ?)", (baslik, yazar, metin, dergi_id))
        self.db_baglantisi.commit()
        self.makaleleri_listele(dergi_id)
    def makale_guncelle(self):
        makale_id = self.makale_combo.currentData()
        if makale_id is None or makale_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen güncellemek için bir makale seçin.")
            return
        baslik = self.baslik_input.text()
        yazar = self.yazar_input.text()
        metin = self.metin_input.toHtml()
        cursor = self.db_baglantisi.cursor()
        cursor.execute("UPDATE makaleler SET baslik = ?, yazar = ?, metin = ? WHERE id = ?", (baslik, yazar, metin, makale_id))
        self.db_baglantisi.commit()
        self.makaleleri_listele(self.dergi_combo.currentData())
    def makale_sil(self):
        makale_id = self.makale_combo.currentData()
        if makale_id is None or makale_id == -1:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir makale seçin.")
            return
        onay = QMessageBox.question(self, "Silme Onayı", "Bu makaleyi kalıcı olarak silmek istediğinizden emin misiniz?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if onay == QMessageBox.StandardButton.Yes:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("DELETE FROM makaleler WHERE id = ?", (makale_id,))
            self.db_baglantisi.commit()
            self.makaleleri_listele(self.dergi_combo.currentData())
            self.formu_temizle()
    def formu_temizle(self):
        if self.makale_combo.count() > 0:
            self.makale_combo.setCurrentIndex(0)
        self.baslik_input.clear()
        self.yazar_input.clear()
        self.metin_input.clear()
        self.onizleme_alani.clear()
    def setup_editor_toolbar(self):
        self.editor_toolbar = QToolBar()
        btn_bold = QPushButton(qta.icon('fa5s.bold'), " Kalın")
        btn_bold.clicked.connect(lambda: self.wrap_text("b"))
        btn_italic = QPushButton(qta.icon('fa5s.italic'), " İtalik")
        btn_italic.clicked.connect(lambda: self.wrap_text("i"))
        btn_h1 = QPushButton("H1")
        btn_h1.clicked.connect(lambda: self.wrap_text("h1"))
        btn_p = QPushButton("Paragraf")
        btn_p.clicked.connect(lambda: self.wrap_text("p", True))
        btn_img = QPushButton(qta.icon('fa5s.image'), " Resim Ekle")
        btn_img.clicked.connect(self.resim_ekle_yerel)
        btn_table = QPushButton(qta.icon('fa5s.table'), " Tablo Ekle")
        btn_table.clicked.connect(self.tablo_ekle)
        self.editor_toolbar.addWidget(btn_bold)
        self.editor_toolbar.addWidget(btn_italic)
        self.editor_toolbar.addWidget(btn_h1)
        self.editor_toolbar.addWidget(btn_p)
        self.editor_toolbar.addWidget(btn_img)
        self.editor_toolbar.addWidget(btn_table)
    def resim_ekle_yerel(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.gif)")
        if dosya_yolu:
            html = f'<img src="file:///{dosya_yolu}" width="400"><p></p>'
            self.metin_input.textCursor().insertHtml(html)
    def tablo_ekle(self):
        html = """<p>&nbsp;</p><table border="1" width="100%" cellpadding="5" cellspacing="0"><tr><th>Başlık 1</th><th>Başlık 2</th></tr><tr><td>Veri 1</td><td>Veri 2</td></tr></table><p>&nbsp;</p>"""
        self.metin_input.textCursor().insertHtml(html)

#==============================================================================
# OKUYUCU ARAYÜZÜ
#==============================================================================
class OkuyucuArayuzu(QWidget):
    girise_don_istegi = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.db_baglantisi = None
        self.init_db()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setup_toolbar()
        main_layout.addWidget(self.toolbar)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        self.setup_left_panel()
        content_layout.addWidget(self.left_panel)
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget, 1)
        main_layout.addLayout(content_layout)
        self.setup_kart_gorunumu()
        self.setup_okuma_gorunumu()
        self.dergileri_kart_olarak_yukle()
        self.setup_arama_tamamlayici()
        self.left_panel.hide()
    def init_db(self):
        try:
            self.db_baglantisi = sqlite3.connect('tarih_makaleleri.db')
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı açılamadı: {e}")
    def setup_toolbar(self):
        self.toolbar = QToolBar("Ana Araç Çubuğu")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tüm arşivde ara...")
        self.search_input.textChanged.connect(self.arama_yap)
        self.toolbar.addWidget(self.search_input)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)
        btn_girise_don = QPushButton(qta.icon('fa5s.user-circle'), " Giriş Yap / Üye Ol")
        btn_girise_don.clicked.connect(self.girise_don_sinyali_gonder)
        self.toolbar.addWidget(btn_girise_don)
    def girise_don_sinyali_gonder(self):
        self.girise_don_istegi.emit()
    def setup_arama_tamamlayici(self):
        try:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("SELECT ad FROM dergiler")
            dergi_adlari = [item[0] for item in cursor.fetchall()]
            cursor.execute("SELECT baslik FROM makaleler")
            makale_basliklari = [item[0] for item in cursor.fetchall()]
            oneriler = list(set(dergi_adlari + makale_basliklari))
            self.completer_model = QStringListModel(oneriler)
            self.completer = QCompleter(self.completer_model, self)
            self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.search_input.setCompleter(self.completer)
        except sqlite3.Error as e:
            print(f"Arama önerileri yüklenirken hata: {e}")
    def setup_kart_gorunumu(self):
        self.kart_stack = QStackedWidget()
        kart_container_wrapper = QWidget()
        self.kart_layout = QGridLayout(kart_container_wrapper)
        self.kart_layout.setContentsMargins(25, 25, 25, 25)
        self.kart_layout.setSpacing(30)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(kart_container_wrapper)
        self.kart_stack.addWidget(scroll_area)
        karsilama_mesaji = QLabel("<h2>Henüz hiç dergi eklenmemiş.</h2>")
        karsilama_mesaji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kart_stack.addWidget(karsilama_mesaji)
        self.stacked_widget.addWidget(self.kart_stack)
    def setup_okuma_gorunumu(self):
        self.okuma_widget = QWidget()
        self.okuma_layout = QHBoxLayout(self.okuma_widget)
        self.okuma_layout.setContentsMargins(0,0,0,0)
        self.okuma_layout.setSpacing(0)
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.setup_right_panel()
        self.okuma_layout.addWidget(self.text_browser, 8)
        self.okuma_layout.addWidget(self.right_panel, 2)
        self.stacked_widget.addWidget(self.okuma_widget)
        self.update_content()
    def dergileri_kart_olarak_yukle(self, dergi_listesi=None):
        while self.kart_layout.count():
            item = self.kart_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        if dergi_listesi is None:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("SELECT id, ad, kapak_yolu FROM dergiler ORDER BY ad ASC")
            dergiler = cursor.fetchall()
        else:
            dergiler = dergi_listesi
        self.kart_stack.setCurrentIndex(1 if not dergiler else 0)
        row, col = 0, 0
        for dergi_id, ad, kapak_yolu in dergiler:
            kart = DergiKarti(dergi_id, ad, kapak_yolu, self.kart_stack.widget(0))
            kart.mouseReleaseEvent = lambda event, d_id=dergi_id: self.dergi_karti_tiklandi(d_id)
            self.kart_layout.addWidget(kart, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
    def arama_yap(self, metin):
        arama_terimi = metin.strip()
        if not arama_terimi:
            self.dergileri_kart_olarak_yukle()
            return
        arama_pattern = f"%{arama_terimi}%"
        cursor = self.db_baglantisi.cursor()
        cursor.execute("""
            SELECT DISTINCT d.id, d.ad, d.kapak_yolu FROM dergiler d
            LEFT JOIN makaleler m ON d.id = m.dergi_id
            WHERE d.ad LIKE ? OR m.baslik LIKE ?
        """, (arama_pattern, arama_pattern))
        sonuclar = cursor.fetchall()
        self.dergileri_kart_olarak_yukle(sonuclar)
    def dergi_karti_tiklandi(self, dergi_id):
        self.makaleleri_listele(dergi_id)
        self.stacked_widget.setCurrentWidget(self.okuma_widget)
        self.left_panel.show()
    def ana_sayfaya_don(self):
        self.search_input.clear()
        self.dergileri_kart_olarak_yukle()
        self.stacked_widget.setCurrentWidget(self.kart_stack)
        self.left_panel.hide()
    def setup_left_panel(self):
        self.left_panel = QWidget()
        self.left_panel.setObjectName("LeftPanel")
        layout = QVBoxLayout(self.left_panel)
        layout.setContentsMargins(10, 15, 10, 15)
        btn_ana_sayfa = QPushButton(qta.icon('fa5s.arrow-left'), " Ana Sayfaya Dön")
        btn_ana_sayfa.clicked.connect(self.ana_sayfaya_don)
        layout.addWidget(btn_ana_sayfa)
        layout.addSpacing(15)
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderHidden(True)
        self.nav_tree.setIndentation(15)
        self.nav_tree.itemClicked.connect(self.agac_ogesi_tiklandi)
        layout.addWidget(self.nav_tree)
    def setup_right_panel(self):
        self.right_panel = QWidget()
        self.right_panel.setObjectName("RightPanel")
        layout = QVBoxLayout(self.right_panel)
        layout.setContentsMargins(15, 25, 15, 15)
        self.infobox_layout = QFormLayout()
        layout.addLayout(self.infobox_layout)
        layout.addStretch()
    def makaleleri_listele(self, dergi_id):
        self.nav_tree.clear()
        try:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("SELECT id, baslik FROM makaleler WHERE dergi_id = ? ORDER BY id ASC", (dergi_id,))
            makaleler = cursor.fetchall()
            for makale_id, baslik in makaleler:
                makale_item = QTreeWidgetItem(self.nav_tree, [baslik])
                makale_item.setIcon(0, qta.icon('fa5s.file-alt'))
                makale_item.setData(0, Qt.ItemDataRole.UserRole, makale_id)
        except sqlite3.Error as e:
            print(f"Hata: {e}")
    def agac_ogesi_tiklandi(self, item, column):
        makale_id = item.data(0, Qt.ItemDataRole.UserRole)
        if makale_id is not None:
            self.makale_detay_goster(makale_id)
    def makale_detay_goster(self, makale_id):
        try:
            cursor = self.db_baglantisi.cursor()
            cursor.execute("SELECT baslik, yazar, metin FROM makaleler WHERE id = ?", (makale_id,))
            makale = cursor.fetchone()
            if makale:
                self.update_content(makale[0], makale[1], makale[2])
        except sqlite3.Error as e:
            print(f"Hata: {e}")
    def update_content(self, baslik="Hoş Geldiniz", yazar="", metin="<p>Lütfen bir makale seçin.</p>"):
        font_size = 17
        html = f"""
            <style>
                body{{font-family:'Georgia', serif;}}
                p{{line-height:1.7;font-size:{font_size}px;}}
                h1{{font-size:{font_size+16}px; font-family: 'Segoe UI', sans-serif;}}
            </style>
            <h1>{baslik}</h1>
            {metin if metin else ""}
        """
        self.text_browser.setHtml(html)
        
        # DÜZELTİLMİŞ KISIM
        for i in reversed(range(self.infobox_layout.count())):
            item = self.infobox_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        
        self.infobox_layout.addRow("<b>Yazar:</b>", QLabel(yazar if yazar else "Belirtilmemiş"))
        self.infobox_layout.addRow("<b>Kelime Sayısı:</b>", QLabel(str(len(metin.split()))))

#==============================================================================
# ANA PENCERE VE UYGULAMA BAŞLANGICI
#==============================================================================
class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarih Arşivi Uygulaması")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)
        
        self.giris_ekrani = GirisPaneli()
        self.stack.addWidget(self.giris_ekrani)
        self.okuyucu_arayuzu = OkuyucuArayuzu()
        self.stack.addWidget(self.okuyucu_arayuzu)
        self.yonetici_paneli = YoneticiPaneli()
        self.stack.addWidget(self.yonetici_paneli)
        
        self.giris_ekrani.login_basarili.connect(self.login_sonrasi)
        self.giris_ekrani.misafir_girisi.connect(self.misafir_penceresini_ac)
        self.okuyucu_arayuzu.girise_don_istegi.connect(self.show_login_screen)
        self.yonetici_paneli.girise_don_istegi.connect(self.show_login_screen)
        
        self.show_login_screen()

    def show_login_screen(self):
        self.title_bar.hide()
        self.stack.setCurrentWidget(self.giris_ekrani)

    def login_sonrasi(self, rol):
        self.setStyleSheet(LIGHT_THEME_QSS)
        self.title_bar.show()
        if rol == 'admin':
            self.title_bar.title_label.setText("Yönetici Paneli")
            self.stack.setCurrentWidget(self.yonetici_paneli)
        else:
            self.misafir_penceresini_ac()
    
    def misafir_penceresini_ac(self):
        self.setStyleSheet(LIGHT_THEME_QSS)
        self.title_bar.show()
        self.title_bar.title_label.setText("Tarih Arşivi")
        self.okuyucu_arayuzu.dergileri_kart_olarak_yukle()
        self.stack.setCurrentWidget(self.okuyucu_arayuzu)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnaPencere()
    window.showMaximized()
    sys.exit(app.exec())
