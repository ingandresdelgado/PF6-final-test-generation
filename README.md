# Instructions
Now you have the opportunity to create a menu of typical dishes from our country! Your menu can work however you want.

First, let's separate our *interactive* logic into the `main()` function, as follows:

```
def main():
print("Hello, students!")

if __name__=="__main__":
main()
```

This is recycled Python code, which will only be executed when a person invokes the program. All your code should be inside a function, whether this `main()` function (where you can include elements such as input statements) or another function.

Automatic grading will be based on the functionality of the following function (which must be built into your program):

* `dish_fetch(num)`: This function must exist in your program. It must take a number as input and generate a dictionary with the information about that dish related to that number.

**Remember**: This project will be graded automatically, and computers are very literal! 
**Note:** Use the tests! There's nothing wrong with repeating them until you pass. It's not cheating!