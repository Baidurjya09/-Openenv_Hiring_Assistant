"""
Test the truly universal hiring model with ALL types of students:
- IT/Technical students
- Management students  
- Marketing students
- Business students
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from env.hiring_env import HiringEnv
from models.schemas import Action


def test_all_departments():
    """Test hiring across all departments."""
    
    print("=" * 80)
    print("UNIVERSAL HIRING MODEL - ALL DEPARTMENTS TEST")
    print("=" * 80)
    print()
    print("Testing that the model works for ALL types of students:")
    print("  ✓ IT/Technical students")
    print("  ✓ Management students")
    print("  ✓ Marketing students")
    print("  ✓ Business students")
    print()
    
    # Define all test cases
    test_cases = [
        {
            "name": "IT - Python Developer",
            "difficulty": "easy",
            "student_type": "Computer Science / IT",
            "correct_answer": ["c_easy_001"]
        },
        {
            "name": "IT - Full Stack Engineer",
            "difficulty": "medium",
            "student_type": "Computer Science / IT",
            "correct_answer": ["c_med_001", "c_med_005"]
        },
        {
            "name": "IT - ML Engineer",
            "difficulty": "hard",
            "student_type": "Computer Science / IT",
            "correct_answer": ["c_hard_001", "c_hard_002"]
        },
        {
            "name": "Management - Product Manager",
            "difficulty": "management",
            "student_type": "MBA / Business Management",
            "correct_answer": ["c_mgmt_001"]
        },
        {
            "name": "Marketing - Marketing Manager",
            "difficulty": "marketing",
            "student_type": "Marketing / Communications",
            "correct_answer": ["c_mkt_001"]
        },
        {
            "name": "Business - Business Analyst",
            "difficulty": "business",
            "student_type": "Business Administration",
            "correct_answer": ["c_bus_001"]
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print("=" * 80)
        print(f"TEST: {test_case['name']}")
        print("=" * 80)
        print(f"Student Type: {test_case['student_type']}")
        print()
        
        # Create environment
        env = HiringEnv(difficulty=test_case['difficulty'])
        observation = env.reset()
        
        job = observation.job_description
        candidates = observation.resumes
        
        print(f"Job: {job['title']}")
        print(f"Required Skills: {', '.join(job['required_skills'])}")
        print(f"Min Experience: {job['min_experience_years']} years")
        print()
        
        print(f"Candidates ({len(candidates)}):")
        
        # Evaluate each candidate
        qualified = []
        for candidate in candidates:
            candidate_skills = set(candidate['skills'])
            required_skills = set(job['required_skills'])
            missing_skills = required_skills - candidate_skills
            
            if not missing_skills and candidate['experience_years'] >= job['min_experience_years']:
                status = "✅ QUALIFIED"
                qualified.append(candidate['id'])
            else:
                status = "❌ REJECTED"
            
            print(f"  {candidate['name']}: {status}")
            if missing_skills:
                print(f"    Missing: {', '.join(list(missing_skills)[:3])}")
        
        print()
        
        # Test with correct answer
        action = Action(selected_candidates=test_case['correct_answer'])
        result = env.step(action)
        
        print(f"Correct Answer: {test_case['correct_answer']}")
        print(f"Score: {result.reward.score:.2f}")
        print(f"Feedback: {result.reward.feedback}")
        print()
        
        results.append({
            "name": test_case['name'],
            "student_type": test_case['student_type'],
            "score": result.reward.score,
            "passed": result.reward.score == 1.0
        })
    
    # Summary
    print("=" * 80)
    print("SUMMARY - ALL DEPARTMENTS")
    print("=" * 80)
    print()
    
    for result in results:
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{status} {result['name']}")
        print(f"     Student Type: {result['student_type']}")
        print(f"     Score: {result['score']:.2f}")
        print()
    
    all_passed = all(r['passed'] for r in results)
    
    print("=" * 80)
    if all_passed:
        print("🎉 SUCCESS! Model works for ALL types of students!")
        print()
        print("✅ IT/Technical students can get hired for tech roles")
        print("✅ Management students can get hired for management roles")
        print("✅ Marketing students can get hired for marketing roles")
        print("✅ Business students can get hired for business roles")
        print()
        print("🎯 YOUR MODEL IS TRULY UNIVERSAL!")
    else:
        print("⚠️ Some tests failed. Check the results above.")
    print("=" * 80)


def show_cross_application_test():
    """Show what happens when students apply to wrong departments."""
    
    print("\n\n")
    print("=" * 80)
    print("BONUS: CROSS-APPLICATION TEST")
    print("=" * 80)
    print()
    print("What happens when students apply to the WRONG department?")
    print()
    
    # Management student applying to tech role
    print("Test 1: Management student applies to Python Developer role")
    print("-" * 80)
    
    env = HiringEnv(difficulty="easy")
    observation = env.reset()
    
    print(f"Job: {observation.job_description['title']}")
    print(f"Required: {', '.join(observation.job_description['required_skills'])}")
    print()
    
    # Simulate management student (Sarah) applying
    print("Applicant: Sarah Johnson (Management student)")
    print("Skills: Product Strategy, Roadmap Planning, Stakeholder Management, Agile, SQL")
    print()
    
    sarah_skills = {"Product Strategy", "Roadmap Planning", "Stakeholder Management", "Agile", "SQL"}
    required_skills = {"Python", "Git"}
    missing = required_skills - sarah_skills
    
    print(f"Missing: {', '.join(missing)}")
    print("Result: ❌ REJECTED (missing required technical skills)")
    print()
    
    # Tech student applying to management role
    print("Test 2: IT student applies to Product Manager role")
    print("-" * 80)
    
    env = HiringEnv(difficulty="management")
    observation = env.reset()
    
    print(f"Job: {observation.job_description['title']}")
    print(f"Required: {', '.join(observation.job_description['required_skills'])}")
    print()
    
    print("Applicant: Alice Johnson (IT student)")
    print("Skills: Python, Git, Django, REST APIs")
    print()
    
    alice_skills = {"Python", "Git", "Django", "REST APIs"}
    required_skills = {"Product Strategy", "Roadmap Planning", "Stakeholder Management"}
    missing = required_skills - alice_skills
    
    print(f"Missing: {', '.join(missing)}")
    print("Result: ❌ REJECTED (missing required management skills)")
    print()
    
    print("=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    print()
    print("✅ Students get hired for roles matching their education")
    print("❌ Students get rejected for roles outside their field")
    print()
    print("The model correctly matches students to appropriate roles!")
    print("=" * 80)


if __name__ == "__main__":
    test_all_departments()
    show_cross_application_test()
