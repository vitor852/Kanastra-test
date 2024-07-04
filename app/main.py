from fastapi import FastAPI, UploadFile, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging


from .services import Data
from .models import Base
from .database import engine
from .dependecies.database import get_db
from .settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('Starting up.')

@app.get("/")
async def root():
    return {"message": "ping pong"}

@app.post("/", status_code=status.HTTP_200_OK)
def handle_file(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        logger.info('File extension indvalid, raising error.')
        error_code, msg = getattr(settings.error, settings.error_codes.INVALID_FILE)
        raise HTTPException(status_code=error_code, detail=msg)
    
    logger.info('File extension validated.')

    try:
        logger.info(f'Processing file: {file.filename}')
        Data(db).from_file(file).process()
        return
    except Exception as e:
        if len(e.args) == 2:
            error_code, reason = e.args
        else:
            error_code = e.args[0]
            reason = None

        status_code, msg = getattr(settings.error, error_code)

        logger.error(f'Error processing file: {msg}')
        logger.error(reason)
        
        raise HTTPException(
            status_code=status_code, 
            detail=dict(
                msg=msg,
                reason=reason
            )
        )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
