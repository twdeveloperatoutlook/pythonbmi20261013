import math


def calculate_bmi(height_cm, weight_kg):
    height_meters = height_cm / 100
    height_squared = height_meters * height_meters
    if not math.isfinite(height_squared) or height_squared == 0:
        return None, "height"

    bmi = weight_kg / height_squared
    if not math.isfinite(bmi) or bmi == 0:
        return None, "weight"

    return bmi, None


def bmi_guidance(bmi):
    if bmi < 18.5:
        return {
            "label": "體重過輕",
            "tone": "low",
            "advice": "留意是否攝取足夠且均衡的營養，規律進食並搭配適度肌力活動；若體重持續下降，建議諮詢醫師或營養師。",
        }
    if bmi < 24:
        return {
            "label": "健康體位",
            "tone": "healthy",
            "advice": "維持均衡飲食與規律運動，並持續留意睡眠及生活習慣，幫助保持健康體位。",
        }
    if bmi < 27:
        return {
            "label": "體重過重",
            "tone": "high",
            "advice": "可從減少含糖飲料、增加蔬菜與日常活動量開始，循序建立適合自己的健康習慣。",
        }
    return {
        "label": "肥胖",
        "tone": "high",
        "advice": "建議與醫師或營養師討論適合自己的飲食及運動計畫，並留意血壓、血糖等健康指標。",
    }


GAUGE_MIN_BMI = 10
GAUGE_MAX_BMI = 40


def gauge_angle(bmi):
    """Map a BMI value onto the half-circle gauge needle angle (-90° to 90°)."""
    clamped = min(max(bmi, GAUGE_MIN_BMI), GAUGE_MAX_BMI)
    fraction = (clamped - GAUGE_MIN_BMI) / (GAUGE_MAX_BMI - GAUGE_MIN_BMI)
    return round(-90 + 180 * fraction, 1)