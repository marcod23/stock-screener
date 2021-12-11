#include <fstream>
#include <iostream>
#include <cmath>
using namespace std;


void cagr(double data[], int numYears) {

	double max = data[numYears - 1] / data[0];
	double maxRate = pow(max, 1.0/(numYears-1)) - 1;
	cout << numYears - 1 << "yr CAGR: " << maxRate << endl;
	
	if (numYears > 11) {
		double ten = data[numYears - 1] / data[numYears-11];
		double tenRate = pow(ten, 0.1) - 1;
		cout << "10yr CAGR: " << tenRate << endl;
	}

        double seven = data[numYears-1] / data[numYears-8];
        double five = data[numYears-1] / data[numYears-6];
        double three = data[numYears-1] / data[numYears-4];
 
        double sevenRate = pow(seven, 0.14285714) - 1;
        double fiveRate = pow(five, 0.2) - 1;
        double threeRate = pow(three, 0.33333333) - 1;

        cout << "7yr CAGR: " << sevenRate << endl;
        cout << "5yr CAGR: " << fiveRate << endl;
        cout << "3yr CAGR: " << threeRate << endl;
}


void findMOS() {
	
	double overallGrowthRate;
	cout << "Overall Growth Rate: ";
	cin >> overallGrowthRate;

	double currentEPS;
	cout << "Current EPS: ";
	cin >> currentEPS;

	double peRatio;
	cout << "P/E Ratio: ";
	cin >> peRatio;

	double tenYearEPS = currentEPS * pow((1 + overallGrowthRate), 10);
	double tenYearPrice = peRatio * tenYearEPS;
	double stickerPrice = tenYearPrice / pow(1.15, 10);
	double lowerMarginOfSafety = stickerPrice * 0.5;
	double upperMarginOfSafety = stickerPrice * 0.66;

	cout << "MOS Range: " << lowerMarginOfSafety << " - " << upperMarginOfSafety << endl;
}


void findTenCap() {
	
	double netIncome;
	cout << "Net Income: ";
	cin >> netIncome;

	double depAndAmor;
	cout << "Depreciation and Amortization: ";
	cin >> depAndAmor;

	double accRec;
	cout << "Accounts Receivable: ";
	cin >> accRec;

	double accPay;
	cout << "Accounts Payable: ";
	cin >> accPay;

	double incomeTax;
	cout << "Income Tax: ";
	cin >> incomeTax;

	double maintCapExp;
	cout << "Maintenance Capital Expenditures: ";
	cin >> maintCapExp;

	double sharesOut;
	cout << "Shares Outstanding: ";
	cin >> sharesOut;

	double ownerEarnings = netIncome + depAndAmor + accRec + accPay + incomeTax + maintCapExp;

	double tenCap = (ownerEarnings * 10) / sharesOut;

	cout << "Ten Cap Price: " << tenCap << endl;
}


void findPayback() {

	double overallGrowthRate;
	cout << "Overall Growth Rate: ";
	cin >> overallGrowthRate;

	double sharesOut;
	cout << "Shares Outstanding: ";
	cin >> sharesOut;

	double operatingCash;
	cout << "Net Cash Provided by Operating Activities: ";
	cin >> operatingCash;

	double propAndEquip;
	cout << "Purchase of Property and Equipment: ";
	cin >> propAndEquip;

	double otherCapExp;
	cout << "Other Capital Expenditures: ";
	cin >> otherCapExp;

	double freeCashFlow = operatingCash + propAndEquip + otherCapExp;
	
	double onePlusOGR = 1 + overallGrowthRate;
	double paybackTime = freeCashFlow * (onePlusOGR + pow(onePlusOGR, 2) + pow(onePlusOGR, 3) + pow(onePlusOGR, 4) 
			+ pow(onePlusOGR, 5) + pow(onePlusOGR, 6) + pow(onePlusOGR, 7) + pow(onePlusOGR, 8));

	double paybackPrice = paybackTime / sharesOut;

	cout << "Payback Time Price: " << paybackPrice << endl;
}

