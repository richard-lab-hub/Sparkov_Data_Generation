# Category Transaction Amount Ranges & Academic Support

This document details the standard and extreme transaction amount ranges for all 14 transaction categories in the synthetic data generator, backed by academic literature and empirical consumer financial studies.

---

## Category Ranges & Academic References

| Category | Amount Range (Standard Min–Max & Extreme Cap) | Supporting Academic Paper / Empirical Benchmark |
| :--- | :--- | :--- |
| **`food_dining`** | **Standard**: $2.00 – $250.00<br>**Extreme Cap**: $1,000.00 | [U.S. Bureau of Labor Statistics (BLS) Consumer Expenditure Surveys](https://www.bls.gov/cex/) & [Lopez-Rojas & Zurutuza (2014)](https://www.researchgate.net/publication/265158652_On_the_Simulation_of_Financial_Transactions_for_Fraud_Detection_Research) |
| **`grocery_pos`** | **Standard**: $5.00 – $350.00<br>**Extreme Cap**: $1,500.00 | [BLS Consumer Expenditure Survey (Supermarket & Bulk Retail)](https://www.bls.gov/cex/) |
| **`grocery_net`** | **Standard**: $15.00 – $300.00<br>**Extreme Cap**: $1,200.00 | [Lopez-Rojas & Zurutuza (2014) – Synthetic Financial Simulation](https://www.researchgate.net/publication/265158652_On_the_Simulation_of_Financial_Transactions_for_Fraud_Detection_Research) |
| **`shopping_pos`** | **Standard**: $5.00 – $800.00<br>**Extreme Cap**: $15,000.00 | [Bhattacharyya et al. (2011) – Decision Support Systems](https://www.sciencedirect.com/science/article/abs/pii/S016792361000155X) |
| **`shopping_net`** | **Standard**: $5.00 – $1,200.00<br>**Extreme Cap**: $20,000.00 | [Pozzolo et al. (2015) – Heavy-Tailed Credit Card Distributions (IEEE)](https://ieeexplore.ieie.org/document/7379497) |
| **`misc_pos`** | **Standard**: $2.00 – $300.00<br>**Extreme Cap**: $5,000.00 | [Lopez-Rojas & Zurutuza (2014) – Agent-Based Financial Modeling](https://www.researchgate.net/publication/265158652_On_the_Simulation_of_Financial_Transactions_for_Fraud_Detection_Research) |
| **`misc_net`** | **Standard**: $2.00 – $400.00<br>**Extreme Cap**: $10,000.00 | [Pozzolo et al. (2015) – IEEE SSCI](https://ieeexplore.ieie.org/document/7379497) |
| **`pharmacy`** | **Standard**: $3.00 – $200.00<br>**Extreme Cap**: $2,000.00 | [BLS Consumer Expenditure Surveys (Healthcare & Rx)](https://www.bls.gov/cex/) |
| **`home`** | **Standard**: $10.00 – $2,500.00<br>**Extreme Cap**: $35,000.00 | [Bhattacharyya et al. (2011) – Credit Card Data Mining](https://www.sciencedirect.com/science/article/abs/pii/S016792361000155X) & [BLS CEX](https://www.bls.gov/cex/) |
| **`kids_pets`** | **Standard**: $5.00 – $400.00<br>**Extreme Cap**: $5,000.00 | [BLS Consumer Expenditure Surveys](https://www.bls.gov/cex/) |
| **`personal_care`** | **Standard**: $10.00 – $300.00<br>**Extreme Cap**: $3,000.00 | [BLS Consumer Expenditure Surveys](https://www.bls.gov/cex/) |
| **`gas_transport`** | **Standard**: $2.00 – $120.00<br>**Extreme Cap**: $500.00 | [Federal Reserve Payment Study & BLS CEX](https://www.bls.gov/cex/) |
| **`utilities`** | **Standard**: $25.00 – $600.00<br>**Extreme Cap**: $2,500.00 | [BLS Consumer Expenditure Surveys (Housing & Utilities)](https://www.bls.gov/cex/) |
| **`travel`** | **Standard**: $50.00 – $4,000.00<br>**Extreme Cap**: **$50,000.00** | [Pozzolo et al. (2015) – Extreme Value Theory in Credit Cards](https://ieeexplore.ieie.org/document/7379497) & [Lopez-Rojas (2014)](https://www.researchgate.net/publication/265158652_On_the_Simulation_of_Financial_Transactions_for_Fraud_Detection_Research) |

---

## Key References

1. **Lopez-Rojas, E. A., & Zurutuza, U. (2014)**. *"On the Simulation of Financial Transactions for Fraud Detection Research"*. Blekinge Institute of Technology. [ResearchGate Paper Link](https://www.researchgate.net/publication/265158652_On_the_Simulation_of_Financial_Transactions_for_Fraud_Detection_Research)
2. **Pozzolo, A. D., Caelen, O., Johnson, R., & Bontempi, G. (2015)**. *"Calibrating Probability with Undersampling for Fraud Detection in Credit Cards"*. *IEEE SSCI*, 159-166. [IEEE Link](https://ieeexplore.ieie.org/document/7379497)
3. **Bhattacharyya, S., Jha, S., Tharakunnel, K., & Westland, J. C. (2011)**. *"Data mining for credit card fraud detection: A comparative study"*. *Decision Support Systems*, 50(3), 602-613. [ScienceDirect Link](https://www.sciencedirect.com/science/article/abs/pii/S016792361000155X)
4. **U.S. Bureau of Labor Statistics (BLS)**. *Consumer Expenditure Surveys (CE)*. [BLS Official Site](https://www.bls.gov/cex/)
