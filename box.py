
import turtle

# Create a turtle screen
screen = turtle.Screen()
screen.title("Square Box Drawing")

# Create a turtle
box_turtle = turtle.Turtle()

# Function to draw a square
def draw_square():
    for _ in range(4):
                box_turtle.forward(100)  # Move the turtle forward by 100 units
                box_turtle.right(90) # Turn the turtle 90 degrees to the right

# Call the draw_square function to draw the square
draw_square()

# Close the turtle graphics window when clicked
screen.exitonclick()

