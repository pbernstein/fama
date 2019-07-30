#!/usr/bin/python
import types


NetIncome = []
for i in """
NetIncomeLoss
ComprehensiveIncomeNetOfTax
AccumulatedOtherComprehensiveIncomeLossNetOfTax
NetCashProvidedByUsedInOperatingActivities
NetCashProvidedByUsedInFinancingActivities
NetCashProvidedByUsedInInvestingActivities
""".split("\n"):
	if len(i) > 1:
		NetIncome.append(i)


Liabilities = []
for i in """
Liabilities
LiabilitiesAndStockholdersEquity
OtherLiabilitiesNoncurrent
LiabilitiesNoncurrent
OtherLiabilities
""".split("\n"):
	if len(i) > 1:
		Liabilities.append(i)


LiabilitiesCurrent = []
for i in """
LiabilitiesCurrent
AccruedLiabilitiesCurrent
OtherLiabilitiesCurrent
OtherAccruedLiabilitiesCurrent
""".split("\n"):
	if len(i) > 1:
		LiabilitiesCurrent.append(i)

Assets = []
for i in """
Assets
OtherAssetsNoncurrent
OtherAssets
AssetsNoncurrent
""".split("\n"):
	if len(i) > 1:
		Assets.append(i)

AssetsCurrent = []
for i in """
AssetsCurrent
PrepaidExpenseAndOtherAssetsCurrent
OtherAssetsCurrent
""".split("\n"):
	if len(i) > 1:
		AssetsCurrent.append(i)


Revenues = []
for i in """
Revenues
SalesRevenueNet
SalesRevenueGoodsNet
SalesRevenueServicesNet
LicensesRevenue
OtherSalesRevenueNet
salesandotheroperatingrevenueincludingsalesbasedtaxes
""".split("\n"):
	if len(i) > 1:
		Revenues.append(i)


Cash = []
for i in """
Cash
cashandcashequivalentsatcarryingvalue
assetsfairvaluedisclosure
CashAndDueFromBanks
""".split("\n"):
	if len(i) > 1:
		Cash.append(i)


AccountsPayable = []
for i in """
AccountsPayableCurrent
AccountsPayableTradeCurrent
accountspayableothercurrent
AccountsPayableAndAccruedLiabilitiesCurrent
NotesPayableCurrent
LongTermNotesPayable
""".split("\n"):
	if len(i) > 1:
		AccountsPayable.append(i)

AccountsReceivable = []
for i in """
AccountsReceivableNetCurrent
accountsandotherreceivablesnetcurrent
ReceivablesNetCurrent
AccountsReceivableNet
OtherReceivables
NotesAndLoansReceivableNetCurrent
""".split("\n"):
	if len(i) > 1:
		AccountsReceivable.append(i)


AdditionalPaidInCapital = []
for i in """
AdditionalPaidInCapital
""".split("\n"):
	if len(i) > 1:
		AdditionalPaidInCapital.append(i)


SharesOutstanding = []
for i in """
SharesOutstanding
CommonStockSharesOutstanding
SharesIssued
CommonStockSharesIssued
CommonStockSharesAuthorized
entitycommonstocksharesoutstanding
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
PropertyPlantAndEquipmentNet
PropertyPlantAndEquipmentOtherNet
""".split("\n"):
	if len(i) > 1:
		PropertyPlantAndEquipment.append(i)


StockholdersEquity = []
for i in """
StockholdersEquity
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

