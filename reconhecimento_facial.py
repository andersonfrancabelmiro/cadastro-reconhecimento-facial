import sys
import os
import re
import cv2
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QHBoxLayout, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from dotenv import load_dotenv
load_dotenv()

# 🔑 API 
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_PESSOAS = os.path.join(BASE_DIR, "pessoas")
os.makedirs(PASTA_PESSOAS, exist_ok=True)
LIMITE_CONFIANCA = 90

# ===============================
# Funções
# =============================== 


def salvar_no_firebase(nome):
    """Envia o nome para o banco de dados via API REST"""
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/usuarios?documentId={nome.replace(' ', '_')}&key={FIREBASE_API_KEY}"
    payload = {
        "fields": {
            "nome": {"stringValue": nome},
            "status": {"stringValue": "cadastrado"}
        }
    }
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except:
        return False

def validar_campos(nome):
    padrao = "^[A-Za-zÁÉÍÓÚÀÂÊÔÃÕáéíóúàâêôãõ ]+$"
    return re.match(padrao, nome)

def capturar_foto(nome_arquivo):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        status_label.setText("❌ Câmera não encontrada ou não conectada!")
        QMessageBox.critical(window, "Erro", "Nenhuma câmera foi detectada no computador.")
        return False

    print(f"Tire a foto e pressione ESPAÇO ({nome_arquivo})")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite(nome_arquivo, frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    return True 

def cadastrar_pessoa():
    nome, ok = QInputDialog.getText(window, "Cadastro", "Digite o nome da pessoa:")
    
    if not ok or not nome:
        return
    
    nome = nome.strip()  
    
    if not validar_campos(nome):
        status_label.setText("❌ Nome invalido !")
        return   

    caminho = os.path.join(PASTA_PESSOAS, f"{nome}.jpg")
    
    if capturar_foto(caminho):
        if salvar_no_firebase(nome):
            status_label.setText(f"✅ '{nome}' cadastrado e salvo no banco!")
        else:
            status_label.setText(f"✅ '{nome}' salvo local, mas erro no banco.")

def reconhecer_pessoa():
    if not capturar_foto("webcam.jpg"): return
    
    melhor_nome = None
    melhor_conf = 0
    melhor_caminho = None

    for arquivo in os.listdir(PASTA_PESSOAS):
        if arquivo.endswith(".jpg"):
            caminho = os.path.join(PASTA_PESSOAS, arquivo)
            url = "https://api-us.faceplusplus.com/facepp/v3/compare"
            
            with open("webcam.jpg", "rb") as f1, open(caminho, "rb") as f2:
                files = {"image_file1": f1, "image_file2": f2}
                data = {"api_key": API_KEY, "api_secret": API_SECRET}
                resposta = requests.post(url, data=data, files=files)
                resultado = resposta.json()
                conf = resultado.get("confidence", 0)

            if conf > melhor_conf:
                melhor_conf = conf
                melhor_nome = os.path.splitext(arquivo)[0]
                melhor_caminho = caminho

    if melhor_conf >= LIMITE_CONFIANCA:
        status_label.setText(f"✅ Pessoa reconhecida: {melhor_nome} (Confiança: {melhor_conf})")
        foto = cv2.imread(melhor_caminho)
        cv2.imshow(f"Pessoa Reconhecida: {melhor_nome}", foto)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        status_label.setText(f"❌ Pessoa não reconhecida! Confiança máxima: {melhor_conf}")

# ===============================
# Front PyQt5 (Mantido original)
# ===============================
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sistema de Reconhecimento Facial")
window.setFixedSize(400, 300)
window.setStyleSheet("background-color: #f0f0f0;")

layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)

title = QLabel("👤 Sistema Facial")
title.setFont(QFont("Arial", 18, QFont.Bold))
title.setAlignment(Qt.AlignCenter)
layout.addWidget(title)

btn_style = """
QPushButton {
    background-color: #4CAF50; 
    color: white; 
    border-radius: 10px;
    padding: 12px;
    font-size: 14pt;
}
QPushButton:hover {
    background-color: #45a049;
}
"""

btn_cadastrar = QPushButton("Cadastrar nova pessoa")
btn_cadastrar.setStyleSheet(btn_style)
btn_cadastrar.clicked.connect(cadastrar_pessoa)
layout.addWidget(btn_cadastrar)

btn_reconhecer = QPushButton("Reconhecer pessoa")
btn_reconhecer.setStyleSheet(btn_style)
btn_reconhecer.clicked.connect(reconhecer_pessoa)
layout.addWidget(btn_reconhecer)

btn_sair = QPushButton("Sair")
btn_sair.setStyleSheet(btn_style)
btn_sair.clicked.connect(sys.exit)
layout.addWidget(btn_sair)

line = QFrame()
line.setFrameShape(QFrame.HLine)
line.setFrameShadow(QFrame.Sunken)
layout.addWidget(line)

status_label = QLabel("📌 Status: aguardando ação...")
status_label.setFont(QFont("Arial", 10))
status_label.setAlignment(Qt.AlignCenter)
layout.addWidget(status_label)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())