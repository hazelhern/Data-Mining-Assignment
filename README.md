### Interactive Supermarket Simulation with Association Rule Mining

#### Author Information

- **Name**: Hazel Hernandez, Bryan Borge
- **Student ID**: 6463890, 6337476
- **Course**: CAI 4002 - Artificial Intelligence
- **Semester**: Fall 2025



#### System Overview

[2-3 sentences describing what your application does]



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
- Click “Run Apriori + Eclat” 
- View rule outputs, execution times, and performance comparison table

##### 4. Query Results
- Select product from dropdown
- View associated items and recommendation strength
- Read the automatically generated business insights suggesting product placement strategy



#### Algorithm Implementation

##### Apriori
[2-3 sentences on your implementation approach]
- Data structure: [e.g., dictionary of itemsets]
- Candidate generation: [breadth-first, level-wise]
- Pruning strategy: [minimum support]

##### Eclat
[2-3 sentences on your implementation approach]
- Data structure: [e.g., TID-set representation]
- Search strategy: [depth-first]
- Intersection method: [set operations]

##### CLOSET
[2-3 sentences on your implementation approach]
- Data structure: [e.g., FP-tree / prefix tree]
- Mining approach: [closed itemsets only]
- Closure checking: [method used]



#### Performance Results

Tested on provided dataset (80-100 transactions after cleaning):

| Algorithm | Runtime (ms) | Rules Generated | Memory Usage |
|-----------|--------------|-----------------|--------------|
| Apriori   | [value]      | [value]         | [value]      |
| Eclat     | [value]      | [value]         | [value]      |
| CLOSET    | [value]      | [value]         | [value]      |

**Parameters**: min_support = 0.2, min_confidence = 0.5

**Analysis**: [1-2 sentences explaining performance differences]



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
- Case inconsistencies: [count] standardized
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
- [Describe 2-3 key test scenarios]



#### Known Limitations

- Memory usage not measured
- Very large datasets (10k+ transactions) may slow down Apriori significantly



#### AI Tool Usage

[Required: 1 paragraph describing which AI tools you used and for what purpose]

Example:
"Used ChatGPT for explaining Eclat algorithm vertical representation and debugging file parsing errors. Used GitHub Copilot for generating UI boilerplate code. All generated code was reviewed, tested, and adapted for this specific implementation."



#### References

- Course lecture materials
- Streamlit documentation: https://docs.streamlit.io/
- Pandas documentation: https://pandas.pydata.org/docs/