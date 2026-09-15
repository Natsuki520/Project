from t3_from_pop_to_oop import Student

def test_pass_check():
    student1 = Student("a",75).pass_check()
    assert student1 == "Pass"

    student2 = Student("b",60).pass_check()
    assert student2 == "Pass"

    student3 = Student("d",50).pass_check()
    assert student3 == "Fail"

    student4 = Student("e",-10).pass_check()
    assert student4 == "Fail"

    try:
        Student("c", "abc") 
        assert True
    except ValueError:
        pass


