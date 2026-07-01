import json
import logging
from typing import Any

from aiokafka import AIOKafkaProducer

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_producer: AIOKafkaProducer | None = None


async def start_event_publisher() -> None:
    global _producer
    _producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    try:
        await _producer.start()
        logger.info("Kafka producer connected")
    except Exception:
        logger.warning("Kafka unavailable — events will be skipped", exc_info=True)
        await _producer.stop()
        _producer = None


async def stop_event_publisher() -> None:
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None


async def publish_event(event_type: str, payload: dict[str, Any]) -> None:
    if not _producer:
        logger.debug("Skipping event %s (no Kafka connection)", event_type)
        return

    topic = f"{settings.kafka_topic_prefix}.{event_type}"
    try:
        await _producer.send_and_wait(topic, {"type": event_type, **payload})
    except Exception:
        logger.warning("Failed to publish event %s", event_type, exc_info=True)
