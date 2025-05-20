import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs.log")],
)


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

process_transactions(user, amount)
