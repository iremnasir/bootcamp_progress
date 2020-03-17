
def count_words(s):
    return len(s.split())

# 1. Make sure the following statement works
assert count_words("hello world") == 2

# 2. Make sure the following statement fails
assert count_words("in love with the shape of you") == 3

# 3. Insert a string that does not result in 2
assert count_words(...) == ...

# 4. Check an empty string
assert count_words("") == ...

# 5. Check a string with lots of special characters
assert count_words(...) == ...

# 6. Create a very long string (10000+ chars) and check it
assert count_words(...) == ...

# 7. Call the function with a number
try:
    count_words(...)
except:
    ...
