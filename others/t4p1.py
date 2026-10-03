def calculate_average(scores):
    total = 0

    for score in scores:
        if score >= 60:
            total += score

    return total / len(scores)


scores1 = [80, 55, 70, 90]
scores2 = [40, 50, 55]
scores3 = [60, 60, 60]
scores4 = [90, 95, 100]

average = calculate_average(scores1)

print("Average:", average)