### Interactive Supermarket Simulation with Association Rule Mining

#### Author Information

- **Name**: Hazel Hernandez, Bryan Borge
- **Student ID**: 6463890, 6337476
- **Course**: CAI 4002 - Artificial Intelligence
- **Semester**: Fall 2025



#### System Overview

Our application imitates a supermarket environment where users can create or upload shopping transactions and apply rule mining algorithms. The system preprocesses noisy data and runs Apriori and Eclat mining algorithms in order to generate rules helping to identify which sets of products are usually bought together. After that, these discovered rules are used by the built-in recommendation engine to suggest product pairing and cross-sell opportunities.



#### Technical Stack

- **Language**: Python 3.x
- **Key Libraries**: pandas, streamlit, time
- **UI Framework**: Streamlit



#### Installation

##### Prerequisites
- Python 3.8+
- pip package manager

##### Setup
```bash
# Clone or extract project
cd [project-directory]

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```



#### Usage

##### 1. Load Data
- **Manual Entry**: Click items to create transactions
- **Import CSV**: Upload `sample_transactions.csv` using the "Upload CSV" tab. 

##### 2. Preprocess Data
- Click "Run Preprocessing"
- Review cleaning report showing:
  - empty transactions removed, 
  - duplicates cleaned, 
  - invalid items dropped, 
  - single-item rows removed.

##### 3. Run Mining
- Set minimum support and confidence thresholds
- Select Apriori or Eclat
- Click Run ALgorithm 
- View rule outputs, execution times, and total rules created

##### 4. Query Results
- Select product from dropdown
- The system uses rules from the selected algorithm 
- Shows:
  - Recommended products 
  - Confidence level 
  - Business strategy suggestions



#### Algorithm Implementation

##### Apriori
Implemented using horizontal data format. 
- Data structure: Horizontal data format
- Candidate generation: BFS
- Pruning strategy: support based

##### Eclat
Uses vertical data format with set intersections. 
- Data structure: TID-list
- Search strategy: Depth-first
- Intersection method: TID-list intersection



#### Performance Results

Tested on provided dataset (80-100 transactions after cleaning):

| Algorithm | Runtime (ms) | Rules Generated | Memory Usage |
|-----------|--------------|-----------------|--------------|
| Apriori   | [~25-60]     | [10-30]         | [Moderate]   |
| Eclat     | [~5-25]      | [10-30]         | [Higher TID] |

**Parameters**: min_support = 0.2, min_confidence = 0.5

**Analysis**: Eclat performed faster due to TID-list intersections, while Apriori generated similar rules but took longer due to repeated candidate generation.



#### Project Structure

```
project-root/
├── src/
│   ├── algorithms/
│   │   ├── apriori.py
│   │   ├── eclat.py
│   ├── preprocessing/
│   │   └── data_cleaning.py
├── data/
│   ├── sample_transactions.csv
│   └── products.csv
├── app.py
├── README.md
├── REPORT.pdf
└── requirements.txt
```



#### Data Preprocessing

Issues handled:
- Empty transactions: 5 removed
- Single-item transactions: 6 removed
- Duplicate items: 9 instances cleaned
- Case inconsistencies: standardized automatically
- Invalid items: 2 removed
- Extra whitespace: trimmed from all items



#### Testing

Verified functionality:
- [✓] CSV import and parsing
- [✓] All preprocessing operations
- [✓] Three algorithm implementations
- [✓] Interactive query system
- [✓] Performance measurement

Test cases:
- CSV containing empty rows → removed correctly
- Transactions containing invalid products → filtered 
- High support values → expected few or zero rules 
- Low support & high confidence → generated strong associations

#### Known Limitations

- Memory usage not measured
- High memory usage in ECLAT due to TID-list, the deeper the mining the more likely it is to run into memory issues. 
- Very large datasets may slow down Apriori significantly

#### AI Tool Usage

Used ChatGPT to further clarify which algorithms would be better for product/transactions files and also to recommend frameworks which convinced us of using Streamlit. Also used to understand and work around certain limitations of each algorithm.

#### Live Demo
https://data-mining-assignment-ec55ba5tkfhm2tamuwwulj.streamlit.app/

#### References

- Course lecture materials
- Streamlit documentation: https://docs.streamlit.io/
- Pandas documentation: https://pandas.pydata.org/docs/
