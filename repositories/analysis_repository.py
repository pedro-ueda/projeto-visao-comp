from typing import List, Optional
from sqlalchemy.orm import Session
from models.analysis import AnalysisModel
from utils.logger import get_logger

logger = get_logger("analysis_repository")

class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, analysis: AnalysisModel) -> AnalysisModel:
        try:
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            logger.info(f"Análise ID {analysis.id} salva com sucesso.")
            return analysis
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no banco de dados: {str(e)}")
            raise e

    def get_all(self) -> List[AnalysisModel]:
        return self.db.query(AnalysisModel).order_by(AnalysisModel.created_at.desc()).all()

    def delete(self, analysis_id: int) -> bool:
        try:
            analysis = self.db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()
            if analysis:
                self.db.delete(analysis)
                self.db.commit()
                logger.info(f"Análise ID {analysis_id} removida do banco.")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar análise ID {analysis_id}: {str(e)}")
            raise e