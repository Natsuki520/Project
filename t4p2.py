def analyze_scores(scores):
    passed = 0
    failed = 0
    total = 0

    for score in scores:
        total += score

        if score >= 60:
            passed += 1
        else:
            failed += 1

    average = total / len(scores)

    return passed, failed, average


scores = [40,50,55]

passed, failed, average = analyze_scores(scores)

print("Passed:", passed)
print("Failed:", failed)
print("Average:", average)