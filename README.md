Usage
-----

### Prerequisites

-   Python 3.8+

-   Required libraries (install via `pip install -r requirements.txt`):

    -   requests

    -   pydantic

    -   duckdb
 
    -   numpy
 
    -   pandas 

### Execution

1.  Clone the repository.

2.  Install dependencies using `pip install -r requirements.txt`.

3.  Run the script: `python main.py`.

### Output

-   Queries are executed and printed to the console.

-   A local DuckDB database file (`data_store.duckdb`) is created, containing the processed data.




### Design Choices for the Solution

1.  **Data Fetching**:

    -   Used Python's `requests` library for its simplicity and reliability in handling HTTP requests.

    -   Fetched data from `/posts` and `/users` endpoints of JSONPlaceholder API, ensuring the required data was obtained efficiently.

2.  **Data Validation**:

    -   Leveraged `Pydantic` models to validate and enforce the structure of the fetched data. This ensures the data aligns with expected schemas, reducing the risk of processing invalid inputs.

    -   Used Pydantic's modern features for type safety and easy debugging.

3.  **Data Storage**:

    -   Chose `DuckDB` for its lightweight nature and excellent performance for analytical queries on local storage.

    -   Structured tables for `posts` and `users` were created to store the data, ensuring easy querying.

4.  **Data Querying**:

    -   Performed analytical queries using SQL within `DuckDB` to extract insights like:

        -   Number of posts per user.

        -   The user who wrote the longest post (by body length).

        -   An additional query to identify the top users by total content length.

5.  **Code Organization**:

    -   Modularized the code into distinct functions for fetching, validating, storing, and querying data. This ensures readability, maintainability, and easier debugging.

    -   Type hints were added throughout the code to improve clarity and reduce errors during development.

6.  **Error Handling**:

    -   Incorporated basic error handling during API requests and DuckDB operations to ensure robustness.

7.  **Scalability and Reusability**:

    -   The use of DuckDB makes the solution scalable for handling larger datasets locally without significant overhead.

    -   Custom functions and reusable components make it adaptable for future modifications or integrations.

8.  **Efficiency**:

    -   Used DuckDB's in-memory processing capabilities for fast query execution.

    -   Efficient data validation with Pydantic ensures issues are caught early in the pipeline.

This design prioritizes simplicity, performance, and maintainability, while leveraging modern tools to achieve the project objectives.
