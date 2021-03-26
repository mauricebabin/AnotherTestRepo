# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *


def StrAndPad(DollarValue):
    DollarValueStr = "${:,.2f}".format(DollarValue)
    DollarValuePad = "{:>10}".format(DollarValueStr)

    return DollarValuePad

# creates a Tk() object
master = Tk()

# sets the geometry of main
# root window
master.geometry("1000x600")


# function to open a new window
# on a button click
def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)
    newWindow.title("Print Claims Report")

    results_listbox = Listbox(newWindow, height=20, width=80, font=("Courier New", 12))
    results_listbox.grid(row=0, column=0, padx=10, pady=10)

    exit_button = Button(newWindow, text="Close", width=20, command=newWindow.destroy)
    exit_button.grid(row=1, column=0, padx=20, sticky=E)

    results_listbox.insert(END, "ABC Company")
    results_listbox.insert(END, "Claims Processing Report")
    results_listbox.insert(END, "")
    results_listbox.insert(END, "Claim #   Client Name     Item Cost   HST  Total Cost")
    results_listbox.insert(END, "*" * 53)

    ClaimCtr = 0
    ItemCostAcc = 0
    HSTAcc = 0
    TotalCostAcc = 0

    f = open("Claims.dat", "r")

    for lines in f:
        splitline = lines.split(",")

        EmpNum = splitline[0]
        EmpName = splitline[2]
        ItemCost = float(splitline[3])
        HST = float(splitline[4])
        TotalCost = float(splitline[5].strip())

        results_listbox.insert(END,"  {}  {:<20}  ${:,.2f}  ${:,.2f}   ${:,.2f}".format(EmpNum, EmpName, ItemCost, HST, TotalCost))

        ClaimCtr += 1
        ItemCostAcc += ItemCost
        HSTAcc += HST
        TotalCostAcc += TotalCost

    f.close()
    results_listbox.insert(END, "*" * 53)
    results_listbox.insert(END, "  {} {:<20}  ${:,.2f} ${:,.2f} ${:,.2f}".format(ClaimCtr, "Claims listed", ItemCostAcc, HSTAcc, TotalCostAcc))

    # make dialog modal
    newWindow.transient(master)
    newWindow.grab_set()
    # instead of mainloop call wait_window
    newWindow.wait_window()

