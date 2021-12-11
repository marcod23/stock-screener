from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import xlsxwriter
import sys, traceback
import time


def zoom_in(driver):

    driver.get('chrome://settings/')
    time.sleep(1)
    driver.execute_script("setTimeout(function(){chrome.settingsPrivate.setDefaultZoom(1.00);}, 5);")
    time.sleep(1)
    driver.execute_script("window.history.go(-1)")
    time.sleep(3)


def zoom_out(driver):

    driver.get('chrome://settings/')
    time.sleep(1)
    driver.execute_script("setTimeout(function(){chrome.settingsPrivate.setDefaultZoom(0.5);}, 5);")
    time.sleep(1)
    driver.execute_script("window.history.go(-1)")
    time.sleep(3)


def navigate_to_data(driver):

    driver.get("https://stockrow.com")
    time.sleep(5)
    
    search = driver.find_element_by_css_selector(".Select-input > input:nth-child(1)")
    search.send_keys('aapl')
    time.sleep(3)
    search.send_keys('\n')
    time.sleep(4)
  
    navi = driver.find_element_by_class_name("hamburger-icon")
    navi.click()
    navi = driver.find_element_by_css_selector("li.has-drop-down:nth-child(10) > a:nth-child(1)")
    navi.click()
    navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.navigation-submenu > div > div.third-level > a:nth-child(2)")
    navi.click()
    time.sleep(3)
    navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.company-financials > div > div.grid-x.align-center.grid-margin-x.control-buttons > div.cell.medium-5 > button")
    navi.click()
    time.sleep(4)
    zoom_out(driver)
    

def get_data(driver):

    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    #result = soup.find(id='root')
    values = soup.find_all('div', class_= 'financials-value')
    
    value_list = []
    for value in values:
        value_list.append(value.text)

    while '' in value_list:
        value_list.remove('')
    
    return value_list


def count_dates(data):
    
    count = 0
    p = re.compile('[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}')
    
    for d in data:
        m = p.match(d)
        if m:
            count += 1

    return count


def get_values(data, financial_str):
    
    values = []
    num_years = count_dates(data)
    
    if financial_str in data:
        start = data.index(financial_str)
        index = data.index(financial_str, start+1)
        values = data[index+1:index+(num_years+1)]
    else:
        for x in range(num_years):
            values.append('0')
    
    return values


def not_all_positive(num_list):

    positive_nums = 0
    are_negatives = True
    
    for x in range(10):
        if num_list[x].find('(') == -1:
            positive_nums += 1
    
    if positive_nums == 10:
        are_negatives = False

    return are_negatives


def string_to_num(data):
    
    new_data = []
    data_decimals = []

    for d in data:
        nd = d.replace(',', '')
        nnd = nd.replace('(', '')
        nnnd = nnd.replace(')', '')
        new_data.append(nnnd)

    for d in new_data:
        nd = float(d)
        data_decimals.append(nd)

    return data_decimals


def calculate_growth(data):

    growth = []
    
    for x in range(9):
        if data[x] == 0:
            growth.append(1000000)
        else:
            num = (data[x+1] / data[x]) - 1
            num *= 100
            num = round(num, 2)
            growth.append(num)

    return growth


def consistent_growth(data):

    positive_nums = 0
    consistent = False

    for x in range(9):
        if data[x] >= 0:
            positive_nums += 1

    if positive_nums >= 7:
        consistent = True

    return consistent


def set_up_table(worksheet, ticker, bold, row):
    
    info = ["Revenue Growth", "Net Income Growth", "Equity Growth", "Operating Cash Growth", "Profit Margin", "Quick Ratio", "Debt to Equity", "Long Term Debt", "Free Cash Flow", "ROE", "ROIC", "Cash ROIC", "CAGRs", "Revenue", "Net Income", "Equity", "Operating Cash"]
    years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    cagr_years = ["9 year", "7 year", "5 year", "3 year"]
    col = 0
    
    worksheet.set_column(0, 0, len("Operating Cash Growth"))
    worksheet.write(row, col, ticker, bold)

    for year in years:
        col += 1
        worksheet.write(row, col, year, bold)
    
    col = 0
    for i in info:
        row += 1
        if i == "CAGRs":
            for y in cagr_years:
                col += 1
                worksheet.write(row, col, y, bold)
        worksheet.write(row, 0, i)


def output_data(worksheet, row, data):

    if len(data) == 9:
        col = 2
    else:
        col = 1

    for d in data:
        worksheet.write(row, col, d)
        col += 1


