import unittest
from functions import database, initials, grade, has_duplicate, ith_position, passwordGen


class Testdatabase(unittest.TestCase):
    def testValue(self):
        self.assertRaises(ValueError, database, -2)
    def testType(self):
        self.assertRaises(TypeError, database, 'id')
        self.assertRaises(TypeError, database, False)

class TestInitials(unittest.TestCase):
    def testInitials(self):
        self.assertEqual(initials('orji kalu kelvin'), 'okk')
        self.assertEqual(initials('orji kalu'), 'ok')
        self.assertEqual(initials('orji'), 'o')
    def testInitialType(self):
        self.assertRaises(TypeError, initials, False)
        self.assertRaises(TypeError, initials, 3)
        self.assertRaises(TypeError, initials, 5+1j)

class TestGrade(unittest.TestCase):
    def testGrades(self):
        self.assertEqual(grade(0),{'score_grade': 'F9','pass_mark':40})
        self.assertEqual(grade(100),{'score_grade': 'A1','pass_mark':40})
        self.assertEqual(grade(40),{'score_grade': 'E8','pass_mark':40})
        self.assertEqual(grade(69, 'waec'),{'score_grade': 'B3','pass_mark':40})
        self.assertEqual(grade(0, 'SUBEB'),{'score_grade': 'F','pass_mark':30})
        self.assertEqual(grade(100, 'SUBEB'),{'score_grade': 'A','pass_mark':30})
        self.assertEqual(grade(30, 'SUBEB'),{'score_grade': 'E','pass_mark':30})
        self.assertEqual(grade(49, 'subeb'),{'score_grade': 'D','pass_mark':30})
    def testGradeValues(self):
        self.assertRaises(ValueError,grade,69,'weac')
        self.assertRaises(ValueError, grade, -2,'SUBEB')
    def testGradeValueType(self):
        self.assertRaises(TypeError, grade, 'number', 'waec')
        self.assertRaises(TypeError, grade, 49, 25)

class TestHas_duplicate(unittest.TestCase):
    def testHasduplicate(self):
        self.assertEqual(has_duplicate([1,2,2,3,4,2,25,7,8,9]),True)
        self.assertEqual(has_duplicate([1,2,3,4,25,7,8,9]),False)
        self.assertEqual(has_duplicate(['joseph','kindness', 'chidi']),False)
        self.assertEqual(has_duplicate(['joseph','kindness', 'chidi', 'joseph']),True)

    def testValues(self):
        self.assertRaises(ValueError, has_duplicate, 'okechukwu')
        self.assertRaises(ValueError, has_duplicate, 3)

class TestIth_position(unittest.TestCase):
    def testIth_position(self):
        self.assertEqual(ith_position(1), '1st')
        self.assertEqual(ith_position(2), '2nd')
        self.assertEqual(ith_position(3), '3rd')
        self.assertEqual(ith_position(4), '4th')
        self.assertEqual(ith_position(10), '10th')
        self.assertEqual(ith_position(257), '257th')
    def testIth_position_values(self):
        self.assertRaises(ValueError, ith_position, 0)
        self.assertRaises(ValueError, ith_position, -2)
        self.assertRaises(ValueError, ith_position, -156)
    def testIth_position_values_types(self):
        self.assertRaises(TypeError, ith_position,'first')
        self.assertRaises(TypeError, ith_position,False)
        self.assertRaises(TypeError, ith_position,4+1j)

class TestPasswordGen(unittest.TestCase):
    def testPasswordGen(self):
        self.assertNotEqual(passwordGen(9), passwordGen(9))
        self.assertNotEqual(passwordGen(), passwordGen())
        self.assertNotEqual(passwordGen(7), passwordGen(7))
        self.assertNotEqual(passwordGen(21), passwordGen(21))
    def testPasswordGenType(self):
        self.assertRaises(TypeError, passwordGen, 'password')
        self.assertRaises(TypeError, passwordGen, False)
        self.assertRaises(TypeError, passwordGen, 3+9j)
    def testPasswordGenValue(self):
        self.assertRaises(ValueError, passwordGen, 0)
        self.assertRaises(ValueError, passwordGen, -2)
        