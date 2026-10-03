import pandas as pd

df = pd.read_csv(r"D:\biuh\Introduction to project work\student_performance_1 (1).csv")
print(df.head(3))
print(df[["name", "exam_score"]])
result = df[(df["study_hours"] > 5) & (df["attendence"] > 80)]
print(result)
print(df.columns)