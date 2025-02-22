import pandas as pd
import random
import string


# Define a function to generate random titles, barcodes, and call numbers
def generate_sample_data(num_samples=100):
    titles = [
        "The dependent patient : a practitioner's guide",
        "Advanced Networking Concepts",
        "Modern Database Management",
        "Psychology: An Introduction",
        "The Art of Computer Programming",
        "Basic Economics",
        "Cognitive Science Essentials",
        "Principles of Microeconomics",
        "World History Overview",
        "Climate Change and Sustainability",
        "Artificial Intelligence: A Modern Approach",
        "Foundations of Quantum Mechanics",
        "Medical Terminology Simplified",
        "Anatomy & Physiology",
        "The Great Gatsby",
        "Modern Political Theory",
        "Sociology in Our Times",
        "Introduction to Cultural Anthropology",
        "Creative Writing 101",
        "Data Structures and Algorithms",
        "Digital Photography Handbook",
        "Marketing Principles and Strategies",
        "The Road to Financial Freedom",
        "Essentials of Nutrition",
        "Exploring Astronomy",
        "The World of Mathematics",
        "Basics of Mechanical Engineering",
        "Introduction to Philosophy",
        "Criminal Justice in America",
        "Environmental Science",
        "Essentials of Chemistry",
        "Introduction to Statistical Analysis",
        "Human Anatomy Atlas",
        "Understanding Physics",
        "Principles of Marketing",
        "Data Analytics for Business",
        "Biology: Concepts and Applications",
        "Modern Art History",
        "Introduction to Sociology",
        "Basics of Organic Chemistry",
        "World Politics Today",
        "Discrete Mathematics",
        "Electrical Engineering Principles",
        "Macroeconomics: Theory and Policy",
        "Introduction to Nursing",
        "Basic Calculus",
        "Physical Science Essentials",
        "Business Communication Skills",
        "Ethics: Theory and Practice",
        "History of the United States",
        "Introduction to Programming",
        "Digital Logic Design",
        "Operating System Concepts",
        "Mechanics of Materials",
        "Fluid Mechanics Essentials",
        "Understanding Genetics",
        "Fundamentals of Biochemistry",
        "Microbiology in Practice",
        "Introduction to Public Health",
        "Child Development",
        "Learning Psychology",
        "World Literature",
        "Classical Music Theory",
        "Introduction to Robotics",
        "Marine Biology",
        "Modern Physics",
        "Elementary Statistics",
        "Machine Learning Basics",
        "Cybersecurity Fundamentals",
        "The World of Cell Biology",
        "Entrepreneurship for Beginners",
        "Digital Marketing Essentials",
        "Introduction to Law",
        "Investment Strategies",
        "Neuroscience: Exploring the Brain",
        "Essentials of Linguistics",
        "History of Ancient Civilizations",
        "The Biology of Plants",
        "Genetics: A Conceptual Approach",
        "Introduction to Renewable Energy",
        "Sports Science and Exercise",
        "Forensic Science Fundamentals",
        "Machine Learning for Data Science",
        "Introduction to Veterinary Medicine",
        "Essentials of Neuroscience",
        "Introductory Biology",
        "Nutrition for Health",
        "World Economic History",
        "Introduction to Digital Arts",
        "Basics of Environmental Health",
        "Social Psychology",
        "Introduction to Geology",
        "Introduction to Ecology",
        "The Science of Weather",
        "Human Physiology",
        "Computer Systems Architecture",
        "Theories of Personality",
        "Introduction to Agriculture",
        "History of Philosophy",
        "Basics of Information Technology",
        "Introduction to Business",
        "Essentials of Physical Fitness",
    ]

    # Sample call numbers in a similar format to provided sample
    call_numbers = [
        f"BF {random.randint(100, 999)}.{random.randint(1, 99)} .{''.join(random.choices(string.ascii_uppercase, k=3))} {random.randint(1, 9)}{random.choice(['e', 'm', 'n', 'p'])} {random.randint(1900, 2023)}"
        for _ in range(num_samples)
    ]
    barcodes = [
        f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
        for _ in range(num_samples)
    ]

    # Randomly sample titles
    data = {
        "title": [random.choice(titles) for _ in range(num_samples)],
        "barcode": barcodes,
        "call_number": call_numbers,
    }

    return pd.DataFrame(data)


# Generate the sample data
sample_data = generate_sample_data(100)

# Save to CSV
sample_data_path = "sample_library_data.csv"
sample_data.to_csv(sample_data_path, index=False)

sample_data_path
