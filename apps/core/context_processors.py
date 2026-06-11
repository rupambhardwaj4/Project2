from .models import CompanyProfile


def company_context(request):
    try:
        company = CompanyProfile.load_cached()
        return {
            "company": company,
            "company_json": company.to_dict() if hasattr(company, "to_dict") else {}
        }
    except Exception:
        company = CompanyProfile()
        return {
            "company": company,
            "company_json": company.to_dict() if hasattr(company, "to_dict") else {}
        }
