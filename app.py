import math

from flask import Flask, render_template, request

from bmi import bmi_guidance, calculate_bmi, gauge_angle

app = Flask(__name__)


def parse_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


@app.route("/", methods=["GET", "POST"])
def index():
    name_input = ""
    height_input = ""
    weight_input = ""
    errors = {}
    result = None

    if request.method == "POST":
        name_input = request.form.get("name", "").strip()
        height_input = request.form.get("height", "").strip()
        weight_input = request.form.get("weight", "").strip()
        height = parse_positive_number(height_input)
        weight = parse_positive_number(weight_input)

        if height is None:
            errors["height"] = "請輸入大於 0 的有效身高（公分）。"
        if weight is None:
            errors["weight"] = "請輸入大於 0 的有效體重（公斤）。"

        if not errors:
            bmi, error_field = calculate_bmi(height, weight)
            if error_field:
                errors[error_field] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
            else:
                displayed_bmi = round(bmi, 1)
                result = {
                    "bmi": f"{displayed_bmi:.1f}",
                    "gauge_angle": gauge_angle(displayed_bmi),
                    **bmi_guidance(displayed_bmi),
                }

    return render_template(
        "index.html",
        name_input=name_input,
        height_input=height_input,
        weight_input=weight_input,
        errors=errors,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)