int main ()
{
	
	int numYears;
	cout << "How many years of data do you have?" << endl;
	cin >> numYears;

	double operatingCash[numYears];
        double equity[numYears];
        double longTermDebt[numYears];
	double revenue[numYears];
	double netIncome[numYears];
	double dividends[numYears];

	ifstream file("info.txt");

	
	for (int i = 0; i < numYears; i++) {
		file >> revenue[i];
	}
		
	for (int i = 0; i < numYears; i++) {
		file >> netIncome[i];
	}
		
	for (int i = 0; i < numYears; i++) {
		file >> operatingCash[i];
	}

	for (int i = 0; i < numYears; i++) {
		file >> longTermDebt[i];
	}
			
	for (int i = 0; i < numYears; i++) {
		file >> equity[i];
	}
			
	for (int i = 0; i < numYears; i++) {
		file >> dividends[i];
	}

	
	file.close();	

	
	double equityPlusDiv[numYears];

	for (int i = 0; i < numYears; i++) {
		equityPlusDiv[i] = equity[i] + dividends[i];
	}

	
	double revenueGrowth[numYears - 1];
	double netIncomeGrowth[numYears - 1];
	double operatingCashGrowth[numYears - 1];
	double equityGrowth[numYears - 1];


	for (int i = 0; i < numYears - 1; i++) {
		revenueGrowth[i] = (revenue[i+1] / revenue[i]) - 1;
		netIncomeGrowth[i] = (netIncome[i+1] / netIncome[i]) - 1;
		operatingCashGrowth[i] = (operatingCash[i+1] / operatingCash[i]) - 1;
		equityGrowth[i] = (equityPlusDiv[i+1] / equityPlusDiv[i]) - 1;
	}

	for (int i = 0; i < numYears - 1; i++) {
		cout << "Year " << i+1 << " Revenue Growth: " << revenueGrowth[i] << endl;
	}

	cout << endl;

	for (int i = 0; i < numYears - 1; i++) {
		cout << "Year " << i+1 << " Net Income Growth: " << netIncomeGrowth[i] << endl;
	}
	
	cout << endl;

	for (int i = 0; i < numYears - 1; i++) {
		cout << "Year " << i+1 << " Operating Cash Growth: " << operatingCashGrowth[i] << endl;
	}

	cout << endl;

	for (int i = 0; i < numYears - 1; i++) {
		cout << "Year " << i+1 << " Equity Growth: " << equityGrowth[i] << endl;
	}

	cout << endl;


	cout << "Revenue CAGRs: " << endl;
	cagr(revenue, numYears);
	cout << endl;

	cout << "Net Income CAGRs: " << endl;
	cagr(netIncome, numYears);
	cout << endl;
	
	cout << "Operating Cash CAGRs: " << endl;
	cagr(operatingCash, numYears);
	cout << endl;

	cout << "Equity CAGRs: " << endl;
	cagr(equityPlusDiv, numYears);
	cout << endl;


	double returnOnEquity;
	double returnOnInvestedCap;

	for (int i = 0; i < numYears; i++) {
		returnOnEquity = netIncome[i] / equity[i];
		returnOnInvestedCap = netIncome[i] / (equity[i] + longTermDebt[i]);
			
		cout << "Year " << i+1 << endl; 
		cout <<	"	ROE: " << returnOnEquity << endl;
		cout << "	ROIC: " << returnOnInvestedCap << endl;
		cout << "	Long-term Debt: " << longTermDebt[i] << endl;
		cout << endl;
	}
	
	
	bool findVal;
	cout << "Would you like to calculate the company's valuation? (0 for no, 1 for yes)" << endl;
	cin >> findVal;
	cout << endl;

	if (findVal == 1) {
		findMOS();
		cout << endl;
		findTenCap();
		cout << endl;
		findPayback();
		cout << endl;	
	}

	
	return 0;
}
