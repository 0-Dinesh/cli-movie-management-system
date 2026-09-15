# Role-Based Movie Catalog & Recommendation System

A command-line database application written in Python that manages a movie catalog using SQLite3, featuring role-based access control (RBAC), CSV batch processing, and custom query filters.

---

## Key Features

- **Role-Based Access Control:** Validates email strings via regular expressions to partition administrative permissions (`@movsys.com`) from standard consumer workflows.
- **Persistent Storage:** Executes parameterized SQL operations against an embedded SQLite3 database to ensure transactional integrity and prevent SQL injection.
- **Batch CSV Ingestion:** Parses external comma-separated datasets into the relational schema with structural error-handling for malformed rows.
- **Catalog Query Engine:** Supports real-time filtering by release year, genre taxonomy, or pseudo-random recommendation generation.

---

## System Architecture & Roles

```text
                    [ User Authentication ]
                               │
                      Regex Email Validator
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
      [ Admin Privileges ]            [ Standard User ]
   Domain: *@movsys.com           Domain: Any valid format
  ─────────────────────────      ─────────────────────────
  • Add Single Movie             • View Filtered by Genre
  • Update Catalog Metadata      • View Filtered by Year
  • Remove Record                • Random Movie Selector
  • Batch Import (CSV)           • View Complete Catalog
  • Display Full Catalog
  ```

  ## Project Structure

  ```text
  
├── data/
│   └── sample_movies.csv
├── .gitignore
├── LICENSE
├── main.py
└── README.md

  ```

  ## Getting Started

**Prerequisites:**

Python 3.8+ installed (uses Python standard libraries: `sqlite3`, `csv`, `re`, `random`).

**Installation & Execution:**

1. Clone or download this repository:
```bash
git clone https://github.com/your-username/cli-movie-management-system.git
cd cli-movie-management-system
```

2. Run the application:
```bash
python main.py
```

3. Access the system:

- For Admin Mode: Input an email ending in `@movsys.com` (e.g., `admin@movsys.com`).
- For User Mode: Input any standard formatted email (e.g., `user@gmail.com`).


## Data Ingestion Format

To batch-import movie records, provide a CSV file formatted without headers containing exactly three attributes per record:

```
Inception,Sci-Fi,2010
The Godfather,Crime,1972
Interstellar,Sci-Fi,2014
Spirited Away,Animation,2001
```

## License

This project is open-source and distributed under the MIT License.
