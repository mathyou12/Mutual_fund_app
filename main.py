from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Investment, SIP, FundPerformance, Base

app = FastAPI(title="Mutual Fund App – Analytics Enabled")

# Create tables
Base.metadata.create_all(bind=engine)

# -------------------------
# DB SESSION
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# MUTUAL FUNDS (STATIC LIST)
# -------------------------
funds = [
    {"id": 1, "name": "Union Large Cap Fund", "category": "Large Cap"},
    {"id": 2, "name": "ICICI Prudential Large Cap", "category": "Large Cap"},
    {"id": 3, "name": "Axis Large Cap", "category": "Large Cap"},
]

# -------------------------
# HELPER FUNCTIONS (DOCUMENT LOGIC)
# -------------------------
def category_average(db, category):
    records = db.query(FundPerformance).filter(
        FundPerformance.category == category
    ).all()
    returns = [r.return_1y for r in records]
    return round(sum(returns) / len(returns), 2)


def alpha(fund_return, benchmark_return):
    return round(fund_return - benchmark_return, 2)


def performance_tag(diff):
    if diff > 1:
        return "Superior Performance"
    elif diff >= -1:
        return "In-line Performance"
    else:
        return "Under Performance"

# -------------------------
# APIs
# -------------------------

@app.get("/")
def home():
    return {"message": "Mutual Fund App with Analytics Running"}

# -------------------------
# SEED FUND PERFORMANCE (ONE-TIME CALL)
# -------------------------
@app.post("/seed/fund-performance")
def seed_data(db: Session = Depends(get_db)):
    if db.query(FundPerformance).count() > 0:
        return {"message": "Data already seeded"}

    data = [
        ("Union Large Cap Fund", "Large Cap", 12.8, 8.5),
        ("ICICI Prudential Large Cap", "Large Cap", 11.6, 8.5),
        ("Axis Large Cap", "Large Cap", 6.3, 8.5),
    ]

    for fund, cat, ret, bench in data:
        db.add(
            FundPerformance(
                fund_name=fund,
                category=cat,
                return_1y=ret,
                benchmark_return=bench
            )
        )
    db.commit()

    return {"message": "Fund performance data seeded"}

# -------------------------
# FUND ANALYSIS (🔥 CORE FEATURE)
# -------------------------
@app.get("/funds/{fund_name}/analysis")
def analyze_fund(fund_name: str, db: Session = Depends(get_db)):
    fund = db.query(FundPerformance).filter(
        FundPerformance.fund_name == fund_name
    ).first()

    if not fund:
        return {"error": "Fund not found"}

    cat_avg = category_average(db, fund.category)
    alpha_val = alpha(fund.return_1y, fund.benchmark_return)
    diff_vs_cat = round(fund.return_1y - cat_avg, 2)

    return {
        "fund_name": fund.fund_name,
        "category": fund.category,
        "return_1y": fund.return_1y,
        "benchmark_return": fund.benchmark_return,
        "category_average": cat_avg,
        "alpha_vs_benchmark": alpha_val,
        "diff_vs_category_avg": diff_vs_cat,
        "performance_tag": performance_tag(diff_vs_cat)
    }
