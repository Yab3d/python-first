# grade_tracker.py

def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def calculate_average(scores):
    return sum(scores) / len(scores)

def run_tracker():
    students = {}

    print("=== Student Grade Tracker ===")
    print("Type 'done' when finished adding students.\n")

    while True:
        name = input("Student name (or 'done'): ")
        if name.lower() == "done":
            break

        scores = []
        for subject in ["Math", "English", "Science"]:
            score = float(input(f"  {subject} score: "))
            scores.append(score)

        students[name] = scores

    print("\n=== Results ===")
    for name, scores in students.items():
        avg = calculate_average(scores)
        grade = get_grade(avg)
        print(f"{name}: Average = {avg:.1f}, Grade = {grade}")

run_tracker()