def PPWindow():

    app = Toplevel(master)
    app.title("Process Payroll")

    # CONSTANTS #

    COMMISSION_PERCENTAGE = 0.15
    BASE_SALARY_STANDARD = 16.50 * 40
    BASE_SALARY_RAISE = 18.50 * 40
    SALES_THRESHOLD = 250.00
    INCOME_TAX_PERCENTAGE = 0.21


    ## INPUT FRAME ##

    input_frame = LabelFrame(app, text="Please Enter")
    input_frame.grid(row=0, column=0, sticky="ns")

    employee_number_var = StringVar()
    employee_number_label = Label(input_frame, text="Employee Number: ")
    employee_number_label.grid(row=0, column=0, sticky=W)
    employee_number_entry = Entry(input_frame, width=4, textvariable=employee_number_var)
    employee_number_entry.grid(row=0, column=1, sticky=W)

    employee_name_var = StringVar()
    employee_name_label = Label(input_frame, text="Employee Name: ")
    employee_name_label.grid(row=1, column=0, sticky=W)
    employee_name_entry = Entry(input_frame, textvariable=employee_name_var)
    employee_name_entry.grid(row=1, column=1, sticky=W)

    monday_sales_var = StringVar()
    monday_sales_label = Label(input_frame, text="Monday Sales: ")
    monday_sales_label.grid(row=2, column=0, sticky=W)
    monday_sales_entry = Entry(input_frame, textvariable=monday_sales_var, width=10, justify="right")
    monday_sales_entry.grid(row=2, column=1, sticky=E)

    tuesday_sales_var = StringVar()
    tuesday_sales_label = Label(input_frame, text="Tuesday Sales: ")
    tuesday_sales_label.grid(row=3, column=0, sticky=W)
    tuesday_sales_entry = Entry(input_frame, textvariable=tuesday_sales_var, width=10, justify="right")
    tuesday_sales_entry.grid(row=3, column=1, sticky=E)

    wednesday_sales_var = StringVar()
    wednesday_sales_label = Label(input_frame, text="Wednesday Sales: ")
    wednesday_sales_label.grid(row=4, column=0, sticky=W)
    wednesday_sales_entry = Entry(input_frame, textvariable=wednesday_sales_var, width=10, justify="right")
    wednesday_sales_entry.grid(row=4, column=1, sticky=E)

    thursday_sales_var = StringVar()
    thursday_sales_label = Label(input_frame, text="Thursday Sales: ")
    thursday_sales_label.grid(row=5, column=0, sticky=W)
    thursday_sales_entry = Entry(input_frame, textvariable=thursday_sales_var, width=10, justify="right")
    thursday_sales_entry.grid(row=5, column=1, sticky=E)

    friday_sales_var = StringVar()
    friday_sales_label = Label(input_frame, text="Friday Sales: ")
    friday_sales_label.grid(row=6, column=0, sticky=W)
    friday_sales_entry = Entry(input_frame, textvariable=friday_sales_var, width=10, justify="right")
    friday_sales_entry.grid(row=6, column=1, sticky=E)

    ## OUTPUT FRAME ##

    output_frame = LabelFrame(app, text="Payroll Results")
    output_frame.grid(row=0, column=1, sticky="ns")

    results_listbox = Listbox(output_frame, height=8, width=40, font=("Courier New", 12))
    results_listbox.grid(row=0, column=0, sticky="NSWE")

    ## CONTROLS FRAME ##

    def calculate_button_function():

        try:
            Mon = float(monday_sales_var.get())
        except:
            tkinter.messagebox.showerror(title="Input Error", message="Monday sales cannot be blank")
            monday_sales_entry.focus_set()
            return
        else:
            if Mon < 0 or Mon > 5000:
                tkinter.messagebox.showerror(title="Input Error", message="Monday sales cannot exceed 5000.00")
                monday_sales_entry.focus_set()
                return

        Tue = float(tuesday_sales_var.get())
        Wed = float(wednesday_sales_var.get())
        Thu = float(thursday_sales_var.get())
        Fri = float(friday_sales_var.get())

        total_sales = Mon + Tue + Wed + Thu + Fri
        commission = COMMISSION_PERCENTAGE * total_sales
        base_salary = BASE_SALARY_STANDARD
        if total_sales > SALES_THRESHOLD:
            base_salary = BASE_SALARY_RAISE
        gross_pay = base_salary + commission
        income_tax = gross_pay * INCOME_TAX_PERCENTAGE
        net_pay = gross_pay - income_tax

        results_listbox.insert(END, "Payroll Calculations for " + employee_name_var.get())
        results_listbox.insert(END, "")
        results_listbox.insert(END, "Total Sales:       {}".format(StrAndPad(total_sales)))
        results_listbox.insert(END, "Commission:        {}".format(StrAndPad(commission)))
        results_listbox.insert(END, "Base salary:       {}".format(StrAndPad(base_salary)))
        results_listbox.insert(END, "Gross pay::        {}".format(StrAndPad(gross_pay)))
        results_listbox.insert(END, "Income tax:        {}".format(StrAndPad(income_tax)))
        results_listbox.insert(END, "Net pay:           {}".format(StrAndPad(net_pay)))

        results_listbox.insert(END, "Payroll Calculations for " + employee_name_var.get())
        results_listbox.insert(END, "")
        results_listbox.insert(END, "Total Sales:       {}".format(StrAndPad(total_sales)))
        results_listbox.insert(END, "Commission:        {}".format(StrAndPad(commission)))
        results_listbox.insert(END, "Base salary:       {}".format(StrAndPad(base_salary)))
        results_listbox.insert(END, "Gross pay::        {}".format(StrAndPad(gross_pay)))
        results_listbox.insert(END, "Income tax:        {}".format(StrAndPad(income_tax)))
        results_listbox.insert(END, "Net pay:           {}".format(StrAndPad(net_pay)))


    def clear_button_function():
        # Inputs:
        employee_name_var.set("")
        employee_number_var.set("")

        monday_sales_var.set("")
        tuesday_sales_var.set("")
        wednesday_sales_var.set("")
        thursday_sales_var.set("")
        friday_sales_var.set("")

        # Clear Output list
        results_listbox.delete(0,'end')

        employee_number_entry.focus_set()

    def exit_button_function():
        app.destroy()


    controls_frame = Frame(app)
    controls_frame.grid(row=1, column=0, columnspan=2)

    calculate_button = Button(controls_frame, text="Calculate", width=20, command=calculate_button_function)
    calculate_button.grid(row=0, column=0, padx=20)

    clear_button = Button(controls_frame, text="Clear", width=20, command=clear_button_function)
    clear_button.grid(row=0, column=1, padx=20)

    exit_button = Button(controls_frame, text="Exit", width=20, command=exit_button_function)
    exit_button.grid(row=0, column=2, padx=20)

    employee_number_entry.focus_set()
    monday_sales_var.set("100.00")

    # make dialog modal
    app.transient(master)
    app.grab_set()
    # instead of mainloop call wait_window
    app.wait_window()


# a button widget which will open a
# new window on button click
btn = Button(master, text="Click to view Claims Report", command=openNewWindow)
btn.pack(pady=10)

btn = Button(master, text="Click to Process Payroll", command=PPWindow)
btn.pack(pady=10)

# mainloop, runs infinitely
master.mainloop()
