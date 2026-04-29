def calculate_risk_score(data_access_level: str, oauth_scopes: list, compliance_certs: list) -> int:
    """
    Calculate risk score based on data access, OAuth scopes, and compliance certifications.
    Returns a score from 0-100.
    """
    
    # Data Access Points
    data_access_points = {
        "none": 0,
        "read-only": 15,
        "read-write": 30,
        "admin": 40
    }
    data_score = data_access_points.get(data_access_level.lower(), 0)
    
    # OAuth Scope Points (cumulative)
    oauth_points = {
        "email": 5,
        "profile": 8,
        "files": 15,
        "write": 20,
        "admin": 35
    }
    oauth_score = sum(oauth_points.get(scope.lower(), 0) for scope in oauth_scopes)
    
    # Compliance Reductions (stacking)
    compliance_reductions = {
        "soc2": -5,
        "iso27001": -5,
        "gdpr": -8,
        "hipaa": -10
    }
    compliance_score = sum(compliance_reductions.get(cert.lower(), 0) for cert in compliance_certs)
    
    # Calculate final score
    final_score = data_score + oauth_score + compliance_score
    final_score = max(0, min(100, final_score))
    
    return final_score


def get_rating(risk_score: int) -> str:
    """
    Get traffic-light rating based on risk score.
    """
    if risk_score <= 30:
        return "green"
    elif risk_score <= 60:
        return "amber"
    else:
        return "red"
