# Calculator Expressions

This is just an exploration of parsing and evaluating calculator expressions.

For now, we have:
parentheses, integers (+/- numbers including 0) and operators (+, -, *, /)
but no exponent (^) operator, and unary operator (-(3 + 4))

Hence we have to handle operator precedence and left-to-right associativity

There are currently 2 parsing algorithms used:
+ RecursivePrecedenceReduction:
  which is just my shot at a solution (of course, a bad one) without knowledge. \
  We gather the brackets and recurse through them, starting from inner most one \
  For an expression with no brackets \
  We sort operators in the expression with the highest precedence and on tie-break which came first from left \
  We get the left and right values for that operator, build the node and replace in-place \
  Then we repeat, until a single node is available \
  This is how roughly it works. The implementation is messy.

* Pratt Parser:
  This involves binding power of operators. 
  We have left and right expressions for operators (for example 1 + 4 has 1 and 4 as left and right). \
  We have operators with binding power which is how strong they capture their neighbouring elements. This reflects precedence. 
  in 1 + 2 * 3, * should have more strength than +
  The idea is, we first get the initial value in the expression
  for example, 1 in 1 + 2 * 3 \
  then we see the next operator, here it's + \
  then we recursively parse the remaining right side, to get the right value, but under the condition that, the next operator must have binding power that's the same or higher. So in 1 * 2 + 3, the + has lower binding power, so the right is 1 * 2 and not 1 * (2 + 3). But there's also left to right associativity, so we say the right operator should have binding power + 1, so 1 - 2 - 3 evaluates to (1 - 2) - 3. \
  We use a while True loop and recursion in it for the same, to build the AST \
  We peek for operator, check its binding power, if its lower we break into previous call while returning the expression for the previous operator's right. Or else, we parse the right expression recursively again. \
  We advance or consume the token. \
  left and parsed rights are combined into a node and reassigned to left. until the first call's loop which is the AST's root.
  This gives us the correct AST.
