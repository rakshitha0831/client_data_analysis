from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        inputs = {
            "region": request.form.get('region', ''),
            "industry": request.form.get('industry', ''),
            "sessions": request.form.get('sessions', ''),
            "revenue": request.form.get('revenue', ''),
            "satisfaction_score": request.form.get('satisfaction_score', ''),
            "support_tickets": request.form.get('support_tickets', '')
        }

        region = float(inputs["region"] or 0)
        industry = float(inputs["industry"] or 0)
        sessions = float(inputs["sessions"] or 0)
        revenue = float(inputs["revenue"] or 0)
        satisfaction = float(inputs["satisfaction_score"] or 0)
        support_tickets = float(inputs["support_tickets"] or 0)

        # Derived engineered features (same as training)
        avg_session_time = 15
        conversion_rate = 0.3
        customer_tenure_months = 12
        product_adoption_rate = 0.5
        engagement_score = 60
        marketing_spend = 10000
        revenue_per_session = revenue / sessions if sessions > 0 else 0
        support_intensity = support_tickets / (customer_tenure_months + 1)

        # Prepare feature vector
        features = np.array([[
            region, industry, sessions, avg_session_time, conversion_rate,
            customer_tenure_months, engagement_score, marketing_spend,
            product_adoption_rate, revenue, satisfaction,
            support_tickets, revenue_per_session, support_intensity
        ]])

        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0][1]

        # Result formatting
        if prediction == 1:
            result = f"⚠️ High Churn Risk ({proba*100:.1f}%) — Client likely to churn."
            result_class = "churn"
        else:
            result = f"✅ Retained Client ({(1-proba)*100:.1f}%) — Low churn probability."
            result_class = "retained"

        # Input summary display
        summary = f"""
        <div class='input-summary'>
            <p><strong>📊 Client Input Summary:</strong></p>
            <ul>
                <li>Region: {region}</li>
                <li>Industry: {industry}</li>
                <li>Sessions: {sessions}</li>
                <li>Revenue: £{revenue:,.0f}</li>
                <li>Satisfaction Score: {satisfaction}</li>
                <li>Support Tickets: {support_tickets}</li>
            </ul>
        </div>
        """

        return render_template(
            'index.html',
            result=summary + f"<p class='{result_class}'>{result}</p>",
            result_class=result_class,
            inputs=inputs
        )

    except Exception as e:
        return render_template('index.html', result=f"Error: {str(e)}", result_class="error")

if __name__ == '__main__':
    app.run(debug=True)
