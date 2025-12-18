class Smoother:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.value = None

    def update(self, value):
        if self.value is None:
            self.value = value
        else:
            self.value = self.alpha * value + (1 - self.alpha) * self.value
        return self.value