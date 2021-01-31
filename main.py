import math
import csv
import os
from ui.loan_gui import Settings, app


class AutoLoanScheduler(object):

    def __init__(self):
        self.settings = Settings()
        self.balance_needed = self.settings.total_account_balance
        self.remaining_balance = self.settings.remaining_balance
        self.total_principal = 0.0
        self.total_account_balance = self.settings.total_account_balance

    def calc_scheduled_months_left(self):
        return round(self.settings.remaining_balance / self.settings.scheduled_monthly_payment)

    def calc_actual_months_left(self):
        return math.ceil(self.settings.loan / self.settings.actual_monthly_payment)

    def calc_monthly_deposit(self):
        self.settings.deposit_amt = round((self.settings.deposit_amt * self.settings.deposit_freq) - self.settings.actual_monthly_payment, self.settings.sig_figs)
        return self.settings.deposit_amt

    def calc_remaining_balance(self):
        self.settings.remaining_balance = round(self.settings.remaining_balance - self.settings.principal, self.settings.sig_figs)
        return self.settings.remaining_balance

    def calc_principal(self):
        self.settings.principal = round(self.settings.actual_monthly_payment - self.settings.monthly_interest_amt, self.settings.sig_figs)
        return self.settings.principal

    def calc_total_principal(self):
        self.total_principal = round(self.total_principal + self.settings.principal, self.settings.sig_figs)
        return self.total_principal

    def calc_amount_paid(self):
        self.settings.amount_paid = round(self.settings.actual_monthly_payment + self.settings.monthly_interest_amt, self.settings.sig_figs)
        return self.settings.amount_paid

    def calc_monthly_interest_paid(self):
        self.settings.monthly_interest_amt = round(self.settings.remaining_balance * self.settings.monthly_interest_percent, self.settings.sig_figs)
        return self.settings.monthly_interest_amt

    def calc_total_interest_paid(self):
        self.settings.total_interest_paid = round(self.settings.total_interest_paid + self.settings.monthly_interest_amt, self.settings.sig_figs)
        return self.settings.total_interest_paid

    def total_account_balance_needed(self, month):
        self.balance_needed = round(self.balance_needed + self.settings.actual_monthly_deposit, self.settings.sig_figs)
        self.remaining_balance = round(self.remaining_balance - self.settings.principal, self.settings.sig_figs)

        if self.balance_needed >= self.remaining_balance and self.settings.account_balance_eq_owed is False:
            print("Remaining Balance: ", self.remaining_balance)
            print("Account Balance Needed: ", self.balance_needed)
            print("Months remaining to fully pay off auto loan: ", month)
            self.settings.account_balance_eq_owed = True

    def write_csv_headers(self):
        """ Write the headers for the csv file """
        if os.path.isfile(self.settings.file_name):
            os.remove(self.settings.file_name)

        with open(self.settings.file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.settings.sheet_columns.keys())
            writer.writeheader()

    def write_csv(self):
        """ Writes the monthly amount in a CSV """
        with open(self.settings.file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)

            row_values = self.settings.sheet_columns

            writer.writerow(row_values.values())

    def scheduler(self):
        """ Outputs how many months would be needed before fully paying off the loan"""
        # need to calculate the number of months before loan is fully paid off
        self.settings.scheduled_months_left = self.calc_scheduled_months_left()
        self.settings.actual_months_left = self.calc_actual_months_left()
        self.settings.actual_monthly_deposit = self.calc_monthly_deposit()

        self.write_csv_headers()

        self.settings.sheet_columns["Monthly Payment"] = self.settings.actual_monthly_payment

        # need to calculate when the balance in the account is sufficient to pay the rest of the loan
        # need the number of months and a looping mechanism
        while self.settings.remaining_balance >= 0:
            self.settings.sheet_columns["Interest"] = self.calc_monthly_interest_paid()
            self.settings.sheet_columns["Principal"] = self.calc_principal()
            self.settings.sheet_columns["Total Interest Paid"] = self.calc_total_interest_paid()
            self.settings.sheet_columns["Remaining Balance"] = self.calc_remaining_balance()
            self.calc_total_principal()
            self.write_csv()

        for month in range(1, self.settings.actual_months_left):
            self.total_account_balance_needed(month)


if __name__ == "__main__":
    calc = AutoLoanScheduler()
    calc.scheduler()

    app.exec()