def calculate_pm(revenue, netinc):

    profit_margin = []

    for (r, ni) in zip(revenue, netinc):
        if r == 0:
            profit_margin.append(0)
        else:
            pm = ni / r
            pm *= 100
            pm = round(pm, 2)
            profit_margin.append(pm)

    return profit_margin


def dash_to_zero(data):

    new_data = []

    for d in data:
        nd = d.replace('—', '0')
        new_data.append(nd)

    return new_data


def calculate_qr(cash, receivables, currliab):
    
    quick_ratio = []

    for (c, r, cl) in zip(cash, receivables, currliab):
        if cl == 0:
            quick_ratio.append(0)
        else:
            qr = (c + r) / cl
            qr = round(qr, 2)
            quick_ratio.append(qr)

    return quick_ratio


def calculate_de(noncurrliab, shortdebt, equity):

    debt_equity = []

    for (ncl, sd, e) in zip(noncurrliab, shortdebt, equity):
        if e == 0:
            debt_equity.append(0)
        else:
            de = (ncl + sd) / e
            de = round(de, 2)
            debt_equity.append(de)

    return debt_equity


def calculate_fcf(opcash, capex, intangible):

    free_cash_flow = []

    for (oc, ce, i) in zip(opcash, capex, intangible):
        fcf = oc - (ce + i)
        fcf = round(fcf, 2)
        free_cash_flow.append(fcf)

    return free_cash_flow


def calculate_roe(netinc, equity):

    return_on_equity = []

    for (ni, e) in zip(netinc, equity):
        if e == 0:
            return_on_equity.append(0)
        else:
            roe = ni / e
            roe *= 100
            roe = round(roe, 2)
            return_on_equity.append(roe)

    return return_on_equity


def calculate_roic(equity, longdebt, shortdebt, operinc, inctax, ebt):
    
    return_invested_capital = []
    nopat = []
    invested_cap = []

    for (oi, it, e) in zip(operinc, inctax, ebt):
        if e == 0:
            nopat.append(0)
        else:
            tax_rate = it / e
            n = oi * (1 - tax_rate)
            nopat.append(n)

    for (e, ld, sd) in zip(equity, longdebt, shortdebt):
        ic = e + ld + sd
        invested_cap.append(ic)

    for (n, ic) in zip(nopat, invested_cap):
        if ic == 0:
            return_invested_capital.append(0)
        else:
            roic = n / ic
            roic *= 100
            roic = round(roic, 2)
            return_invested_capital.append(roic)

    return return_invested_capital


def calculate_croic(free_cflow, equity, longdebt, shortdebt):

    cash_roic = []
    invested_cap = []

    for (e, ld, sd) in zip(equity, longdebt, shortdebt):
        ic = e + ld + sd
        invested_cap.append(ic)

    for (fcf, ic) in zip(free_cflow, invested_cap):
        if fcf < 0 or ic == 0:
            cash_roic.append(0)
        else:
            croic = fcf / ic
            croic *= 100
            croic = round(croic, 2)
            cash_roic.append(croic)

    return cash_roic


def calculate_cagrs(data):

    cagrs = []

    if data[0] == 0: data[0] = 0.00001 
    if data[2] == 0: data[2] = 0.00001 
    if data[4] == 0: data[4] = 0.00001 
    if data[6] == 0: data[6] = 0.00001
        
    nine = ((data[9] / data[0]) ** (1/9)) - 1
    seven = ((data[9] / data[2]) ** (1/7)) - 1
    five = ((data[9] / data[4]) ** (1/5)) - 1
    three = ((data[9] / data[6]) ** (1/3)) - 1
    
    clist = [nine, seven, five, three]
    
    for c in clist:
        c *= 100
        c = round(c, 2)
        cagrs.append(c)
        
    return cagrs


def count_positives(data):

    positive_nums = 0

    for d in data:
        if d > 0:
            positive_nums += 1

    return positive_nums


#  MAIN STARTS HERE
#  program flow starts here 
#  everything above is functions used below

