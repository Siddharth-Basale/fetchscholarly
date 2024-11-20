import streamlit as st
from scholarly import scholarly

def fetch_publications_by_scholar_id(scholar_id):
    try:
        # Search for the author using their Scholar ID
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author)  # Fill complete author details

        publications = []
        for pub in author['publications']:
            pub_details = scholarly.fill(pub)
            publications.append({
                'title': pub_details.get('bib', {}).get('title', 'N/A'),
                'year': pub_details.get('bib', {}).get('pub_year', 'N/A'),
                'venue': pub_details.get('bib', {}).get('venue', 'N/A'),
                'citation_count': pub_details.get('num_citations', 0)
            })

        return author['name'], publications

    except Exception as e:
        return None, str(e)

# Streamlit UI
st.title("Google Scholar Publications Fetcher")
st.write("Enter the Scholar ID to fetch the publication details.")

# Input for Scholar ID
scholar_id = st.text_input("Enter Scholar ID (e.g., rnaR6eEAAAAJ):", "")

if st.button("Fetch Publications"):
    if scholar_id.strip():
        st.write("Fetching publications...")
        author_name, publication_details = fetch_publications_by_scholar_id(scholar_id.strip())

        if publication_details:
            st.write(f"### Publications for {author_name}:")
            for idx, pub in enumerate(publication_details, start=1):
                st.write(
                    f"{idx}. **{pub['title']}** ({pub['year']}) - {pub['venue']}, "
                    f"Citations: {pub['citation_count']}"
                )
        else:
            st.error(f"Error: {publication_details}")
    else:
        st.error("Please enter a valid Scholar ID.")

