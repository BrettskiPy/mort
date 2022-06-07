import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from mort_server.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Tries to create a session to check if the DB is awake or not
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()


def main() -> None:
    logger.info("Initializing Service")
    init()
    logger.info("Service Finished Initializing")


if __name__ == "__main__":
    main()
