import logging


logger = logging.getLogger(__name__)
RETRIES_LIMIT = 3

class ControlledException(Exception):
    None


class WithRetry:
    def __init__(
        self,
        retries_limit=RETRIES_LIMIT,
        allowed_exceptions=None):
        self.retries_limit = retries_limit
        self.allowed_exceptions = allowed_exceptions or (ControlledException, )

    def __call__(self, operation):

        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None

            for _ in range(self.retries_limit):
                try:
                    return operation(*args, **kwargs)
                except self.allowed_exceptions as e:
                    logger.info(f"retrying {operation} due to {e}")
                    last_raised = e
                raise last_raised

                return last_raised

            return wrapped


@WithRetry
def run_operation(task):
    return task.run()


@WithRetry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()


@WithRetry(allowed_exceptions=(AttributeError, ))
def run_with_custom_exceptions(task):
    return task.run()


@WithRetry(
    retries_limit=4,
    allowed_exceptions=(ZeroDivisionError, AttributeError)
)
def run_with_params(task):
    return task.run()
