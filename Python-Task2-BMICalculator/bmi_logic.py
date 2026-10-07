"""BMI calculation and classification logic."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BMIResult:
    bmi: float
    category: str
    color: str  

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Return BMI rounded to 2 decimals. Raises ValueError on invalid input."""
    if weight_kg <= 0:
        raise ValueError("Weight must be a positive number.")
    if height_m <= 0:
        raise ValueError("Height must be a positive number.")

    if height_m > 3:
        height_m = height_m / 100

    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> tuple[str, str]:
    """Return (category, hex_color)."""
    if bmi < 18.5:
        return "Underweight", "#3498db"   
    if bmi < 25:
        return "Normal", "#2ecc71"        
    if bmi < 30:
        return "Overweight", "#f39c12"    
    return "Obese", "#e74c3c"             


def evaluate(weight_kg: float, height_m: float) -> BMIResult:
    """Convenience wrapper: compute + classify in one call."""
    bmi = calculate_bmi(weight_kg, height_m)
    category, color = classify_bmi(bmi)
    return BMIResult(bmi=bmi, category=category, color=color)