#!/usr/bin/python
import types


NetIncome = []
for i in """
NET INCOME (LOSS)  
Net (Loss)/Income
Net income
""".split("\n"):
	if len(i) > 1:
		NetIncome.append(i)


Liabilities = []
for i in """
Total liabilities
""".split("\n"):
	if len(i) > 1:
		Liabilities.append(i)


LiabilitiesCurrent = []
for i in """
Total current liabilities 
""".split("\n"):
	if len(i) > 1:
		LiabilitiesCurrent.append(i)

Assets = []
for i in """
Assets
Total Assets
""".split("\n"):
	if len(i) > 1:
		Assets.append(i)

AssetsCurrent = []
for i in """
Total current assets
""".split("\n"):
	if len(i) > 1:
		AssetsCurrent.append(i)


Revenues = []
for i in """
Total operating revenues
Revenues
Total revenue, net of interest expense
""".split("\n"):
	if len(i) > 1:
		Revenues.append(i)


Cash = []
for i in """
Cash and cash equivalents
Cash and equivalents at end of period
""".split("\n"):
	if len(i) > 1:
		Cash.append(i)


AccountsPayable = []
for i in """
Accounts payable and accrued liabilities
Accounts payable

""".split("\n"):
	if len(i) > 1:
		AccountsPayable.append(i)

AccountsReceivable = []
for i in """
Accounts and other receivables
Accounts receivable
Customer and other receivables
""".split("\n"):
	if len(i) > 1:
		AccountsReceivable.append(i)


AdditionalPaidInCapital = []
for i in """
Additional paid-in capital
""".split("\n"):
	if len(i) > 1:
		AdditionalPaidInCapital.append(i)


SharesOutstanding = []
for i in """
Weighted-average shares outstanding, basic
""".split("\n"):
	if len(i) > 1:
		SharesOutstanding.append(i)

ShareBasedCompensation = []
for i in """
ShareBasedCompensation
""".split("\n"):
	if len(i) > 1:
		ShareBasedCompensation.append(i)


PropertyPlantAndEquipment = []
for i in """
Property and equipment, at cost
Property and equipment, net
Premises and equipment, net
""".split("\n"):
	if len(i) > 1:
		PropertyPlantAndEquipment.append(i)


StockholdersEquity = []
for i in """
Total stockholders' equity
""".split("\n"):
	if len(i) > 1:
		StockholdersEquity.append(i)

columns = {}


# globals() is a function that returns all of the declared variables in a dict (name: value)
# Here, I am iterating through the global dict to instantiate all the lists i created above in a dict with format (name: value)
# There is a precaution to only add list variables to the column dict

for i in globals():
	try:
		assert isinstance(globals()[i], types.ListType)
		columns[i] =  globals()[i]
	except:
		pass
		

#for i in columns:
#	print i, columns[i]

