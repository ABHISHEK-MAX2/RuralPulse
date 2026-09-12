from retriever import MedicalRetriever

def run_tests():
    retriever = MedicalRetriever()

    test_queries = [
        {
            "category": "Level 1 / 2 (Cardiac / High Risk)",
            "query": "Patient presents with acute substernal chest pressure radiating to the left arm, diaphoresis, and shortness of breath."
        },
        {
            "category": "Decision Point D (Pediatric Fever)",
            "query": "A 3-week-old baby presents with a rectal fever of 101 degrees Fahrenheit and poor feeding."
        },
        {
            "category": "Level 4 (Single Resource / Minor Injury)",
            "query": "Healthy adult twisted ankle playing sports, needs an ankle x-ray, bearing weight is painful."
        }
    ]

    for item in test_queries:
        print("=" * 80)
        print(f"TEST CATEGORY: {item['category']}")
        print(f"QUERY: {item['query']}")
        print("=" * 80)

        results = retriever.get_top_k(item["query"], k=2)
        for i, res in enumerate(results, 1):
            print(f"\n--- [MATCH {i} | Page {res['page']}] ---")
            print(res["text"].strip())
        print("\n")

if __name__ == "__main__":
    run_tests()