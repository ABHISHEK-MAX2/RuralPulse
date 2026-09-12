from retriever import MedicalRetriever

def main():
    print("Loading Medical Retriever (Dev 2)...")
    retriever = MedicalRetriever()
    print("Retriever ready!\n")
    print("Type any patient symptom/scenario below to test (type 'exit' or 'q' to quit).\n")

    while True:
        try:
            query = input("Enter Patient Complaint / Symptoms: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "q", "quit"]:
                print("Exiting test.")
                break

            print("\nSearching ChromaDB guidelines...")
            # Retrieve top 2 most relevant excerpts
            results = retriever.get_top_k(query, k=2)

            print("\n" + "=" * 60)
            print(f"QUERY: {query}")
            print("=" * 60)

            if not results:
                print("No relevant context found.")
            else:
                for idx, item in enumerate(results, 1):
                    print(f"\n[Match {idx} | ESI Handbook Page {item['page']}]:")
                    print(item['text'].strip())

            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()