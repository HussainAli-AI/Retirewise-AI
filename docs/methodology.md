# RetireWise AI — Financial Methodology

## 1. Financial Health Formulation

### Net Worth & Capital Calculation
$$\text{Net Worth} = \text{Total Assets} - \text{Total Liabilities}$$
$$\text{Net Investable Capital} = \max(0, \text{Investable Retirement Assets} - \text{Total Liabilities})$$

### Monthly Retirement Gap
$$\text{Guaranteed Passive Income} = \text{Pension} + \text{Rental} + \text{Annuity/Other}$$
$$\text{Monthly Retirement Gap} = \max(0, \text{Projected Retirement Expenses} - \text{Guaranteed Passive Income})$$

### Emergency Reserve Adequacy Ratio
$$\text{Target Emergency Reserve} = \text{Target Months} \times \text{Essential Monthly Expenses}$$
$$\text{Reserve Adequacy Ratio} = \frac{\text{Liquid Cash and Equivalents}}{\text{Target Emergency Reserve}}$$

---

## 2. Multi-Year Retirement Simulation Math

For each year $t$ over the planning horizon:
1. **Expenses Adjusted for Inflation**:
   $$\text{Expenses}_t = \text{Base Retirement Expenses} \times (1 + i)^{t-1}$$
   where $i$ is the modeled annual inflation rate.
2. **Guaranteed Passive Income**:
   $$\text{Income}_t = \text{Base Guaranteed Income} \times (1 + 0.5 \times i)^{t-1}$$
   (Guaranteed income in Pakistan such as pensions typically features partial inflation indexation).
3. **Net Portfolio Withdrawal**:
   $$\text{Withdrawal}_t = \max(0, \text{Expenses}_t - \text{Income}_t) + \text{Shock}_t$$
4. **Portfolio Return & Ending Capital**:
   $$\text{Investment Return}_t = \max\left(0, \left(\text{Capital}_{t-1} - \frac{\text{Withdrawal}_t}{2}\right) \times r\right)$$
   $$\text{Capital}_t = \max(0, \text{Capital}_{t-1} + \text{Investment Return}_t - \text{Withdrawal}_t)$$
   where $r$ is the nominal portfolio return. Withdrawals are timed using standard mid-year convention.

---

## 3. Stress Testing Scenarios

1. **Base Case**: Baseline expected return ($r$) and inflation ($i$).
2. **High Inflation Shock**: Inflation increases by $+5\%$ per annum with stagnant returns.
3. **Early Market Drawdown**: Returns depressed by $-4\%$ per annum across horizon.
4. **Healthcare Crisis Shock**: Lump-sum shock of PKR 2,500,000 in Year 3 plus $15\%$ ongoing healthcare expense elevation.
5. **Early Retirement Shock**: Retirement accelerated by 3 years.
