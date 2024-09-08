ClientEngagementMetrics = """
INSERT INTO 
    public.engagement_metrics(
        "ID", "Project ID", "EngagementID", "Customer ID", "Customer Name", "Engagement Date",
        "Revenue", "Revenue USD", "Service", "Sub-Service", "Engagement Type",
        "Employee Count", "Comments", "Project Ref", "Engagement Reference", "Client Revenue",
        "Service Type", "Detailed Sub-Service", "Revenue Currency", "Client Revenue Currency", "Load Date"
    )
    VALUES (
        %(ID)s, %(Project ID)s, %(EngagementID)s, %(Customer ID)s, %(Customer Name)s, %(Engagement Date)s,
        %(Revenue)s, %(Revenue USD)s, %(Service)s, %(Sub-Service)s, %(Engagement Type)s,
        %(Employee Count)s, %(Comments)s, %(Project Ref)s, %(Engagement Reference)s, %(Client Revenue)s,
        %(Service Type)s, %(Detailed Sub-Service)s, %(Revenue Currency)s, %(Client Revenue Currency)s, %(Load Date)s
    )
    ON CONFLICT ("ID")
    DO NOTHING

"""
