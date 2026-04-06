"""
Marketing task: Marketing Manager role for marketing/communications students.
"""

MARKETING_TASK = {
    "task_id": "task_marketing_001",
    "difficulty": "marketing",
    "job_key": "job_marketing_001",
    "resume_pool": "marketing",
    # Emily has all required skills (Marketing Strategy, Campaign Management, Analytics)
    # Frank is missing Marketing Strategy and Analytics
    # Grace is a sales professional with no marketing background
    # Henry is a designer with no marketing strategy or analytics
    "correct_candidate_ids": ["c_mkt_001"],
    "description": (
        "Select the best candidate(s) for a Marketing Manager role. "
        "Emily is a marketing degree holder with all required skills. "
        "Frank is a content writer missing strategy and analytics. "
        "Grace is in sales. Henry is a graphic designer."
    ),
}