def main():

    driver = webdriver.Chrome()
    navigate_to_data(driver)
    
    workbook = xlsxwriter.Workbook('Cool Stocks.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    row_marker = 0

    f = open("stocks.txt", "r")
    
    try:
        
        for ticker in f:
            
            search = driver.find_element_by_css_selector(".Select-input > input:nth-child(1)")
            search.send_keys(ticker)
            time.sleep(2)
            search.send_keys('\n')
            time.sleep(3)

            if len(driver.find_elements_by_class_name('company-financials')) == 0:
                driver.get("https://stockrow.com/AAPL/financials/income/annual")
                time.sleep(5)
                continue
        
            data_list = get_data(driver)
            revenue_vals = get_values(data_list, 'Revenue')
            netinc_vals = get_values(data_list, 'Net Income Common')
            operinc_vals = get_values(data_list, 'Operating Income')
            inctax_vals = get_values(data_list, 'Income Tax Provision')
            ebt_vals = get_values(data_list, 'EBT')

            while '—' in revenue_vals: revenue_vals.remove('—')
            while '—' in netinc_vals: netinc_vals.remove('—')
            if len(revenue_vals) < 10 or len(netinc_vals) < 10: continue
            if not_all_positive(revenue_vals) or not_all_positive(netinc_vals): continue
            if len(revenue_vals) > 10 or len(netinc_vals) > 10:
                print("has more than 10 data points")
                print(ticker)
                continue
            
            zoom_in(driver)
            navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.navigation-submenu > div > div.second-level > a:nth-child(2)")
            navi.click()
            zoom_out(driver)
            
            data_list = get_data(driver)
            equity_vals = get_values(data_list, 'Shareholders Equity (Total)')
            cash_vals = get_values(data_list, 'Cash and Short Term Investments')
            receivable_vals = get_values(data_list, 'Receivables')
            currliab_vals = get_values(data_list, 'Total current liabilities')
            noncurrliab_vals = get_values(data_list, 'Total non-current liabilities')
            shortdebt_vals = get_values(data_list, 'Current Part of Debt')
            longdebt_vals = get_values(data_list, 'Long Term Debt (Total)')

            while '—' in equity_vals: equity_vals.remove('—')
            if len(equity_vals) != 10 or not_all_positive(equity_vals):
                if len(equity_vals) > 10: 
                    print("has more than 10 data points")
                    print(ticker)
                zoom_in(driver)
                navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.navigation-submenu > div > div.second-level > a:nth-child(1)")
                navi.click()
                zoom_out(driver)
                continue
            
            zoom_in(driver)
            navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.navigation-submenu > div > div.second-level > a:nth-child(3)")
            navi.click()
            zoom_out(driver)

            data_list = get_data(driver)
            opcash_vals = get_values(data_list, 'Operating Cash Flow')
            dividend_vals = get_values(data_list, 'Dividends Paid (Common)')
            capex_vals = get_values(data_list, 'Capital expenditures')
            intangible_vals = get_values(data_list, 'Change in intangibles (net)')

            zoom_in(driver)
            navi = driver.find_element_by_css_selector("#root > div > div > section > div > div.main-content > div:nth-child(1) > section.grid-x.align-center.navigation-submenu > div > div.second-level > a:nth-child(1)")
            navi.click()
            zoom_out(driver)
            
            while '—' in opcash_vals: opcash_vals.remove('—')
            if len(opcash_vals) < 10 or not_all_positive(opcash_vals): continue
            if len(opcash_vals) > 10:
                print("has more than 10 data points")
                print(ticker)
                continue
            
            revenue_data = string_to_num(revenue_vals)
            netinc_data = string_to_num(netinc_vals)
            equity_data = string_to_num(equity_vals)
            opcash_data = string_to_num(opcash_vals)
            dividend_data = string_to_num(dividend_vals)
            
            revenue_growth = calculate_growth(revenue_data)        
            netinc_growth = calculate_growth(netinc_data)
            equity_growth = calculate_growth(equity_data)
            opcash_growth = calculate_growth(opcash_data)
            
            num = 0
            for div in dividend_data:
                num += div
            if num == 0 and not consistent_growth(equity_growth):
                continue

            if consistent_growth(revenue_growth) and consistent_growth(netinc_growth) and consistent_growth(opcash_growth):
                set_up_table(worksheet, ticker, bold, row_marker)
                row_marker += 1
                
                output_data(worksheet, row_marker, revenue_growth)
                row_marker += 1
                
                output_data(worksheet, row_marker, netinc_growth)
                row_marker += 1
                
                output_data(worksheet, row_marker, equity_growth)
                row_marker += 1
                
                output_data(worksheet, row_marker, opcash_growth)
                row_marker += 1
                
                profit_margin = calculate_pm(revenue_data, netinc_data)
                output_data(worksheet, row_marker, profit_margin)
                row_marker += 1
                
                if '—' in cash_vals: cash_vals = dash_to_zero(cash_vals)
                if '—' in receivable_vals: receivable_vals = dash_to_zero(receivable_vals)
                if '—' in currliab_vals: currliab_vals = dash_to_zero(currliab_vals)
                cash_data = string_to_num(cash_vals)
                receivable_data = string_to_num(receivable_vals)
                currliab_data = string_to_num(currliab_vals)
                quick_ratio = calculate_qr(cash_data, receivable_data, currliab_data)
                output_data(worksheet, row_marker, quick_ratio)
                row_marker += 1

                if '—' in noncurrliab_vals: noncurrliab_vals = dash_to_zero(noncurrliab_vals)
                if '—' in shortdebt_vals: shortdebt_vals = dash_to_zero(shortdebt_vals)
                noncurrliab_data = string_to_num(noncurrliab_vals)
                shortdebt_data = string_to_num(shortdebt_vals)
                debt_equity = calculate_de(noncurrliab_data, shortdebt_data, equity_data)
                output_data(worksheet, row_marker, debt_equity)
                row_marker += 1
                
                if '—' in longdebt_vals: longdebt_vals = dash_to_zero(longdebt_vals)
                longdebt_data = string_to_num(longdebt_vals)
                output_data(worksheet, row_marker, longdebt_data)
                row_marker += 1
                    
                if '—' in capex_vals: capex_vals = dash_to_zero(capex_vals)
                if '—' in intangible_vals: intangible_vals = dash_to_zero(intangible_vals)
                capex_data = string_to_num(capex_vals)
                intangible_data = string_to_num(intangible_vals)
                free_cash_flow = calculate_fcf(opcash_data, capex_data, intangible_data)
                output_data(worksheet, row_marker, free_cash_flow)
                row_marker += 1
                
                return_on_equity = calculate_roe(netinc_data, equity_data)
                output_data(worksheet, row_marker, return_on_equity)
                row_marker += 1

                if '—' in operinc_vals: operinc_vals = dash_to_zero(operinc_vals)
                if '—' in inctax_vals: inctax_vals = dash_to_zero(inctax_vals)
                if '—' in ebt_vals: ebt_vals = dash_to_zero(ebt_vals)
                operinc_data = string_to_num(operinc_vals)
                inctax_data = string_to_num(inctax_vals)
                ebt_data = string_to_num(ebt_vals)
                return_invested_capital = calculate_roic(equity_data, longdebt_data, shortdebt_data, operinc_data, inctax_data, ebt_data)
                output_data(worksheet, row_marker, return_invested_capital)
                row_marker += 1
                
                cash_roic = calculate_croic(free_cash_flow, equity_data, longdebt_data, shortdebt_data)
                output_data(worksheet, row_marker, cash_roic)
                row_marker += 2
                
                revenue_cagrs = calculate_cagrs(revenue_data)
                output_data(worksheet, row_marker, revenue_cagrs)
                row_marker += 1
                
                netinc_cagrs = calculate_cagrs(netinc_data)
                output_data(worksheet, row_marker, netinc_cagrs)
                row_marker += 1

                equity_cagrs = calculate_cagrs(equity_data)
                output_data(worksheet, row_marker, equity_cagrs)
                row_marker += 1

                opcash_cagrs = calculate_cagrs(opcash_data)
                output_data(worksheet, row_marker, opcash_cagrs)
                row_marker += 1

                rev_pcount = count_positives(revenue_growth)
                ninc_pcount = count_positives(netinc_growth)
                opc_pcount = count_positives(opcash_growth)
                rcagr_pcount = count_positives(revenue_cagrs)
                ncagr_pcount = count_positives(netinc_cagrs)
                ecagr_pcount = count_positives(equity_cagrs)
                ocagr_pcount = count_positives(opcash_cagrs)
                total1 = rev_pcount + ninc_pcount + opc_pcount
                total2 = rcagr_pcount + ncagr_pcount + ecagr_pcount + ocagr_pcount
                
                if total1 == 27 and total2 == 16: 
                    worksheet.write(row_marker, 0, 'very cool')
                elif rev_pcount >= 8 and ninc_pcount >= 8 and opc_pcount >= 8 and total2 == 16:
                    worksheet.write(row_marker, 0, 'pretty cool')
                
                row_marker += 2
            
    except:
        workbook.close()
        print(ticker)
        traceback.print_exc(file=sys.stdout)

    else:
        f.close()
        workbook.close()


if __name__ == "__main__":
    main()




