from services.coda_client import get_docs, get_tables, get_rows
from services.scanner import check_unused, check_public,find_sensitive_fields

alerts = []

def scan():
    global alerts

    docs = get_docs()
    print("TOTAL DOCS:", len(docs))

    temp_alerts = []

    for doc in docs:
        print("DOC DATA:", doc)

        doc_id = doc.get('id')
        doc_name = doc.get('name')

        
        # UNUSED DOCUMENT CHECK
        
        try:
            if check_unused(doc):
                if not any(a["id"] == doc_id and a["type"] == "UNUSED_DOC" for a in temp_alerts):
                    temp_alerts.append({
                        "type": "UNUSED_DOC",
                        "doc": doc_name,
                        "id": doc_id,
                        "severity": "LOW"
                    })
        except Exception as e:
            print("Error in UNUSED check:", e)

        
        # PUBLIC DOCUMENT CHECK
        
        try:
            if check_public(doc):
                if not any(a["id"] == doc_id and a["type"] == "PUBLIC_DOC" for a in temp_alerts):
                    temp_alerts.append({
                        "type": "PUBLIC_DOC",
                        "doc": doc_name,
                        "id": doc_id,
                        "severity": "MEDIUM"
                    })
        except Exception as e:
            print("Error in PUBLIC check:", e)

        
        # SENSITIVE DATA CHECK
        
        try:
            tables = get_tables(doc_id)
            print("TABLES:", tables)

            for table in tables:
                table_id = table.get('id')

                rows = get_rows(doc_id, table_id)

                for row in rows:
                    row_id = row.get('id')  
                    text = str(row)

                    findings = find_sensitive_fields(text)

                    if findings:
                        if not any(a["id"] == doc_id and a["type"] == "SENSITIVE_DATA" for a in temp_alerts):
                            temp_alerts.append({
                                "type": "SENSITIVE_DATA",
                                "doc": doc_name,
                                "id": doc_id,
                                "table_id": table_id, 
                                "row_id": row_id,     
                                "severity": "HIGH",
                                "details": ", ".join(findings)
                            })            

        except Exception as e:
            print("Error in SENSITIVE check:", e)

    alerts = temp_alerts

    print("FINAL ALERTS:", alerts)