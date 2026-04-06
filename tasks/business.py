"""
Business task: Business Analyst role for business administration students.
"""

BUSINESS_TASK = {
    "task_id": "task_business_001",
    "difficulty": "business",
    "job_key": "job_business_001",
    "resume_pool": "business",
    # Jennifer has all required skills (Excel, SQL, Data Analysis, Business Requirements)
    # Kevin is missing SQL, Data Analysis, and Business Requirements
    # Laura is a data scientist missing Business Requirements and Excel
    # Mark is an accountant missing Data Analysis and SQL
    "correct_candidate_ids": ["c_bus_001"],
    "description": (
        "Select the best candidate(s) for a Business Analyst role. "
        "Jennifer is a business administration graduate with all required skills. "
        "Kevin is a recent graduate with limited experience. "
        "Laura is a data scientist. Mark is an accountant."
    ),
}
