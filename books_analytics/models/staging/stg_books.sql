with source as (

    select *
    from {{ source('warehouse', 'books_silver') }}

)

select
    book_title,
    authors,
    original_language,
    first_published_year,
    sales_millions,
    genre,
    ingested_at
from source
