import sys
from PyQt5 import QtWidgets, uic

class Settings(object):

    def __init__(self):
        self.is_csv = False
        self.is_xls = False
        self.loan = 15344.18
        self.loan_duration = 72
        self.loan_start_date = "05/13/2019"
        self.scheduled_monthly_payment = 277.72
        self.actual_monthly_payment = 416.58
        self.principal = 0.0
        self.deposit_freq = 2
        self.deposit_amt = 530.00
        self.scheduled_months_left = 0
        self.actual_months_left = 0
        self.actual_monthly_deposit = 0.0
        self.remaining_balance = self.loan
        self.amount_paid = 0.0
        self.interest_rate = 3.24 / 100.0
        self.monthly_interest_percent = (self.interest_rate / 12)
        self.monthly_interest_amt = 0.0
        self.account_balance_needed = 0.0
        self.curr_account_balance = 2041.75
        self.total_account_balance = self.curr_account_balance
        self.potential_month_payoff = 0
        self.total_interest_paid = 0.0
        self.account_balance_eq_owed = False
        self.sig_figs = 2
        self.file_name = "auto_loan.csv"
        self.sheet_columns = {
            "Payment Date": self.loan_start_date,
            "Monthly Payment": self.scheduled_monthly_payment,
            "Principal": self.principal,
            "Interest": self.monthly_interest_amt,
            "Total Interest Paid": self.total_interest_paid,
            "Remaining Balance": self.remaining_balance
        }


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("ui/loan_gui.ui")
window.show()
