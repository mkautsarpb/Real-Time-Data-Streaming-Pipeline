select
    book_title,
    authors,
    original_language,
    first_published_year,
    sales_millions,
    genre,
    ingested_at
from {{ ref('stg_books') }}
