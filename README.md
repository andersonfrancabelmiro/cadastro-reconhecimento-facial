# 👤 Sistema de Cadastro com Reconhecimento Facial

Este projeto é um sistema desenvolvido em Python que permite cadastrar pessoas através de fotos e realizar reconhecimento facial utilizando uma API externa.

---

## 🚀 Funcionalidades

* 📸 Captura de imagem pela webcam
* 🧑 Cadastro de pessoas com nome
* 🔍 Reconhecimento facial por comparação de imagens
* ☁️ Integração com banco de dados (Firebase)
* 🖥️ Interface gráfica com PyQt5

---

## 🛠️ Tecnologias utilizadas

* Python
* OpenCV
* PyQt5
* Requests
* Firebase (Firestore)
* Face++ API
* python-dotenv

---
---

## 🧾 Requisitos

- Python 3.9.13

> Este projeto utiliza Python 3.9 para garantir melhor compatibilidade com a biblioteca OpenCV e evitar problemas com versões mais recentes do Python.

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```
git clone https://github.com/andersonfrancabelmiro/cadastro-reconhecimento-facial.git
```

---

### 2. Instalar as dependências

```
pip install opencv-python pyqt5 requests python-dotenv
```

---

### 3. Criar o arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env` com:

```
API_KEY= SUA_API_KEY
API_SECRET= SUA_API_SECRET
FIREBASE_API_KEY= SUA_FIREBASE_API_KEY
PROJECT_ID= SEU_PROJECT_ID
```

---

### 4. Executar o sistema

```
python reconhecimento_facial.py
```

---

## 📌 Observações

* Não compartilhe seu arquivo `.env`
* Evite cadastrar nomes duplicados
* O reconhecimento depende da qualidade da imagem capturada

---

## 📷 Como usar

1. Clique em **Cadastrar nova pessoa**
2. Tire a foto pela webcam
3. Clique em **Reconhecer pessoa**
4. O sistema irá comparar com as imagens cadastradas

---

## 👨‍💻 Autor

Anderson de França Belmiro
