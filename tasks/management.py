"""
Management task: Product Manager role for business/management students.
"""

MANAGEMENT_TASK = {
    "task_id": "task_management_001",
    "difficulty": "management",
    "job_key": "job_management_001",
    "resume_pool": "management",
    # Sarah has all required skills (Product Strategy, Roadmap Planning, Stakeholder Management)
    # Mike is missing Product Strategy and Roadmap Planning
    # Lisa is an engineer with no management skills
    # Tom is a marketer with no product management skills
    "correct_candidate_ids": ["c_mgmt_001"],
    "description": (
        "Select the best candidate(s) for a Product Manager role. "
        "Sarah is an MBA graduate with all required product management skills. "
        "Mike is a project manager missing key product skills. "
        "Lisa is a software engineer. Tom is a marketing manager."
    ),
}
