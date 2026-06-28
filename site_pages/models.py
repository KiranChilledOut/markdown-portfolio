"""Models for site_pages.

Content is file-based markdown (see :mod:`site_pages.loader`), so there are no
content models here. The database is only used for Django's own bookkeeping
(sessions, auth, admin). If a future feature needs persistence (e.g. a contact
form or view counter), add the model here.
"""
