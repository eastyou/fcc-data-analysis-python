"""Financial Calculator.

Savings goal, loan payment and payoff time calculators.
Only the standard library is used.
"""


def savings_goal(
    target: float,
    principal: float,
    monthly_deposit: float,
    annual_rate: float,
    years: int,
) -> dict:
    """Return the balance after `years` months of deposits."""
    monthly_rate = annual_rate / 100 / 12
    balance = principal
    for _ in range(years * 12):
        balance = balance * (1 + monthly_rate) + monthly_deposit
    return {
        "balance": round(balance, 2),
        "target": target,
        "reached": balance >= target,
        "shortfall": round(max(0.0, target - balance), 2),
    }


def required_monthly_deposit(
    target: float,
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
    """Return the monthly deposit needed to reach `target`."""
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    growth = (1 + monthly_rate) ** months
    if monthly_rate == 0:
        return round((target - principal) / months, 2)
    deposit = (target - principal * growth) * monthly_rate / (growth - 1)
    return round(max(0.0, deposit), 2)


def loan_payment(principal: float, annual_rate: float, years: int) -> float:
    """Return the fixed monthly payment of an amortized loan."""
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        return round(principal / months, 2)
    payment = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


def loan_summary(principal: float, annual_rate: float, years: int) -> dict:
    """Return payment, total paid and total interest."""
    payment = loan_payment(principal, annual_rate, years)
    total = payment * years * 12
    return {
        "monthly_payment": payment,
        "total_paid": round(total, 2),
        "total_interest": round(total - principal, 2),
    }


def payoff_months(balance: float, annual_rate: float, payment: float) -> int:
    """Return how many months are needed to pay off a balance."""
    monthly_rate = annual_rate / 100 / 12
    if payment <= balance * monthly_rate:
        raise ValueError("Payment is too small to ever pay off this balance")
    months = 0
    while balance > 0 and months < 1200:
        balance = balance * (1 + monthly_rate) - payment
        months += 1
    return months


def menu() -> None:
    print("Financial Calculator")
    print("1. Savings goal")
    print("2. Required monthly deposit")
    print("3. Loan payment")
    print("4. Payoff time")
    choice = input("Choose 1-4: ").strip()
    if choice == "1":
        print(savings_goal(
            float(input("Target amount: ")),
            float(input("Starting principal: ")),
            float(input("Monthly deposit: ")),
            float(input("Annual interest rate (%): ")),
            int(input("Years: ")),
        ))
    elif choice == "2":
        print("Monthly deposit:", required_monthly_deposit(
            float(input("Target amount: ")),
            float(input("Starting principal: ")),
            float(input("Annual interest rate (%): ")),
            int(input("Years: ")),
        ))
    elif choice == "3":
        print(loan_summary(
            float(input("Loan amount: ")),
            float(input("Annual interest rate (%): ")),
            int(input("Years: ")),
        ))
    elif choice == "4":
        print("Months to pay off:", payoff_months(
            float(input("Balance: ")),
            float(input("Annual interest rate (%): ")),
            float(input("Monthly payment: ")),
        ))
    else:
        print("Unknown choice")


if __name__ == "__main__":
    print("Example savings plan:", savings_goal(10000, 1000, 200, 5, 3))
    print("Example loan:", loan_summary(20000, 6, 5))
    print("Example payoff months:", payoff_months(5000, 18, 250))
