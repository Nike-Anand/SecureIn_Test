from flask import Flask, request, jsonify
from flask_cors import CORS
from database.db_config import get_db_connection
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/cpes', methods=['GET'])
def get_cpes():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    
    cursor.execute("SELECT COUNT(*) as total FROM cpes")
    total = cursor.fetchone()['total']
    
    
    cursor.execute("""
        SELECT id, cpe_title, cpe_22_uri, cpe_23_uri, reference_links, 
               cpe_22_deprecation_date, cpe_23_deprecation_date
        FROM cpes 
        ORDER BY id 
        LIMIT %s OFFSET %s
    """, (limit, offset))
    
    data = cursor.fetchall()
    
    
    for item in data:
        if item['reference_links']:
            item['reference_links'] = json.loads(item['reference_links'])
        if item['cpe_22_deprecation_date']:
            item['cpe_22_deprecation_date'] = str(item['cpe_22_deprecation_date'])
        if item['cpe_23_deprecation_date']:
            item['cpe_23_deprecation_date'] = str(item['cpe_23_deprecation_date'])
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'page': page,
        'limit': limit,
        'total': total,
        'data': data
    })

@app.route('/api/cpes/search', methods=['GET'])
def search_cpes():
    cpe_title = request.args.get('cpe_title', '')
    cpe_22_uri = request.args.get('cpe_22_uri', '')
    cpe_23_uri = request.args.get('cpe_23_uri', '')
    deprecation_date = request.args.get('deprecation_date', '')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    
    query = "SELECT * FROM cpes WHERE 1=1"
    params = []
    
    if cpe_title:
        query += " AND cpe_title LIKE %s"
        params.append(f"%{cpe_title}%")
    
    if cpe_22_uri:
        query += " AND cpe_22_uri LIKE %s"
        params.append(f"%{cpe_22_uri}%")
    
    if cpe_23_uri:
        query += " AND cpe_23_uri LIKE %s"
        params.append(f"%{cpe_23_uri}%")
    
    if deprecation_date:
        query += " AND (cpe_22_deprecation_date < %s OR cpe_23_deprecation_date < %s)"
        params.extend([deprecation_date, deprecation_date])
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    
    for item in data:
        if item['reference_links']:
            item['reference_links'] = json.loads(item['reference_links'])
        if item['cpe_22_deprecation_date']:
            item['cpe_22_deprecation_date'] = str(item['cpe_22_deprecation_date'])
        if item['cpe_23_deprecation_date']:
            item['cpe_23_deprecation_date'] = str(item['cpe_23_deprecation_date'])
    
    cursor.close()
    conn.close()
    
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
