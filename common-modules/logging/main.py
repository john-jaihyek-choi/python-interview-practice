import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs.log")],
)

# Most commonly and frequently used log levels
logging.info("Informational log")
logging.debug("Logs for debugging")
logging.warning("Logs to give warnings")
logging.critical("Critial logs")
logging.exception("Logs used for exception catching")
logging.error("Errors")


def process_transactions(user: str, amount: int) -> bool:
    try:
        if not user:
            logging.warning(f"Invalid user provided. Please provide user: {user}")
            return False

        if not isinstance(user, str):
            logging.warning("user must be a valid str")
            return False

        if int(amount) <= 0:
            logging.warning(f"Amount processing must be greater than 0")
            return False

        logging.debug(f"transaction of ${amount} for {user} successful")

        return True
    except ValueError:
        return False
    except Exception:
        logging.exception("Unknown error occurred!")
        return False


user = input("user: ")
amount = input("amount: ")

try:
    process_transactions(user, int(amount))
except ValueError:
    logging.exception(f"amount, {amount}, must be a number")
except Exception:
    logging.exception("Unknown error")
