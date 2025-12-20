import numpy as np

# (a) read_student_data
def read_student_data(filename):
    """
    Reads student data from a file.
    Returns a list of tuples: (name, age, math, english, science)
    Skips empty or malformed lines using try-except.
    """
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 5:
                        continue
                    name, age, math, english, science = parts
                    age = int(age)
                    math = int(math)
                    english = int(english)
                    science = int(science)
                    data.append((name, age, math, english, science))
                except ValueError:
                    # malformed numbers → skip that line
                    continue
    except FileNotFoundError:
        print("File not found:", filename)
    return data


# (b) filter_students_by_score
def filter_students_by_score(data, subject, threshold):
    """
    Returns list of names with score < threshold in given subject.
    """
    subject = subject.lower()
    if subject == "math":
        idx = 2
    elif subject == "english":
        idx = 3
    elif subject == "science":
        idx = 4
    else:
        raise ValueError("Invalid subject")

    result = []
    for rec in data:
        if rec[idx] < threshold:
            result.append(rec[0])
    return result


# (c) calculate_subject_statistics
def calculate_subject_statistics(data):
    """
    Returns dict with avg, max, min for each subject.
    """
    if not data:
        return {}

    scores = np.array([[r[2], r[3], r[4]] for r in data], dtype=float)
    subjects = ["math", "english", "science"]
    stats = {}
    for i, s in enumerate(subjects):
        col = scores[:, i]
        stats[s] = {
            "avg": float(col.mean()),
            "max": int(col.max()),
            "min": int(col.min())
        }
    return stats


# (d) assign_grades + grade_all_students
def assign_grades(score):
    """
    90+  -> A
    80–89 -> B
    70–79 -> C
    60–69 -> D
    <60   -> F
    """
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


def grade_all_students(data):
    """
    Returns list of dicts: {'name': ..., 'grades': {...}}
    """
    results = []
    for name, age, m, e, s in data:
        grades = {
            "math": assign_grades(m),
            "english": assign_grades(e),
            "science": assign_grades(s)
        }
        results.append({"name": name, "grades": grades})
    return results


# (e) students_passing_all
def students_passing_all(data, passing_score=60):
    """
    Returns:
      - set of names who passed all subjects
      - dict of pass counts per subject
    """
    passed_all = set()
    pass_counts = {"math": 0, "english": 0, "science": 0}

    for name, age, m, e, s in data:
        if m >= passing_score:
            pass_counts["math"] += 1
        if e >= passing_score:
            pass_counts["english"] += 1
        if s >= passing_score:
            pass_counts["science"] += 1

        if m >= passing_score and e >= passing_score and s >= passing_score:
            passed_all.add(name)

    return passed_all, pass_counts


# (f) convert_scores_to_array
def convert_scores_to_array(data):
    """
    Returns:
      - NumPy array of scores (n, 3)
      - list of (name, total_score)
    """
    if not data:
        return np.empty((0, 3), dtype=int), []

    arr = np.array([[r[2], r[3], r[4]] for r in data], dtype=int)
    totals = [(r[0], r[2] + r[3] + r[4]) for r in data]
    return arr, totals


# main()
def main():
    filename = "students.txt"   # must match EXACT file name
    data = read_student_data(filename)

    print("Total students loaded:", len(data))

    print("Below 60 in math:", filter_students_by_score(data, "math", 60))

    stats = calculate_subject_statistics(data)
    print("Statistics:", stats)

    grades = grade_all_students(data)
    print("Grades sample:", grades[:3])

    passed, counts = students_passing_all(data)
    print("Passed all:", passed)
    print("Pass counts:", counts)

    arr, totals = convert_scores_to_array(data)
    print("Array shape:", arr.shape)
    print("Totals:", totals[:5])


if __name__ == "_main_":
    main()