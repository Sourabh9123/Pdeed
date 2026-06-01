from datetime import datetime, timezone
from typing import Any

from app.db.mongodb import mongodb


async def save_document_analysis(filename: str, analysis: dict[str, Any]) -> str:
    if mongodb.database is None:
        raise RuntimeError("MongoDB database is not initialized.")

    result = await mongodb.database.document_analyses.insert_one(
        {
            "filename": filename,
            "analysis": analysis,
            "created_at": datetime.now(timezone.utc),
        }
    )

    return str(result.inserted_id)
