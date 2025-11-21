from features import (
    analyze_url,
    analyze_email,
    predict_url_ml,
    predict_email_ml,
    calculate_score,
    visualize_result
)

def main():
    print("=== PhishShield: AI-Powered Phishing Detection ===")
    user_input = input("Enter URL or Email Text: ")

    # Decide type
    if "http" in user_input or "www" in user_input:
        print("\nDetected: URL")
        features = analyze_url(user_input)
        ml_prob = predict_url_ml(user_input)

    else:
        print("\nDetected: Email")
        features = analyze_email(user_input)
        ml_prob = predict_email_ml(user_input)

    score, verdict = calculate_score(features, ml_prob)

    print("\n=== RESULTS ===")
    print(f"ML Probability of Phishing: {round(ml_prob*100, 2)}%")
    print(f"Final Risk Score: {round(score, 2)}%")
    print(f"Verdict: {verdict}")

    visualize_result(features, score, verdict)
    print("\nGraph saved → screenshots/risk_chart.png")

if __name__ == "__main__":
    main()

