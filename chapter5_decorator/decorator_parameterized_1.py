import logging


logger = logging.getLogger(__name__)
RETRIES_LIMIT = 3

class ControlledException(Exception):
    None


def with_retry(retries_limit=RETRIES_LIMIT, allowed_exceptions=None):
    """
    함수를 3단계나 중첩. 필요하다면 이런 식으로도 중첩해야함. 필요에 따라...
    일단 어떻게 쓰는지 손으로 익히고 눈으로 이해하고 몸으로 바로 갈 수 있도록 공부하자.
    """
    allowed_exceptions = allowed_exceptions or (ControlledException, )

    def retry(operation):

        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(retries_limit):
                try:
                    return operation(*args, **kwargs)
                except allowed_exceptions as e:
                    logger.info(f"retrying {operation} due to {e}")
                    last_raised = e
                raise last_raised

            return wrapped

        return retry


@with_retry
def run_operation(task):
    return task.run()


@with_retry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()


@with_retry(allowed_exceptions=(AttributeError, ))
def run_with_custom_exceptions(task):
    return task.run()


@with_retry(
    retries_limit=4,
    allowed_exceptions=(ZeroDivisionError, AttributeError)
)
def run_with_params(task):
    return task.run()
