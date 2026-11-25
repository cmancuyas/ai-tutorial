"""
LESSON 1: Python basics for a C# developer.

Run this file with:   uv run python lessons/01_python_basics.py

Read it top to bottom. Each section shows the C# you already know,
then the Python version. Change things and re-run to experiment.
"""

# ---------------------------------------------------------------
# 1. VARIABLES
# C#:     string name = "Juan"; int age = 30; var price = 9.99;
# Python: no semicolons, no "var". Type hints (": str") are optional
#         but we use them, because they help the editor catch mistakes.
# ---------------------------------------------------------------
name: str = "Juan"
age: int = 30
price: float = 9.99
is_active: bool = True          # True/False are capitalized in Python

# f-strings are like C# interpolated strings: $"Hello {name}"
print(f"1. Hello {name}, you are {age} years old.")


# ---------------------------------------------------------------
# 2. IF / ELSE  -- Python uses INDENTATION instead of { }
# C#:  if (age >= 18) { ... } else if (...) { ... } else { ... }
# ---------------------------------------------------------------
if age >= 60:
    print("2. Senior")
elif age >= 18:                  # "elif" = "else if"
    print("2. Adult")
else:
    print("2. Minor")

# && is "and", || is "or", ! is "not"
if is_active and not age < 18:
    print("2. Active adult")


# ---------------------------------------------------------------
# 3. LISTS  (like List<T>)
# C#:  var offices = new List<string> { "Manila", "Cebu" };
# ---------------------------------------------------------------
offices: list[str] = ["Manila", "Cebu", "Davao"]
offices.append("Iloilo")         # C#: offices.Add("Iloilo")
print(f"3. First office: {offices[0]}, count: {len(offices)}")  # len() = .Count

# foreach loop
for office in offices:
    print(f"   - {office}")


# ---------------------------------------------------------------
# 4. DICTIONARIES  (like Dictionary<string, int>)
# ---------------------------------------------------------------
ratings: dict[str, int] = {"Manila": 4, "Cebu": 5}
ratings["Davao"] = 3             # add or update
print(f"4. Cebu rating: {ratings['Cebu']}")

for office, rating in ratings.items():   # like foreach (var kv in dict)
    print(f"   {office}: {rating}")


# ---------------------------------------------------------------
# 5. LIST COMPREHENSIONS  (Python's version of LINQ)
# C#:  var good = ratings.Where(r => r.Value >= 4).Select(r => r.Key).ToList();
# ---------------------------------------------------------------
good_offices = [office for office, rating in ratings.items() if rating >= 4]
print(f"5. Good offices: {good_offices}")

numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]                 # .Select(n => n * n)
total = sum(numbers)                               # .Sum()
print(f"   squares={squares}, total={total}")


# ---------------------------------------------------------------
# 6. FUNCTIONS  (methods)
# C#:  public static decimal AddVat(decimal amount, decimal rate = 0.12m) { ... }
# Python: "def", type hints, "-> return type"
# ---------------------------------------------------------------
def add_vat(amount: float, rate: float = 0.12) -> float:
    return amount * (1 + rate)


print(f"6. 100 with VAT = {add_vat(100):.2f}")    # :.2f = 2 decimals, like {x:F2}
print(f"   100 with 5% = {add_vat(100, rate=0.05):.2f}")  # named argument


# ---------------------------------------------------------------
# 7. CLASSES
# @dataclass is like a C# record: it creates the constructor,
# ToString and Equals for you.
# ---------------------------------------------------------------
from dataclasses import dataclass  # imports are like "using"


@dataclass
class Office:
    name: str
    region: str
    rating: int = 0              # default value
    manager: str | None = None

    def is_good(self) -> bool:   # "self" is like "this" (you must write it)
        return self.rating >= 4


cebu = Office(name="Cebu", region="Visayas", rating=5)   # no "new" keyword
print(f"7. {cebu}  good? {cebu.is_good()}")


# ---------------------------------------------------------------
# 8. NULL  -- C# null is Python None
# C#:  string? note = null;  if (note == null) ...
# ---------------------------------------------------------------
note: str | None = None
if note is None:
    print("8. No note yet")


# ---------------------------------------------------------------
# 9. ERRORS  -- try/catch is try/except
# ---------------------------------------------------------------
try:
    result = 10 / 0
except ZeroDivisionError as error:
    print(f"9. Caught an error: {error}")


# ---------------------------------------------------------------
# YOUR TURN (exercises) - edit below, then re-run the file
# ---------------------------------------------------------------
# a) Make a list of 5 survey ratings (1 to 5) and print the average.
#    Hint: sum(list) / len(list)
my_ratings: list[int] = [5, 3, 4, 1, 2]
average = sum(my_ratings) / len(my_ratings)
print(f"a) Average rating: {average}")


# b) Use a list comprehension to keep only ratings below 3.
low_ratings = [r for r in my_ratings if r < 3]
print(f"b) Low ratings: {low_ratings}")


# c) Write a function  label(rating: int) -> str  that returns
#    "bad" for 1-2, "ok" for 3, "good" for 4-5.
def label(rating: int) -> str:
    if rating <= 2:
        return "bad"
    elif rating == 3:
        return "ok"
    else:
        return "good"


print(f"c) {label(1)} {label(3)} {label(5)}")   # call it AFTER it is defined


# d) Add a field  manager: str | None = None  to the Office class
#    and print an office that has a manager.
#    (The field was added to the Office class in section 7 above.)
davao = Office(name="Davao", region="Mindanao", rating=4, manager="Ana")
print(f"d) {davao}")
print(f"   {cebu}")   # cebu was created without a manager, so it shows manager=None


