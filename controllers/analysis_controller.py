import json
from database.connection import SessionLocal
from repositories.analysis_repository import AnalysisRepository
from services.vision_service import VisionService
from models.analysis import AnalysisModel
from utils.logger import get_logger
from pathlib import Path

logger = get_logger("analysis_controller")

class AnalysisController:
    def __init__(self):
        self.vision_service = VisionService()

    def process_and_store(self, image_bytes: bytes) -> AnalysisModel:
        db = SessionLocal()
        repository = AnalysisRepository(db)
        try:
            # Executa pipeline analítico
            metrics = self.vision_service.process_image(image_bytes)
            
            # Persiste arquivo local
            saved_path = self.vision_service.save_image_file(image_bytes)
            
            # Converte para Entidade ORM
            analysis = AnalysisModel(
                image_path=saved_path,
                descricao=metrics["descricao"],
                objetos=metrics["objetos"],
                quantidade_pessoas=metrics["quantidade_pessoas"],
                rostos=metrics["rostos"],
                idade=metrics["idade"],
                emocao=metrics["emocao"],
                cores=metrics["cores"],
                luminosidade=metrics["luminosidade"],
                nitidez=metrics["nitidez"],
                json_resultado=json.dumps(metrics)
            )
            
            saved_record = repository.save(analysis)
            return saved_record
        except Exception as e:
            logger.error(f"Erro controlado no fluxo do Controller: {str(e)}")
            raise e
        finally:
            db.close()

    def fetch_all_records(self):
        db = SessionLocal()
        repository = AnalysisRepository(db)
        try:
            return repository.get_all()
        finally:
            db.close()

    def remove_record(self, record_id: int, file_path: str) -> bool:
        db = SessionLocal()
        repository = AnalysisRepository(db)
        try:
            success = repository.delete(record_id)
            if success:
                p = Path(file_path)
                if p.exists():
                    p.unlink()
            return success
        finally:
            db.close()