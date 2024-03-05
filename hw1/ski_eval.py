import src.ski as ski


##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.


def eval(expression: ski.Expr) -> ski.Expr:
    seen = set()
    while expression not in seen:
        seen.add(expression)
        expression = rewrite(expression)
    return expression


# def rewrite(e: ski.Expr) -> ski.Expr:
#     if not isinstance(e, ski.App):
#         return e
#     e.e1 = rewrite(e.e1)
#     e.e2 = rewrite(e.e2)
#     match e.e1:
#         case ski.I():
#             # I e → e
#             return e.e2
#         case ski.App(e1=ski.K()):
#             # K e1 e2 → e1
#             return e.e1.e2
#         case ski.App(e1=ski.App(e1=ski.S())):
#             # S e1 e2 e3 → (e1 e3) (e2 e3).
#             return ski.App(
#                 e1=ski.App(e.e1.e1.e2, e.e2),
#                 e2=ski.App(e.e1.e2, e.e2),
#             )
#         case _:
#             return e


def rewrite(expression: ski.Expr) -> ski.Expr:
    match expression:
        case e1, e2:
            match rewrite(e1), rewrite(e2):
                case "I", e1:
                    # I e1 → e1
                    return e1
                case ("K", e1), e2:
                    # K e1 e2 → e1
                    return e1
                case (("S", e1), e2), e3:
                    # S e1 e2 e3 → (e1 e3) (e2 e3)
                    return (e1, e3), (e2, e3)
                case rewritten:
                    return rewritten
        case _:
            return expression


def representation(expression):
    match expression:
        case (e1, e2):
            return f"({representation(e1)} {representation(e2)})"
        case other:
            return other


inc = ("S", (("S", ("K", "S")), "K"))
_0 = ("S", "K")
_1 = (inc, _0)

for expression, expected_output in [
    [((_0, "f"), "x"), "x"],
    [((_1, "f"), "x"), "(f x)"],
    [(((inc, _1), "f"), "x"), "(f (f x))"],
]:
    reduced = eval(expression)
    print(f"Before:   {representation(expression)}")
    print(f"After:    {representation(reduced)}")
    print(f"Expected: {expected_output}\n")
    assert representation(reduced) == expected_output
