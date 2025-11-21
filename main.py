from features import (
    analyze_url,
    analyze_email,
    predict_url_ml,
    predict_email_ml,
    calculate_score,
    visualize_result
)

def main():
    print("========================================")
    print("        🛡️  PhishShield v1.0            ")
    print("   AI-Powered Phishing Detection Tool   ")
    print("========================================\n")

    user_input = input("Enter a URL or an Email text:\n\n> ")

    # Decide if input is URL or Email
    if "http://" in user_input or "https://" in user_input or "www" in user_input:
        print("\nDetected Input Type: URL\n")

        # 1. Extract heuristic features from URL
        features = analyze_url(user_input)

        # 2. ML prediction (RandomForest)
        ml_prob = predict_url_ml(features)

    else:
        print("\nDetected Input Type: Email Text\n")

        # 1. Extract heuristic features from email
        features = analyze_email(user_input)

        # 2. ML prediction (TF-IDF + Logistic Regression)
        ml_prob = predict_email_ml(user_input)

    # 3. Combine ML + Heuristics
    final_score, verdict = calculate_score(features, ml_prob)

    # 4. Display Results
    print("============ RESULT ============\n")
    print(f"ML Probability of Phishing : {round(ml_prob * 100, 2)}%")
    print(f"Final Risk Score           : {round(final_score, 2)}%")
    print(f"Verdict                    : {verdict}")

    # 5. Save graph
    print("\nGenerating risk visualization chart...")
    visualize_result(features, final_score, verdict)
    print("Chart saved in: screenshots/risk_chart.png")

    print("\n========================================")
    print("        Scan complete. Stay safe!        ")
    print("========================================")

if __name__ == "__main__":
    main()

