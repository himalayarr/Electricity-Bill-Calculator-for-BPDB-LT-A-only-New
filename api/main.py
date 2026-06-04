from flask import Flask, request, render_template
import math
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bill = None
    breakdown = []
    # Default is 'new' for initial page load
    rate_type = "new" 

    if request.method == "POST":
        # Fetch the selected rate type FIRST before anything else
        # This ensures the toggle state is saved even if other calculations fail
        rate_type = request.form.get("rate_type", "new")
        
        try:
            unit = int(request.form["unit"])
            
            breakdown.append(f"Tariff Type: {'New' if rate_type == 'new' else 'Old'} Rate\n")
            breakdown.append(f"Total consumed unit = {unit}\n")
            bill = 0

            # Your old rate
            old_slabs = [
                (75, 5.26),
                (125, 7.20),
                (100, 7.59),
                (100, 8.02),
                (200, 12.67),
                (float('inf'), 14.61)
            ]
            
            # New rate found from PDF
            new_slabs = [
                (75, 6.18),
                (125, 8.50),
                (100, 9.10),
                (100, 9.62),
                (200, 15.01),
                (float('inf'), 17.35)
            ]

            # Assign slabs based on user selection
            slabs = new_slabs if rate_type == "new" else old_slabs

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

    # Crucial: pass rate_type back to the template to persist the toggle state
    return render_template("index.html", bill=bill, breakdown=breakdown, rate_type=rate_type, year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True, port=10020)
