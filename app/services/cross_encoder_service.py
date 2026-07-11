from sentence_transformers import CrossEncoder
from app.core.settings import settings
cross_encoder = CrossEncoder(
    settings.CROSS_ENCODER_MODEL
)