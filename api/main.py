from flask import Flask, request, render_template
import math
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bill = None
    breakdown = []
    if request.method == "POST":
        try:
            unit = int(request.form["unit"])
            breakdown.append(f"Total consumed unit = {unit}\n")
            bill = 0

            slabs = [
                (75, 6.18),
                (125, 8.50),
                (100, 9.10),
                (100, 9.62),
                (200, 15.01),
                (float('inf'), 17.35)
            ]

            for slab_unit, rate in slabs:
                if unit <= 0:
                    break
                u = min(unit, slab_unit)
                amount = u * rate
                breakdown.append(f"{u:>3} × {rate:>5.2f}  = {amount:8.2f} Taka")
                bill += amount
                unit -= u

            breakdown.append(f"{'Meter Rent':<13}= {42:8.2f} Taka")
            bill += 42
            vat = bill * 0.05
            breakdown.append(f"{'VAT (5%)':<13}= {vat:8.2f} Taka")
            bill += vat
            bill = math.ceil(bill) if bill - int(bill) >= 0.5 else int(bill)

        except:
            bill = "Error in input"

    return render_template("index.html", bill=bill, breakdown=breakdown, year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True, port=10020)
