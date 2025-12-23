select distinct
    authors as author_name
from {{ ref('stg_books') }}
where authors is not null
