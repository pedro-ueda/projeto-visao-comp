import cv2
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from config.config import Config
from utils.logger import get_logger

logger = get_logger("vision_service")

class VisionService:
    def __init__(self):
        # Carrega o classificador Haar integrado do OpenCV para detecção facial robusta local
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def process_image(self, image_bytes: bytes) -> dict:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Incapaz de decodificar os bytes da imagem.")

            height, width, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 1. Análise de Luminosidade
            luminosity = float(np.mean(gray))

            # 2. Análise de Nitidez (Variância do Laplaciano)
            sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

            # 3. Detecção de Rostos
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            face_count = len(faces)

            # 4. Cores Predominantes (Cálculo de histograma simplificado BGR)
            avg_color_bgr = np.mean(img, axis=(0, 1))
            dominant_colors = f"R: {int(avg_color_bgr[2])}, G: {int(avg_color_bgr[1])}, B: {int(avg_color_bgr[0])}"

            # 5. Metadados e estruturação preditiva para futuras IAs
            now = datetime.now()
            results = {
                "created_at": now.isoformat(),
                "resolucao": f"{width}x{height}",
                "luminosidade": round(luminosity, 2),
                "nitidez": round(sharpness, 2),
                "quantidade_pessoas": face_count,
                "rostos": face_count,
                "cores": dominant_colors,
                "descricao": f"Captura de imagem em {width}x{height} com detecção ativa.",
                "objetos": "Rosto Humano" if face_count > 0 else "Nenhum detectado localmente",
                "idade": "Não estimada (Pronto para API de IA externa)" if face_count > 0 else "N/A",
                "emocao": "Não detectada (Pronto para API de IA externa)" if face_count > 0 else "N/A"
            }

            logger.info("Pipeline de visão computacional concluído com sucesso.")
            return results
        except Exception as e:
            logger.error(f"Falha no pipeline de visão computacional: {str(e)}")
            raise e

    def save_image_file(self, image_bytes: bytes) -> str:
        filename = f"capture_{int(datetime.utcnow().timestamp())}.jpg"
        file_path = Config.UPLOAD_FOLDER / filename
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Arquivo de imagem armazenado em: {file_path}")
        return str(file_path)