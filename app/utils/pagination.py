# app/utils/pagination.py
from flask import request


def parametros_paginacao(padrao_por_pagina: int = 10, maximo_por_pagina: int = 100):
    try:
        pagina = int(request.args.get("page", 1))
    except (TypeError, ValueError):
        pagina = 1
    try:
        por_pagina = int(request.args.get("per_page", padrao_por_pagina))
    except (TypeError, ValueError):
        por_pagina = padrao_por_pagina

    pagina = max(pagina, 1)
    por_pagina = min(max(por_pagina, 1), maximo_por_pagina)
    return pagina, por_pagina


def serializar_paginacao(paginacao, schema) -> dict:
    return {
        "items": schema.dump(paginacao.items),
        "page": paginacao.page,
        "per_page": paginacao.per_page,
        "total": paginacao.total,
        "pages": paginacao.pages,
    }