class RuleError(Exception):
    """RuleErrors are raised when the program tries to do something that would
       violate the rules of the game of Black Jack. Anytime a RuleError might be
       raised, the program should catch the error and take action. It would be bad
       for the user to see a RuleError."""
    pass
