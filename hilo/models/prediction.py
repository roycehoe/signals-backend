from enum import Enum


class Prediction(str, Enum):
    HIGHER = "Higher"
    LOWER = "Lower"
