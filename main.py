from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.data_loader import dataLoader

app = FastAPI(title="Generador de Fichas Técnicas PCD - MICRO")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")


@app.get("/ficha-tecnica", response_class=HTMLResponse)
def get_ficha_tecnica(request: Request, code: str = Query(..., description="Código del inserto")):
    inserto = dataLoader.find_by_code(code)

    if inserto is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={
                "request": request,
                "codigo": code,
                "logo_path": "/assets/micro-logo.png",
                "css_path": "/static/styles.css"
            },
            status_code=404
        )

    context = {
        "request": request,
        "inserto": inserto,
        "logo_path": "/assets/micro-logo.png",
        "css_path": "/static/styles.css"
    }

    return templates.TemplateResponse(
        request=request,
        name="ficha-tecnica-inserto.html",
        context=context
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
