from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from io import BytesIO
from datetime import datetime
import openpyxl

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

expenses = []
counter = 0


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    total = sum(exp["amount"] for exp in expenses)
    return templates.TemplateResponse(
        request, "index.html",
        context={"expenses": expenses, "total": total}
    )


@app.post("/add")
async def add_expense(
    description: str = Form(...),
    amount: float = Form(...),
):
    global counter
    counter += 1
    expenses.append({
        "id": counter,
        "description": description,
        "amount": amount,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    return RedirectResponse(url="/", status_code=303)


@app.get("/download")
async def download_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    ws.append(["Description", "Amount", "Date"])

    for exp in expenses:
        ws.append([exp["description"], exp["amount"], exp["created_at"]])

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=expenses.xlsx"}
    )
