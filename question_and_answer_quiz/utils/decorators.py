def inject(_callable, **kwargs):
    def decorator(func):
        instance = _callable(**kwargs)
        setattr(func, instance.__class__.__name__.lower(), instance)
        return func

    return decorator
